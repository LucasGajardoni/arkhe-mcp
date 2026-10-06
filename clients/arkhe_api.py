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

    async def _get(
        self,
        caminho: str,
        sessao_arkhe: str,
        params: dict | None = None,
    ) -> dict:
        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            ) as client:
                resposta = await client.get(
                    caminho,
                    headers=self._headers(sessao_arkhe),
                    params=params,
                )
        except httpx.RequestError as e:
            raise ArkheAPIError("Backend do Banco Arkhé indisponível.") from e

        if resposta.status_code in (401, 403):
            raise PermissionError(
                "Sessão Arkhé inválida, expirada ou sem permissão."
            )

        if not resposta.is_success:
            raise ArkheAPIError("Não foi possível consultar o Banco Arkhé.")

        try:
            return resposta.json()
        except ValueError as e:
            raise ArkheAPIError(
                "Resposta inválida recebida do Banco Arkhé."
            ) from e

    async def consultar_conta(self, sessao_arkhe: str) -> dict:
        return await self._get("/internal/mcp/conta", sessao_arkhe)

    async def consultar_saldo(self, sessao_arkhe: str) -> dict:
        return await self._get("/internal/mcp/saldo", sessao_arkhe)

    async def consultar_extrato(
        self,
        sessao_arkhe: str,
        data_inicio: str | None = None,
        data_fim: str | None = None,
        limite: int = 50,
    ) -> dict:
        params = {"limite": limite}

        if data_inicio:
            params["data_inicio"] = data_inicio

        if data_fim:
            params["data_fim"] = data_fim

        return await self._get(
            "/internal/mcp/extrato",
            sessao_arkhe,
            params=params,
        )

    async def consultar_dda(
        self,
        sessao_arkhe: str,
        limite: int = 50,
    ) -> dict:
        return await self._get(
            "/internal/mcp/dda",
            sessao_arkhe,
            params={"limite": limite},
        )

    async def consultar_boletos(
        self,
        sessao_arkhe: str,
        limite: int = 50,
    ) -> dict:
        return await self._get(
            "/internal/mcp/boletos",
            sessao_arkhe,
            params={"limite": limite},
        )

    async def consultar_faturas(self, sessao_arkhe: str) -> dict:
        return await self._get("/internal/mcp/faturas", sessao_arkhe)

    async def consultar_limites(self, sessao_arkhe: str) -> dict:
        return await self._get("/internal/mcp/limites", sessao_arkhe)

    async def listar_chaves_pix(self, sessao_arkhe: str) -> dict:
        return await self._get("/internal/mcp/chaves-pix", sessao_arkhe)


    async def listar_funcionarios(self, sessao_arkhe: str) -> dict:
        return await self._get("/internal/mcp/funcionarios", sessao_arkhe)

    async def consultar_funcionario(
        self,
        sessao_arkhe: str,
        id_funcionario: int,
    ) -> dict:
        return await self._get(
            f"/internal/mcp/funcionarios/{id_funcionario}",
            sessao_arkhe,
        )

    async def listar_folhas(
        self,
        sessao_arkhe: str,
        limite: int = 12,
    ) -> dict:
        return await self._get(
            "/internal/mcp/folhas",
            sessao_arkhe,
            params={"limite": limite},
        )

    async def consultar_folha(
        self,
        sessao_arkhe: str,
        id_folha: int,
    ) -> dict:
        return await self._get(
            f"/internal/mcp/folhas/{id_folha}",
            sessao_arkhe,
        )


    async def gerar_relatorio_funcionarios(self, sessao_arkhe: str) -> dict:
        dados = await self._get(
            "/internal/mcp/relatorios/funcionarios",
            sessao_arkhe,
        )

        download_path = dados.get("download_path")

        if download_path:
            dados["download_url"] = self.base_url + download_path

        dados.pop("download_path", None)
        return dados
