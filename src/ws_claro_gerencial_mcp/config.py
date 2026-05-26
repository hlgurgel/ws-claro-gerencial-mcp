"""Configuração centralizada do projeto — variáveis de ambiente e mapeamento de entidades."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Carrega .env da raiz do projeto, se existir
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

AMBIENTE = os.getenv("CLARO_AMBIENTE", "homologacao")
USUARIO = os.getenv("CLARO_USUARIO", "")
SENHA = os.getenv("CLARO_SENHA", "")

URL_BASE_OUTPUT = os.getenv(
    "CLARO_URL_BASE_OUTPUT",
    "https://clarogerencial.redeinova.com.br/wsoutput",
)
URL_BASE_INPUT = os.getenv(
    "CLARO_URL_BASE_INPUT",
    "https://clarogerencial.redeinova.com.br/wsinput",
)
URL_SEGMENTO = "wsh" if AMBIENTE == "homologacao" else "ws"


@dataclass(frozen=True)
class Entidade:
    """Representa uma entidade do Claro Gerencial."""

    slug: str
    nome: str
    descricao: str
    tem_output: bool = True
    tem_input: bool = False


# Mapeamento de entidades disponíveis nos WebServices
ENTIDADES: dict[str, Entidade] = {
    "cidades": Entidade(
        slug="cidades",
        nome="Cidades",
        descricao="Cadastro de Cidades (IBGE)",
        tem_output=True,
        tem_input=False,
    ),
    "bairros": Entidade(
        slug="bairros",
        nome="Bairros",
        descricao="Cadastro de Bairros",
        tem_output=True,
        tem_input=True,
    ),
    "clientes": Entidade(
        slug="clientes",
        nome="Clientes",
        descricao="Cadastro de Clientes (PDVs)",
        tem_output=True,
        tem_input=True,
    ),
    "clientes_visitas": Entidade(
        slug="clientes_visitas",
        nome="ClientesVisitas",
        descricao="Cadastro de Visitas aos Clientes (dias e ordem)",
        tem_output=True,
        tem_input=True,
    ),
    "empresas": Entidade(
        slug="empresas",
        nome="Empresas",
        descricao="Cadastro de Empresas",
        tem_output=True,
        tem_input=False,
    ),
    "gerentes": Entidade(
        slug="gerentes",
        nome="Gerentes",
        descricao="Cadastro de Gerentes",
        tem_output=True,
        tem_input=True,
    ),
    "supervisores": Entidade(
        slug="supervisores",
        nome="Supervisores",
        descricao="Cadastro de Supervisores",
        tem_output=True,
        tem_input=True,
    ),
    "vendedores": Entidade(
        slug="vendedores",
        nome="Vendedores",
        descricao="Cadastro de Vendedores",
        tem_output=True,
        tem_input=True,
    ),
    "setores": Entidade(
        slug="setores",
        nome="Setores",
        descricao="Cadastro de Setores",
        tem_output=True,
        tem_input=True,
    ),
    "grupos": Entidade(
        slug="grupos",
        nome="Grupos",
        descricao="Cadastro de Grupos de Produtos",
        tem_output=True,
        tem_input=False,
    ),
    "motivos_visitas": Entidade(
        slug="motivos_visitas",
        nome="MotivosVisitas",
        descricao="Cadastro de Motivos de Visita",
        tem_output=True,
        tem_input=True,
    ),
    "produtos": Entidade(
        slug="produtos",
        nome="Produtos",
        descricao="Cadastro de Produtos",
        tem_output=True,
        tem_input=False,
    ),
    "segmentos": Entidade(
        slug="segmentos",
        nome="Segmentos",
        descricao="Cadastro de Segmentos",
        tem_output=True,
        tem_input=False,
    ),
    "tipos_clientes": Entidade(
        slug="tipos_clientes",
        nome="TiposClientes",
        descricao="Cadastro de Tipos de Clientes",
        tem_output=True,
        tem_input=True,
    ),
    "tipos_sinalizacoes": Entidade(
        slug="tipos_sinalizacoes",
        nome="TiposSinalizacoes",
        descricao="Cadastro de Tipos de Sinalizações",
        tem_output=True,
        tem_input=False,
    ),
    "clientes_sinalizacoes": Entidade(
        slug="clientes_sinalizacoes",
        nome="ClientesSinalizacoes",
        descricao="Cadastro de Sinalizações dos Clientes",
        tem_output=True,
        tem_input=True,
    ),
    "visitas": Entidade(
        slug="visitas",
        nome="Visitas",
        descricao="Movimentação de Visitas",
        tem_output=True,
        tem_input=True,
    ),
    "integradores": Entidade(
        slug="integradores",
        nome="Integradores",
        descricao="Cadastro de Integradores (POS/Recarga)",
        tem_output=True,
        tem_input=False,
    ),
    "pedidos": Entidade(
        slug="pedidos",
        nome="Pedidos",
        descricao="Movimentação de Pedidos de Venda",
        tem_output=True,
        tem_input=True,
    ),
    "chipsvendedor": Entidade(
        slug="chipsvendedor",
        nome="ChipsVendedor",
        descricao="Cadastro de Chips do Vendedor (MSISDN)",
        tem_output=True,
        tem_input=True,
    ),
    "motivos_iccid": Entidade(
        slug="motivos_iccid",
        nome="MotivosICCIDS",
        descricao="Cadastro de Motivos de Devolução ICCID",
        tem_output=True,
        tem_input=False,
    ),
    "iccid": Entidade(
        slug="iccid",
        nome="ICCID",
        descricao="Registro de ICCID (Venda/Estoque de Chips)",
        tem_output=True,
        tem_input=True,
    ),
    "redes_pdv": Entidade(
        slug="redes_pdv",
        nome="RedesPDV",
        descricao="Cadastro de Redes de PDVs",
        tem_output=True,
        tem_input=False,
    ),
    "vendas_banda_larga": Entidade(
        slug="vendas_banda_larga",
        nome="VendasBandaLarga",
        descricao="Registro de Vendas de Produto Banda Larga",
        tem_output=True,
        tem_input=True,
    ),
    "releituras_iccid": Entidade(
        slug="releituras_iccid",
        nome="ReleiturasICCID",
        descricao="Releituras de ICCIDs do PDV",
        tem_output=False,
        tem_input=True,
    ),
}


def obter_entidade(slug: str) -> Entidade:
    """Obtém uma entidade pelo slug. Lança ValueError se não encontrada."""
    entidade = ENTIDADES.get(slug)
    if entidade is None:
        slugs_validos = ", ".join(sorted(ENTIDADES.keys()))
        raise ValueError(
            f"Entidade '{slug}' não encontrada. Entidades disponíveis: {slugs_validos}"
        )
    return entidade


def montar_url(entidade: Entidade, direcao: str) -> str:
    """Monta a URL completa do WebService para uma entidade e direção (input/output).

    Em homologação usa /wsh/; em produção usa /ws/.
    """
    base = URL_BASE_INPUT if direcao == "input" else URL_BASE_OUTPUT
    return f"{base}/{URL_SEGMENTO}/{entidade.slug}/servico.asmx"


STATUS_ENVIO: dict[int, str] = {
    0: "Na Fila para importação",
    1: "Registros sendo transferidos para o SGR do Distribuidor",
    2: "Verificar preenchimento das informações dos registros transferidos",
    3: "Verificar se os registros de exclusão são registros já cadastrados",
    4: "Verificar se não existem registros de inclusão repetidos no XML",
    5: "Verificar se os campos contendo informações de cadastros relacionados",
    6: "Atualizar log de registros para Inclusão",
    7: "Atualizar log de registros para Alteração",
    8: "Atualizar log de registros para Exclusão",
    9: "Envio Finalizado",
    99: "Erro ao Enviar",
}


def descrever_status(codigo: int) -> str:
    """Retorna a descrição de um código de status de envio."""
    return STATUS_ENVIO.get(codigo, f"Código de status desconhecido: {codigo}")
