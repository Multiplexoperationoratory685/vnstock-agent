# VNStock Agent - MCP + CLI Monorepo

**Status:** In Progress | **Created:** 2026-04-01

## Architecture

Single Python package with 2 entry points (MCP server + CLI), sharing core vnstock wrapper.

```
vnstock-agent/
├── pyproject.toml          # Package config, dependencies, entry points
├── src/vnstock_agent/
│   ├── __init__.py
│   ├── config.py           # Settings, API key management
│   ├── core.py             # Shared vnstock wrapper (DataFrame→dict conversion)
│   ├── server.py           # FastMCP server (stdio/SSE/HTTP)
│   └── cli.py              # Click CLI
├── tests/
│   ├── test_core.py
│   └── test_cli.py
└── docs/
```

## Tech Stack

- **MCP Server:** FastMCP 3.0 (stdio + SSE + Streamable HTTP)
- **CLI:** Click
- **Core:** vnstock 3.5.0 + pandas
- **Config:** pydantic-settings (env vars)

## MCP Tools (21 tools)

| Category | Tool | Description |
|----------|------|-------------|
| Quote | `stock_history` | Historical OHLCV data |
| Quote | `stock_intraday` | Intraday trading data |
| Quote | `stock_price_depth` | Order book data |
| Company | `company_overview` | Company overview |
| Company | `company_shareholders` | Major shareholders |
| Company | `company_officers` | Company officers |
| Company | `company_news` | Company news |
| Company | `company_events` | Company events |
| Finance | `financial_balance_sheet` | Balance sheet |
| Finance | `financial_income_statement` | Income statement |
| Finance | `financial_cash_flow` | Cash flow |
| Finance | `financial_ratio` | Financial ratios |
| Listing | `listing_all_symbols` | All stock symbols |
| Listing | `listing_symbols_by_group` | VN30, HNX30, etc. |
| Listing | `listing_symbols_by_exchange` | By exchange |
| Listing | `listing_industries` | ICB industries |
| Trading | `trading_price_board` | Price board |
| Global | `fx_history` | Forex history |
| Global | `crypto_history` | Crypto history |
| Global | `world_index_history` | World index history |
| Fund | `fund_listing` | Mutual fund listing |

## Phases

- [x] Phase 1: Research (complete)
- [ ] Phase 2: Project scaffold + dependencies
- [ ] Phase 3: Core wrapper implementation
- [ ] Phase 4: MCP server implementation
- [ ] Phase 5: CLI implementation
- [ ] Phase 6: Testing & verification
- [ ] Phase 7: Documentation + GitHub repo
