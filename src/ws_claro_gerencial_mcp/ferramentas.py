"""Definições das ferramentas (tools) expostas pelo MCP."""

FERRAMENTAS = [
    {
        "name": "listar_entidades",
        "description": (
            "Lista todas as entidades disponíveis no Claro Gerencial, "
            "indicando quais suportam consulta (output) e quais suportam envio (input). "
            "Use esta ferramenta para descobrir quais entidades existem antes de usar as demais."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "obter_registros",
        "description": (
            "Obtém registros de uma entidade do Claro Gerencial (WebService de Output). "
            "Use esta ferramenta para consultar/baixar dados do sistema.\n\n"
            "Parâmetros:\n"
            "- entidade: slug da entidade (ex: 'clientes', 'pedidos', 'visitas'). "
            "Use 'listar_entidades' para ver todas as opções.\n"
            "- completa: True para carga completa (todos os registros), "
            "False para carga incremental (apenas novos/alterados desde a última consulta).\n"
            "- usuario/senha: opcionais, usam as variáveis de ambiente CLARO_USUARIO/CLARO_SENHA por padrão.\n"
            "- ambiente: opcional, 'homologacao' ou 'producao'. Padrão: variável CLARO_AMBIENTE.\n\n"
            "Retorna um ticket que pode ser usado em 'gerar_arquivo' para gerar um arquivo FTP. "
            "Se a quantidade de registros retornados atingir o limite, faça novas chamadas "
            "com completa=False até que o retorno venha vazio."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "entidade": {
                    "type": "string",
                    "description": "Slug da entidade (ex: 'clientes', 'pedidos', 'visitas'). Use 'listar_entidades' para ver todas.",
                },
                "completa": {
                    "type": "boolean",
                    "description": "True para carga completa (SIM), False para incremental (NAO).",
                },
                "usuario": {
                    "type": "string",
                    "description": "Usuário de acesso (opcional — usa env var CLARO_USUARIO se omitido).",
                },
                "senha": {
                    "type": "string",
                    "description": "Senha de acesso (opcional — usa env var CLARO_SENHA se omitido).",
                },
                "ambiente": {
                    "type": "string",
                    "description": "Ambiente: 'homologacao' ou 'producao' (opcional — usa env var CLARO_AMBIENTE).",
                    "enum": ["homologacao", "producao"],
                },
            },
            "required": ["entidade", "completa"],
        },
    },
    {
        "name": "gerar_arquivo",
        "description": (
            "Gera um arquivo FTP com os registros obtidos anteriormente via 'obter_registros'. "
            "Use o ticket retornado por 'obter_registros' para solicitar que o conteúdo seja "
            "disponibilizado via FTP. O arquivo ficará disponível em até 2 horas.\n\n"
            "Parâmetros:\n"
            "- ticket: ticket retornado por 'obter_registros'.\n"
            "- entidade: slug da mesma entidade usada em 'obter_registros'.\n"
            "- usuario/senha/ambiente: opcionais, usam variáveis de ambiente por padrão."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticket": {
                    "type": "string",
                    "description": "Ticket obtido na chamada de 'obter_registros'.",
                },
                "entidade": {
                    "type": "string",
                    "description": "Slug da entidade (a mesma usada em 'obter_registros').",
                },
                "usuario": {
                    "type": "string",
                    "description": "Usuário de acesso (opcional).",
                },
                "senha": {
                    "type": "string",
                    "description": "Senha de acesso (opcional).",
                },
                "ambiente": {
                    "type": "string",
                    "description": "Ambiente: 'homologacao' ou 'producao' (opcional).",
                    "enum": ["homologacao", "producao"],
                },
            },
            "required": ["ticket", "entidade"],
        },
    },
    {
        "name": "enviar_registros",
        "description": (
            "Envia registros em XML para importação no Claro Gerencial (WebService de Input). "
            "Use esta ferramenta para inserir, alterar ou excluir registros no sistema.\n\n"
            "O XML deve seguir o schema XSD da entidade (use 'obter_schema_xml' para validar). "
            "Cada registro no XML deve conter o campo DbAcao: I (Inclusão), A (Alteração), E (Exclusão).\n\n"
            "Parâmetros:\n"
            "- entidade: slug da entidade de destino.\n"
            "- xml: string contendo o XML completo a ser enviado.\n"
            "- usuario/senha/ambiente: opcionais.\n\n"
            "Retorna um ticket para acompanhar o status via 'obter_status'."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "entidade": {
                    "type": "string",
                    "description": "Slug da entidade para envio (ex: 'clientes', 'pedidos').",
                },
                "xml": {
                    "type": "string",
                    "description": "Conteúdo XML completo a ser enviado, conforme schema XSD da entidade.",
                },
                "usuario": {
                    "type": "string",
                    "description": "Usuário de acesso (opcional).",
                },
                "senha": {
                    "type": "string",
                    "description": "Senha de acesso (opcional).",
                },
                "ambiente": {
                    "type": "string",
                    "description": "Ambiente: 'homologacao' ou 'producao' (opcional).",
                    "enum": ["homologacao", "producao"],
                },
            },
            "required": ["entidade", "xml"],
        },
    },
    {
        "name": "obter_status",
        "description": (
            "Consulta o status de um envio de registros pelo ticket (WebService de Input). "
            "Use após 'enviar_registros' para acompanhar o processamento.\n\n"
            "Códigos de status:\n"
            "  0 - Na Fila para importação\n"
            "  1 - Registros sendo transferidos para o SGR\n"
            "  2 - Verificar preenchimento das informações\n"
            "  3 - Verificar se registros de exclusão existem\n"
            "  4 - Verificar registros de inclusão repetidos\n"
            "  5 - Verificar campos de cadastros relacionados\n"
            "  6 - Atualizar log para Inclusão\n"
            "  7 - Atualizar log para Alteração\n"
            "  8 - Atualizar log para Exclusão\n"
            "  9 - Envio Finalizado\n"
            "  99 - Erro ao Enviar\n\n"
            "Quando status=9 (Envio Finalizado), o campo Conteudo traz o log detalhado "
            "com registros importados e eventuais erros."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticket": {
                    "type": "string",
                    "description": "Ticket retornado por 'enviar_registros'.",
                },
                "entidade": {
                    "type": "string",
                    "description": "Slug da entidade enviada.",
                },
                "usuario": {
                    "type": "string",
                    "description": "Usuário de acesso (opcional).",
                },
                "senha": {
                    "type": "string",
                    "description": "Senha de acesso (opcional).",
                },
                "ambiente": {
                    "type": "string",
                    "description": "Ambiente: 'homologacao' ou 'producao' (opcional).",
                    "enum": ["homologacao", "producao"],
                },
            },
            "required": ["ticket", "entidade"],
        },
    },
    {
        "name": "obter_schema_xml",
        "description": (
            "Obtém o schema XSD (XML Schema Definition) de uma entidade para validação "
            "antes do envio (WebService de Input).\n\n"
            "Use esta ferramenta para verificar a estrutura esperada do XML antes de "
            "chamar 'enviar_registros'. O schema define os campos obrigatórios, tipos e "
            "formato esperado para cada entidade.\n\n"
            "Parâmetros:\n"
            "- entidade: slug da entidade.\n"
            "- usuario/senha/ambiente: opcionais."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "entidade": {
                    "type": "string",
                    "description": "Slug da entidade para obter o schema XSD.",
                },
                "usuario": {
                    "type": "string",
                    "description": "Usuário de acesso (opcional).",
                },
                "senha": {
                    "type": "string",
                    "description": "Senha de acesso (opcional).",
                },
                "ambiente": {
                    "type": "string",
                    "description": "Ambiente: 'homologacao' ou 'producao' (opcional).",
                    "enum": ["homologacao", "producao"],
                },
            },
            "required": ["entidade"],
        },
    },
]


def obter_nomes_ferramentas() -> list[str]:
    """Retorna a lista de nomes de ferramentas disponíveis."""
    return [f["name"] for f in FERRAMENTAS]


def obter_ferramenta(nome: str) -> dict | None:
    """Obtém a definição de uma ferramenta pelo nome. Retorna None se não encontrada."""
    for f in FERRAMENTAS:
        if f["name"] == nome:
            return f
    return None
