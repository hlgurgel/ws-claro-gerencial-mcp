"""Cliente SOAP para comunicação com os WebServices do Claro Gerencial."""

import asyncio
from typing import Any

import httpx
from zeep import AsyncClient
from zeep.transports import AsyncTransport

from .config import Entidade, montar_url

_TIMEOUT = httpx.Timeout(30.0, connect=15.0)
_TRANSPORTE = AsyncTransport(timeout=_TIMEOUT.seconds)


def _criar_cliente(wsdl_url: str) -> AsyncClient:
    """Cria um cliente SOAP assíncrono para uma URL WSDL."""
    return AsyncClient(wsdl_url + "?WSDL", transport=_TRANSPORTE)


async def chamar_enviar_registros(
    entidade: Entidade,
    usuario: str,
    senha: str,
    xml: str,
) -> dict[str, Any]:
    """Método EnviarRegistros (Input) — envia XML para importação.

    Retorna dict com chaves: Ticket, Erro, Conteudo, Mensagem.
    """
    url = montar_url(entidade, "input")
    cliente = _criar_cliente(url)
    try:
        resultado = await cliente.service.EnviarRegistros(
            Usuario=usuario,
            Senha=senha,
            Xml=xml,
        )
        return {
            "Ticket": resultado.Ticket if resultado.Ticket else "",
            "Erro": resultado.Erro if resultado.Erro else "NAO",
            "Conteudo": resultado.Conteudo if resultado.Conteudo else "",
            "Mensagem": resultado.Mensagem if resultado.Mensagem else "",
        }
    finally:
        await cliente.transport.session.close()


async def chamar_obter_schema_xml(
    entidade: Entidade,
    usuario: str,
    senha: str,
) -> dict[str, Any]:
    """Método ObterSchemaXml (Input) — obtém o XSD da entidade.

    Retorna dict com chaves: Ticket, Erro, Conteudo, Mensagem.
    """
    url = montar_url(entidade, "input")
    cliente = _criar_cliente(url)
    try:
        resultado = await cliente.service.ObterSchemaXml(
            Usuario=usuario,
            Senha=senha,
        )
        return {
            "Ticket": resultado.Ticket if resultado.Ticket else "",
            "Erro": resultado.Erro if resultado.Erro else "NAO",
            "Conteudo": resultado.Conteudo if resultado.Conteudo else "",
            "Mensagem": resultado.Mensagem if resultado.Mensagem else "",
        }
    finally:
        await cliente.transport.session.close()


async def chamar_obter_status(
    entidade: Entidade,
    usuario: str,
    senha: str,
    ticket: str,
) -> dict[str, Any]:
    """Método ObterStatus (Input) — consulta status de envio por ticket.

    Retorna dict com chaves: Ticket, Erro, Conteudo, Status, StatusDescricao, Mensagem.
    """
    url = montar_url(entidade, "input")
    cliente = _criar_cliente(url)
    try:
        resultado = await cliente.service.ObterStatus(
            Usuario=usuario,
            Senha=senha,
            Ticket=ticket,
        )
        return {
            "Ticket": resultado.Ticket if resultado.Ticket else "",
            "Erro": resultado.Erro if resultado.Erro else "NAO",
            "Conteudo": resultado.Conteudo if resultado.Conteudo else "",
            "Status": resultado.Status if resultado.Status else "",
            "StatusDescricao": resultado.StatusDescricao if resultado.StatusDescricao else "",
            "Mensagem": resultado.Mensagem if resultado.Mensagem else "",
        }
    finally:
        await cliente.transport.session.close()


async def chamar_obter_registros(
    entidade: Entidade,
    usuario: str,
    senha: str,
    completa: bool,
) -> dict[str, Any]:
    """Método ObterRegistros (Output) — obtém registros da entidade.

    Retorna dict com chaves: Ticket, Erro, Conteudo, Mensagem.
    """
    url = montar_url(entidade, "output")
    flag = "SIM" if completa else "NAO"
    cliente = _criar_cliente(url)
    try:
        resultado = await cliente.service.ObterRegistros(
            Usuario=usuario,
            Senha=senha,
            Completa=flag,
        )
        return {
            "Ticket": resultado.Ticket if resultado.Ticket else "",
            "Erro": resultado.Erro if resultado.Erro else "NAO",
            "Conteudo": resultado.Conteudo if resultado.Conteudo else "",
            "Mensagem": resultado.Mensagem if resultado.Mensagem else "",
        }
    finally:
        await cliente.transport.session.close()


async def chamar_gerar_arquivo(
    entidade: Entidade,
    usuario: str,
    senha: str,
    ticket: str,
) -> dict[str, Any]:
    """Método GerarArquivo (Output) — gera arquivo FTP a partir do ticket.

    Retorna dict com chaves: Ticket, Erro, Conteudo, Mensagem.
    """
    url = montar_url(entidade, "output")
    cliente = _criar_cliente(url)
    try:
        resultado = await cliente.service.GerarArquivo(
            Usuario=usuario,
            Senha=senha,
            Ticket=ticket,
        )
        return {
            "Ticket": resultado.Ticket if resultado.Ticket else "",
            "Erro": resultado.Erro if resultado.Erro else "NAO",
            "Conteudo": resultado.Conteudo if resultado.Conteudo else "",
            "Mensagem": resultado.Mensagem if resultado.Mensagem else "",
        }
    finally:
        await cliente.transport.session.close()


async def chamar_listar_entidades() -> list[dict[str, Any]]:
    """Lista todas as entidades disponíveis, com flags de disponibilidade.

    Útil para descoberta das entidades pelo agente de IA.
    """
    from .config import ENTIDADES

    return [
        {
            "slug": e.slug,
            "nome": e.nome,
            "descricao": e.descricao,
            "output": e.tem_output,
            "input": e.tem_input,
        }
        for e in ENTIDADES.values()
    ]
