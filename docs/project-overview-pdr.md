# VNStock Agent - Project Overview & Product Development Requirements

## Project Overview

**VNStock Agent** is a Python package that bridges the Vietnamese stock market data via the `vnstock` library with AI tools through the Model Context Protocol (MCP). It provides both an MCP server for AI assistants and a command-line interface for direct terminal access.

### Vision
Enable AI tools (Claude, GPT, etc.) and developers to seamlessly access Vietnamese financial market data—stocks, forex, crypto, indices, and mutual funds—with programmatic ease and intelligence.

### Core Value Propositions
- **AI-Ready**: 21 MCP tools integrated with Claude Desktop, Cursor, and other MCP clients
- **Developer-Friendly**: CLI with table and JSON output formats for terminal workflows
- **Comprehensive**: Vietnamese stocks, company fundamentals, financials, forex, crypto, world indices, and mutual funds
- **Flexible**: Multiple transport modes (stdio, SSE, HTTP)
- **Lightweight**: Single Python package with minimal dependencies

## Target Users

| User Type | Use Case | Entry Point |
|-----------|----------|-------------|
| AI Tool Developers | Build AI agents for financial analysis | MCP server (stdio, SSE, HTTP) |
| Data Analysts | Quick data exploration via terminal | CLI with table/JSON output |
| Traders | Real-time stock quotes and market tracking | MCP tools in AI assistants |
| Financial Researchers | Company fundamentals and historical data | MCP tools or CLI |
| AI Assistants | Answer financial questions about Vietnamese markets | MCP tools |

## Feature Matrix (v0.1.0)

### MCP Tools (21 tools across 6 categories)

| Category | Tools | Supported |
|----------|-------|-----------|
| **Quotes** | stock_history, stock_intraday, stock_price_depth | ✓ |
| **Company** | overview, shareholders, officers, news, events | ✓ |
| **Financials** | balance_sheet, income_statement, cash_flow, ratio | ✓ |
| **Listings** | all_symbols, symbols_by_group, symbols_by_exchange, industries | ✓ |
| **Trading** | price_board | ✓ |
| **Global Markets** | fx_history, crypto_history, world_index_history, fund_listing | ⚠ Known upstream bugs |

### CLI Commands (22 commands)
All 21 MCP tools available via CLI. Additional `serve` command to start MCP server with custom transport.

### Transports
- **stdio**: For Claude Desktop, Cursor, and local integrations
- **SSE**: HTTP streaming for long-lived connections
- **Streamable HTTP**: Traditional POST-based requests

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Core Data | vnstock | 3.5.0 |
| MCP Framework | FastMCP | ≥2.0.0 |
| CLI Framework | Click | ≥8.0 |
| HTTP Server | uvicorn | ≥0.20.0 |
| Data Processing | pandas | ≥1.5.0 |
| Table Formatting | tabulate | ≥0.9.0 |
| Config Management | pydantic-settings | ≥2.0 |
| Python | 3.10+ | - |

## Functional Requirements

### FR-1: MCP Server
- Provide 21 distinct MCP tools for Vietnamese stock market data
- Support stdio, SSE, and Streamable HTTP transports
- Handle API key registration and management
- Return JSON-serializable data for all tools
- Graceful error handling with error messages in JSON format

### FR-2: CLI Interface
- Expose all 21 tools as CLI commands
- Support both table and JSON output formats
- Allow date range specifications with smart defaults (30-day lookback)
- Support multiple data sources (VCI, KBS)
- Handle symbol case normalization

### FR-3: Data Transformation
- Convert pandas DataFrames to JSON-serializable dicts
- Handle MultiIndex columns, missing values, and timestamps
- Support both single and batch data requests
- Maintain data integrity and precision

### FR-4: Configuration Management
- Load settings from environment variables
- Support custom API keys for vnstock
- Allow source selection (VCI, KBS)
- Configurable server host/port

## Non-Functional Requirements

### NFR-1: Reliability
- Gracefully handle vnstock API failures
- Return error objects instead of crashing
- Support retry logic for transient failures
- Suppress noisy vnstock logging

### NFR-2: Performance
- Respond to data requests within 5 seconds (network dependent)
- Support pagination for large datasets
- Efficient DataFrame-to-JSON conversion
- Minimal memory footprint for CLI invocations

### NFR-3: Compatibility
- Python 3.10+ support
- Cross-platform (Linux, macOS, Windows)
- Works with Claude Desktop, Cursor, and other MCP clients
- Compatible with vnstock ≥3.5.0

### NFR-4: Maintainability
- Clean separation of concerns (config, core, server, CLI)
- Clear error messages for debugging
- Comprehensive docstrings for all functions
- Type hints for better IDE support

## Known Limitations & Workarounds

| Issue | Impact | Workaround |
|-------|--------|-----------|
| vnstock MSN source timezone bug | forex, crypto, world_index return shifted dates | Use VCI source where possible |
| price_depth() unsupported by VCI/KBS | stock_price_depth returns error | Document limitation for users |
| vnstock prints to stdout on API key registration | Pollutes MCP stdio transport | Suppress stdout during registration |
| Limited to 30-day default for history | Users may expect more historical data | Allow custom start dates |

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| MCP tools passing tests | 17/21 (80%) | ✓ |
| CLI commands available | 22/22 | ✓ |
| Transport support | 3/3 (stdio, SSE, HTTP) | ✓ |
| Python version support | 3.10-3.13 | ✓ |
| Package size | <5MB | ✓ |
| Installation time | <30 seconds | ✓ |

## Version Timeline

### v0.1.0 (Current - April 2026)
- Initial public release
- 21 MCP tools across 6 categories
- 22 CLI commands
- 3 transport modes
- Basic documentation

### v0.2.0 (Planned)
- Enhanced error handling and logging
- Caching layer for frequently accessed data
- Support for custom time zones
- Integration tests with real vnstock API
- Advanced filtering and aggregation tools

### v0.3.0+ (Roadmap)
- Portfolio tracking and analysis tools
- Technical analysis indicators
- Historical performance comparison
- Integration with trading platforms
- Mobile-friendly CLI output

## Dependencies & Constraints

### Direct Dependencies
- vnstock ≥3.5.0 (Vietnamese stock market data)
- fastmcp ≥2.0.0 (MCP protocol implementation)
- click ≥8.0 (CLI framework)
- pandas ≥1.5.0 (data processing)
- pydantic-settings ≥2.0 (config management)

### External Constraints
- Requires active vnstock API key for some operations
- Depends on vnstock library's data sources (VCI, KBS, MSN)
- Network connectivity required for all data operations
- Data freshness depends on upstream vnstock updates

### Development Dependencies
- pytest ≥7.0 (unit testing)
- pytest-asyncio ≥0.21 (async test support)
- ruff ≥0.1.0 (linting)

## Acceptance Criteria

- [ ] All 21 MCP tools implemented and tested
- [ ] CLI with all 22 commands and dual output format
- [ ] Support for all 3 transport modes (stdio, SSE, HTTP)
- [ ] Configuration via environment variables
- [ ] Graceful error handling and informative messages
- [ ] Comprehensive documentation and examples
- [ ] Passing unit tests (17/21 tools verified)
- [ ] Clean code meeting ruff linting standards
- [ ] Backward compatible with Python 3.10+

## Exit Criteria for v0.1.0

- [ ] 80%+ test coverage for core functions
- [ ] All MCP tools callable and return valid JSON
- [ ] CLI commands work with sample data
- [ ] Zero critical security vulnerabilities
- [ ] README contains setup, usage, and MCP configuration
- [ ] MIT license included
