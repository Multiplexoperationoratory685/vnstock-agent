# CLAUDE.md

## Overview

VNStock Agent - MCP server and CLI for Vietnamese stock market data. Wraps the `vnstock` Python library to provide AI tool integration via Model Context Protocol.

## Architecture

Single Python package with 2 entry points:
- `vnstock-mcp` - FastMCP server (stdio/SSE/HTTP)
- `vnstock-agent` - Click CLI

```
src/vnstock_agent/
├── config.py   # Settings, API key management
├── core.py     # Shared vnstock wrapper (DataFrame→dict)
├── server.py   # FastMCP server with 21 tools
└── cli.py      # Click CLI with 22 commands
```

## Commands

```bash
# Install
pip install -e ".[dev]"

# Run CLI
VNSTOCK_API_KEY=xxx vnstock-agent history VNM

# Run MCP server (stdio)
VNSTOCK_API_KEY=xxx vnstock-mcp

# Run MCP server (SSE/HTTP)
VNSTOCK_MCP_TRANSPORT=sse vnstock-mcp
VNSTOCK_MCP_TRANSPORT=http vnstock-mcp

# Lint
ruff check src/

# Test
pytest
```

## Key Decisions

- FastMCP 3.2.0: uses `instructions` param (not `description`)
- stdout suppression required: vnstock/vnai prints registration messages
- MultiIndex DataFrame handling: price_board returns tuple-keyed columns
- MSN source (fx/crypto/indices) has upstream timezone bug in vnstock
