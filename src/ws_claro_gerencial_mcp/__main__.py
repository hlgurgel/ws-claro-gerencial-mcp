"""Ponto de entrada do servidor MCP — ws-claro-gerencial-mcp."""

import asyncio

from .server import executar


def main():
    """Inicia o servidor MCP do Claro Gerencial."""
    asyncio.run(executar())


if __name__ == "__main__":
    main()
