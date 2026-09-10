# ws-claro-gerencial-mcp

[![PyPI version](https://img.shields.io/pypi/v/ws-claro-gerencial-mcp.svg)](https://pypi.org/project/ws-claro-gerencial-mcp/)
[![License: MIT](https://img.shields.io/github/license/hlgurgel/ws-claro-gerencial-mcp.svg)](https://github.com/hlgurgel/ws-claro-gerencial-mcp/blob/main/LICENSE)
[![Python versions](https://img.shields.io/pypi/pyversions/ws-claro-gerencial-mcp.svg)](https://pypi.org/project/ws-claro-gerencial-mcp/)

<!-- mcp-name: io.github.hlgurgel/ws-claro-gerencial -->

Servidor MCP (Model Context Protocol) para integração com os **WebServices SOAP** do **Claro Gerencial** (plataforma da Claro gerenciada pela Redeinova Tecnologia).

Este servidor permite que agentes de IA (como o opencode, Claude Code, etc.) interajam diretamente com o Claro Gerencial, realizando consultas e envios de dados de forma autônoma.

## Funcionalidades

O servidor expõe **6 ferramentas** via MCP:

- **listar_entidades** — Lista todas as entidades disponíveis e suas direções (input/output)
- **obter_registros** — Consulta registros de qualquer entidade (completa ou incremental)
- **gerar_arquivo** — Solicita geração de arquivo FTP a partir de um ticket de consulta
- **enviar_registros** — Envia XML para importação de registros
- **obter_status** — Consulta status de processamento de um envio
- **obter_schema_xml** — Obtém schema XSD para validação antes do envio

## Entidades disponíveis

- Cidades, Bairros, Clientes (PDVs), ClientesVisitas, Empresas, Gerentes, Supervisores
- Vendedores, Setores, Grupos de Produtos, MotivosVisitas, Produtos, Segmentos
- TiposClientes, TiposSinalizações, ClientesSinalizações, Visitas
- Integradores, Pedidos, ChipsVendedor, MotivosICCIDS, ICCID, RedesPDV
- VendasBandaLarga, ReleiturasICCID

## Instalação

```bash
pip install ws-claro-gerencial-mcp
```

Ou, sem instalar nada (executa direto do PyPI com cache):

```bash
uvx --from ws-claro-gerencial-mcp ws-claro-gerencial-mcp
```

Ou para desenvolvimento:

```bash
git clone https://github.com/hlgurgel/ws-claro-gerencial-mcp.git
cd ws-claro-gerencial-mcp
pip install -e .
```

## Configuração

Crie um arquivo `.env` na raiz do projeto ou defina as variáveis de ambiente:

```env
CLARO_USUARIO=seu_usuario
CLARO_SENHA=sua_senha
CLARO_AMBIENTE=homologacao
```

### Variáveis de ambiente

| Variável | Obrigatória | Padrão | Descrição |
|----------|:-----------:|--------|-----------|
| `CLARO_USUARIO` | Sim | — | Usuário de acesso ao webservice |
| `CLARO_SENHA` | Sim | — | Senha de acesso ao webservice |
| `CLARO_AMBIENTE` | Não | `homologacao` | Ambiente: `homologacao` ou `producao` |
| `CLARO_URL_BASE_OUTPUT` | Não | `https://clarogerencial.redeinova.com.br/wsoutput` | URL base do WS de Output |
| `CLARO_URL_BASE_INPUT` | Não | `https://clarogerencial.redeinova.com.br/wsinput` | URL base do WS de Input |

## Uso com clientes MCP

### Claude Desktop

Adicione ao `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "claro-gerencial": {
      "command": "uvx",
      "args": ["--from", "ws-claro-gerencial-mcp", "ws-claro-gerencial-mcp"],
      "env": {
        "CLARO_USUARIO": "seu_usuario",
        "CLARO_SENHA": "sua_senha",
        "CLARO_AMBIENTE": "homologacao"
      }
    }
  }
}
```

### OpenCode

Adicione ao `opencode.json` do seu projeto:

```json
{
  "mcp": {
    "claro-gerencial": {
      "type": "local",
      "command": ["ws-claro-gerencial-mcp"],
      "environment": {
        "CLARO_USUARIO": "seu_usuario",
        "CLARO_SENHA": "sua_senha",
        "CLARO_AMBIENTE": "homologacao"
      }
    }
  }
}
```

### Exemplos de uso

```
> Liste as entidades disponíveis no Claro Gerencial.

> Consulte os clientes ativos (entidade: 'clientes') de forma completa.

> Envie um novo cliente:
<Clientes>
  <Cliente>
    <Empresa>1</Empresa>
    <Sequencial>999</Sequencial>
    <Nome>NOVO PDV</Nome>
    <DbAcao>I</DbAcao>
  </Cliente>
</Clientes>
```

## Requisitos de segurança

- **IP fixo**: O distribuidor precisa ter um IP fixo cadastrado na Redeinova.
- **SSL**: Toda comunicação usa HTTPS com TLS.
- **Autenticação**: Usuário e senha fornecidos pela Redeinova, senhas fortes com mínimo de 8 caracteres.

## Autorização por IP (output/baixa)

Para consultas/baixas (output) — e também envios (input) — o WebService exige que o **IP de origem** da máquina esteja autorizado na tabela `RepositorioControleIntClaro.dbo.DistribuidorIP` (coluna `Ip`), associado ao usuário do distribuidor (ex.: `CLAROREDEFLEXWS`) com `Ativo = 1`. Sem isso, o WS responde `Usuário não autorizado para efetuar baixa`.

Dicas para validação:

- Em VPN (ex.: redeinova-dc), o IP de origem é o da interface de túnel (`utun*`). Descobrir com: `ifconfig | grep "inet "`.
- O domínio do WS (`clarogerencial.redeinova.com.br`) resolve para IP interno (`10.177.51.41`), então o tráfego sai pela VPN. O IP a cadastrar é o da interface VPN — **não** o IP público retornado por `curl ifconfig.me`.
- Para liberar/ajustar: `INSERT`/`UPDATE` em `RepositorioControleIntClaro.dbo.DistribuidorIP`.

## Ambiente de homologação

Para solicitar ambiente de homologação, entre em contato com:

- **Redeinova Tecnologia**: [suporte@redeinova.net](mailto:suporte@redeinova.net)
- **Telefone**: +55 (85) 3032-5648 / 3252-3405

## Licença

MIT
