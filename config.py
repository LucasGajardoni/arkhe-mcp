import os


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

ARKHE_API_URL = os.getenv("ARKHE_API_URL", "http://localhost:5000").rstrip("/")
ARKHE_API_TIMEOUT = float(os.getenv("ARKHE_API_TIMEOUT", "15"))
ARKHE_MCP_SERVICE_KEY = os.getenv("ARKHE_MCP_SERVICE_KEY")
ARKHE_MCP_CLIENT_KEY = os.getenv("ARKHE_MCP_CLIENT_KEY")
