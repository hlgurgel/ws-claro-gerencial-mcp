"""Servidor MCP para integração com os WebServices SOAP do Claro Gerencial.

Expõe ferramentas (tools) para consulta e envio de dados via protocolo MCP,
permitindo que agentes de IA (como o opencode) interajam com o Claro Gerencial.
"""

import asyncio
import json
import os
import traceback

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .cliente_soap import (
    chamar_enviar_registros,
    chamar_gerar_arquivo,
    chamar_listar_entidades,
    chamar_obter_registros,
    chamar_obter_schema_xml,
    chamar_obter_status,
)
from .config import AMBIENTE, USUARIO, SENHA, obter_entidade, descrever_status
from .ferramentas import FERRAMENTAS

servidor = Server("ws-claro-gerencial-mcp")


def _resolver_credenciais(
    usuario: str | None = None,
    senha: str | None = None,
    ambiente: str | None = None,
) -> tuple[str, str, str]:
    usr = usuario or USUARIO
    pwd = senha or SENHA
    amb = ambiente or AMBIENTE

    if not usr or not pwd:
        raise ValueError(
            "Credenciais não fornecidas. Defina CLARO_USUARIO e CLARO_SENHA no .env "
            "ou passe usuario/senha nos argumentos da ferramenta."
        )
    return usr, pwd, amb


@servidor.list_tools()
async def listar_ferramentas() -> list[types.Tool]:
    return [
        types.Tool(
            name=f["name"],
            description=f["description"],
            inputSchema=f["inputSchema"],
        )
        for f in FERRAMENTAS
    ]


@servidor.call_tool()
async def executar_ferramenta(
    name: str,
    arguments: dict,
) -> list[types.TextContent]:
    try:
        resultado = await _rotear(name, arguments)
        texto = json.dumps(resultado, ensure_ascii=False, indent=2)
        return [types.TextContent(type="text", text=texto)]
    except ValueError as e:
        return [types.TextContent(type="text", text=str(e))]
    except Exception as e:
        detalhes = traceback.format_exc()
        return [
            types.TextContent(
                type="text",
                text=f"Erro ao executar '{name}': {e}\n\nDetalhes:\n{detalhes}",
            )
        ]


async def _rotear(nome: str, args: dict) -> dict:
    if nome == "listar_entidades":
        entidades = await chamar_listar_entidades()
        return {"entidades": entidades, "total": len(entidades)}

    elif nome == "obter_registros":
        entidade = obter_entidade(args["entidade"])
        if not entidade.tem_output:
            raise ValueError(f"Entidade '{entidade.nome}' não suporta consulta (output).")
        completa = args.get("completa", False)
        usr, pwd, _ = _resolver_credenciais(
            args.get("usuario"), args.get("senha"), args.get("ambiente")
        )
        return await chamar_obter_registros(entidade, usr, pwd, completa)

    elif nome == "gerar_arquivo":
        entidade = obter_entidade(args["entidade"])
        if not entidade.tem_output:
            raise ValueError(f"Entidade '{entidade.nome}' não suporta consulta (output).")
        ticket = args["ticket"]
        usr, pwd, _ = _resolver_credenciais(
            args.get("usuario"), args.get("senha"), args.get("ambiente")
        )
        return await chamar_gerar_arquivo(entidade, usr, pwd, ticket)

    elif nome == "enviar_registros":
        entidade = obter_entidade(args["entidade"])
        if not entidade.tem_input:
            raise ValueError(f"Entidade '{entidade.nome}' não suporta envio (input).")
        xml = args["xml"]
        usr, pwd, _ = _resolver_credenciais(
            args.get("usuario"), args.get("senha"), args.get("ambiente")
        )
        return await chamar_enviar_registros(entidade, usr, pwd, xml)

    elif nome == "obter_status":
        entidade = obter_entidade(args["entidade"])
        if not entidade.tem_input:
            raise ValueError(f"Entidade '{entidade.nome}' não suporta envio (input).")
        ticket = args["ticket"]
        usr, pwd, _ = _resolver_credenciais(
            args.get("usuario"), args.get("senha"), args.get("ambiente")
        )
        resultado = await chamar_obter_status(entidade, usr, pwd, ticket)
        status_codigo = resultado.get("Status", "")
        if status_codigo:
            resultado["StatusDescricao"] = descrever_status(int(status_codigo))
        return resultado

    elif nome == "obter_schema_xml":
        entidade = obter_entidade(args["entidade"])
        if not entidade.tem_input:
            raise ValueError(f"Entidade '{entidade.nome}' não suporta envio (input).")
        usr, pwd, _ = _resolver_credenciais(
            args.get("usuario"), args.get("senha"), args.get("ambiente")
        )
        return await chamar_obter_schema_xml(entidade, usr, pwd)

    else:
        raise ValueError(f"Ferramenta desconhecida: {nome}")


async def executar():
    """Inicia o servidor MCP via stdio."""
    async with stdio_server() as (leitura, escrita):
        await servidor.run(leitura, escrita, servidor.create_initialization_options())
