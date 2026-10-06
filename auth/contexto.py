import secrets

from mcp.server.mcpserver import Context

from config import ARKHE_MCP_CLIENT_KEY


HEADER_CLIENTE_MCP = "x-arkhe-client-key"
HEADER_SESSAO_ARKHE = "x-arkhe-session"


def validar_cliente_mcp(ctx: Context) -> None:
    """Valida a chave fixa do orquestrador autorizado a usar o MCP."""
    if not ARKHE_MCP_CLIENT_KEY:
        raise PermissionError("Cliente MCP não configurado.")

    headers = ctx.headers or {}
    chave = (headers.get(HEADER_CLIENTE_MCP) or "").strip()

    if not chave or not secrets.compare_digest(chave, ARKHE_MCP_CLIENT_KEY):
        raise PermissionError("Cliente MCP não autorizado.")


def obter_sessao_arkhe(ctx: Context) -> str:
    """Obtém e valida o contexto bancário temporário enviado pelo orquestrador."""
    validar_cliente_mcp(ctx)

    headers = ctx.headers or {}
    token = headers.get(HEADER_SESSAO_ARKHE)

    if not token:
        raise PermissionError("Sessão Arkhé não autenticada.")

    token = token.strip()

    if not token or len(token) > 4096:
        raise PermissionError("Sessão Arkhé inválida.")

    return token
