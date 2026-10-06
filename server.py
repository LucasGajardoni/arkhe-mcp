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
        "versao": "0.3.0",
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
        "tipo_conta": "PJ" if dados.get("tipo_conta") == 1 else "PF",
        "nome": dados.get("nome"),
        "vinculo": dados.get("vinculo"),
        "cargo": dados.get("cargo_nome"),
    }


@mcp.tool()
async def consultar_saldo(ctx: Context) -> dict:
    """Consulta o saldo disponível da conta Arkhé selecionada."""
    sessao = obter_sessao_arkhe(ctx)
    dados = await arkhe_api.consultar_saldo(sessao)

    return {
        "saldo": dados.get("saldo"),
        "moeda": "BRL",
    }


@mcp.tool()
async def consultar_extrato(
    ctx: Context,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    limite: int = 50,
) -> dict:
    """Consulta o extrato da conta. Datas opcionais devem usar YYYY-MM-DD."""
    sessao = obter_sessao_arkhe(ctx)

    return await arkhe_api.consultar_extrato(
        sessao,
        data_inicio=data_inicio,
        data_fim=data_fim,
        limite=limite,
    )


@mcp.tool()
async def consultar_dda(
    ctx: Context,
    limite: int = 50,
) -> dict:
    """Consulta os boletos registrados para pagamento pela conta selecionada."""
    sessao = obter_sessao_arkhe(ctx)
    return await arkhe_api.consultar_dda(sessao, limite=limite)


@mcp.tool()
async def consultar_boletos(
    ctx: Context,
    limite: int = 50,
) -> dict:
    """Consulta boletos a pagar e a receber vinculados à conta selecionada."""
    sessao = obter_sessao_arkhe(ctx)
    return await arkhe_api.consultar_boletos(sessao, limite=limite)


@mcp.tool()
async def consultar_faturas(ctx: Context) -> dict:
    """Consulta faturas fechadas e próximas faturas do cartão da conta."""
    sessao = obter_sessao_arkhe(ctx)
    return await arkhe_api.consultar_faturas(sessao)


@mcp.tool()
async def consultar_limites(ctx: Context) -> dict:
    """Consulta os limites de crédito disponíveis no cartão da conta."""
    sessao = obter_sessao_arkhe(ctx)
    return await arkhe_api.consultar_limites(sessao)


@mcp.tool()
async def listar_chaves_pix(ctx: Context) -> dict:
    """Lista as chaves Pix cadastradas na conta selecionada."""
    sessao = obter_sessao_arkhe(ctx)
    return await arkhe_api.listar_chaves_pix(sessao)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        stateless_http=True,
        json_response=True,
    )
