import httpx

from config import ARKHE_API_TIMEOUT, ARKHE_API_URL, ARKHE_MCP_SERVICE_KEY


class ArkheAPIError(RuntimeError):
    pass


class ArkheAPI:
    def __init__(self):
        self.base_url = ARKHE_API_URL
        self.timeout = ARKHE_API_TIMEOUT

    def _headers(self, sessao_arkhe: str) -> dict[str, str]:
        if not ARKHE_MCP_SERVICE_KEY:
            raise ArkheAPIError("Credencial interna do MCP não configurada.")

        return {
            "X-Arkhe-MCP-Key": ARKHE_MCP_SERVICE_KEY,
            "X-Arkhe-Session": sessao_arkhe,
        }

    async def _get(self, caminho: str, sessao_arkhe: str) -> dict:
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
                resposta = await client.get(caminho, headers=self._headers(sessao_arkhe))
        except httpx.RequestError as e:
            raise ArkheAPIError("Backend do Banco Arkhé indisponível.") from e

        if resposta.status_code in (401, 403):
            raise PermissionError("Sessão Arkhé inválida, expirada ou sem permissão.")

        if not resposta.is_success:
            raise ArkheAPIError("Não foi possível consultar o Banco Arkhé.")

        try:
            return resposta.json()
        except ValueError as e:
            raise ArkheAPIError("Resposta inválida recebida do Banco Arkhé.") from e

    async def consultar_conta(self, sessao_arkhe: str) -> dict:
        return await self._get("/internal/mcp/conta", sessao_arkhe)

    async def consultar_saldo(self, sessao_arkhe: str) -> dict:
        return await self._get("/internal/mcp/saldo", sessao_arkhe)
