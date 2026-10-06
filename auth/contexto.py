from mcp.server.mcpserver import Context


HEADER_SESSAO_ARKHE = "x-arkhe-session"


def obter_sessao_arkhe(ctx: Context) -> str:
    """Obtém o token opaco da sessão Arkhé enviado pelo orquestrador."""
    headers = ctx.headers or {}
    token = headers.get(HEADER_SESSAO_ARKHE)

    if not token:
        raise PermissionError("Sessão Arkhé não autenticada.")

    token = token.strip()

    if not token or len(token) > 4096:
        raise PermissionError("Sessão Arkhé inválida.")

    return token
