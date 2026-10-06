from mcp.server.mcpserver import Context, MCPServer

from auth.contexto import obter_sessao_arkhe
from clients.arkhe_api import ArkheAPI
from config import HOST, PORT


mcp = MCPServer(
    "Banco Arkhé MCP",
    instructions=(
        "Servidor oficial de ferramentas do Banco Arkhé. "
        "As ferramentas bancárias respeitam a sessão autenticada, "
        "a conta ativa e as permissões definidas pelo banco."
    ),
)

arkhe_api = ArkheAPI()


@mcp.tool()
def status_arkhe() -> dict[str, str]:
    """Verifica se o serviço MCP do Banco Arkhé está online."""
    return {
        "servico": "Banco Arkhé MCP",
        "status": "online",
        "versao": "0.2.0",
    }


@mcp.tool()
async def consultar_dados_conta(ctx: Context) -> dict:
    """Consulta os dados da conta Arkhé selecionada na sessão autenticada."""
    sessao = obter_sessao_arkhe(ctx)
    dados = await arkhe_api.consultar_conta(sessao)

    return {
        "numero_conta": dados.get("numero_conta"),
        "agencia": dados.get("agencia"),
        "banco": dados.get("banco"),
        "tipo_conta": dados.get("tipo_conta"),
        "nome": dados.get("nome"),
        "vinculo": dados.get("vinculo"),
        "cargo": dados.get("cargo"),
    }


@mcp.tool()
async def consultar_saldo(ctx: Context) -> dict:
    """Consulta o saldo disponível da conta Arkhé selecionada na sessão autenticada."""
    sessao = obter_sessao_arkhe(ctx)
    dados = await arkhe_api.consultar_saldo(sessao)

    return {
        "saldo": dados.get("saldo"),
        "moeda": "BRL",
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        stateless_http=True,
        json_response=True,
    )
