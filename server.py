from mcp.server.mcpserver import MCPServer

from config import HOST, PORT


mcp = MCPServer(
    "Banco Arkhé MCP",
    instructions=(
        "Servidor oficial de ferramentas do Banco Arkhé. "
        "As ferramentas bancárias serão adicionadas gradualmente e sempre "
        "respeitarão autenticação, conta ativa, cargo e nível de permissão."
    ),
)


@mcp.tool()
def status_arkhe() -> dict[str, str]:
    """Verifica se o serviço MCP do Banco Arkhé está online."""
    return {
        "servico": "Banco Arkhé MCP",
        "status": "online",
        "versao": "0.1.0",
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        stateless_http=True,
        json_response=True,
    )
