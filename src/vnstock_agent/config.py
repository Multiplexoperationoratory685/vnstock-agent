"""Configuration and settings for VNStock Agent."""

import os

# API key from environment or default
VNSTOCK_API_KEY = os.environ.get("VNSTOCK_API_KEY", "")

# Default data source
DEFAULT_SOURCE = os.environ.get("VNSTOCK_SOURCE", "VCI")

# Server settings
SERVER_HOST = os.environ.get("VNSTOCK_MCP_HOST", "0.0.0.0")
SERVER_PORT = int(os.environ.get("VNSTOCK_MCP_PORT", "8000"))

# Transport mode: stdio, sse, http
TRANSPORT = os.environ.get("VNSTOCK_MCP_TRANSPORT", "stdio")


_api_key_registered = False


def ensure_api_key():
    """Register API key with vnstock if available. Suppresses stdout output."""
    global _api_key_registered
    if _api_key_registered or not VNSTOCK_API_KEY:
        return
    _api_key_registered = True
    try:
        import sys
        import io
        # Suppress vnstock/vnai registration messages from polluting stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            from vnstock import register_user
            register_user(api_key=VNSTOCK_API_KEY)
        finally:
            sys.stdout = old_stdout
    except Exception:
        pass
