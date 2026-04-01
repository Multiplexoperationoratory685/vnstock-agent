# VNStock Agent - Codebase Summary

## Directory Structure

```
vnstock-agent/
├── src/vnstock_agent/
│   ├── __init__.py           # Package metadata (v0.1.0)
│   ├── config.py             # Settings and environment configuration
│   ├── core.py               # Shared vnstock wrapper and data conversion
│   ├── server.py             # FastMCP server with 21 MCP tools
│   └── cli.py                # Click CLI with 22 commands
├── tests/
│   ├── test_core.py          # Unit tests for core functions
│   └── test_cli.py           # Integration tests for CLI
├── pyproject.toml            # Package configuration, dependencies, entry points
├── README.md                 # User-facing documentation
└── docs/                     # Internal documentation (this folder)
```

## File Manifest

### `src/vnstock_agent/__init__.py` (3 LOC)
**Purpose**: Package initialization and version declaration.

**Contents**:
```python
__version__ = "0.1.0"
```

**Key Functions**: None (metadata only)

---

### `src/vnstock_agent/config.py` (40 LOC)
**Purpose**: Centralized configuration management via environment variables.

**Configuration Variables**:
| Variable | Env Name | Default | Purpose |
|----------|----------|---------|---------|
| VNSTOCK_API_KEY | VNSTOCK_API_KEY | "" | API key for vnstock registration |
| DEFAULT_SOURCE | VNSTOCK_SOURCE | "VCI" | Default data source (VCI, KBS) |
| SERVER_HOST | VNSTOCK_MCP_HOST | "0.0.0.0" | MCP server bind address |
| SERVER_PORT | VNSTOCK_MCP_PORT | 8000 | MCP server listen port |
| TRANSPORT | VNSTOCK_MCP_TRANSPORT | "stdio" | MCP transport mode (stdio, sse, http) |

**Key Functions**:
- `ensure_api_key()`: Registers API key with vnstock if provided. Suppresses stdout to prevent MCP protocol pollution.

**Dependencies**: Built-in modules only (os, sys, io)

---

### `src/vnstock_agent/core.py` (326 LOC)
**Purpose**: Shared wrapper around vnstock library, handles data transformation and API consistency.

**Data Conversion Pipeline**:
1. Call vnstock function → returns DataFrame, Series, dict, or tuple
2. `_df_to_records()` converts to list of dicts
3. Handle MultiIndex columns (flatten to underscore-separated names)
4. Convert NaN → None, Timestamps → ISO strings
5. Return JSON-serializable list of dicts

**Key Internal Functions**:
- `_df_to_records(df)`: Convert DataFrame/Series/dict/tuple to JSON-serializable list of dicts
- `_default_dates(start, end)`: Default to 30-day lookback if dates not provided
- `_safe_call(fn, *args, **kwargs)`: Wrap vnstock calls with error handling
- `_get_stock(symbol, source)`: Initialize Vnstock object for a symbol
- `_suppress_stdout(fn, *args, **kwargs)`: Suppress stdout during function calls

**Quote Tools** (Historical data and intraday):
- `stock_history(symbol, start, end, interval, source)`: OHLCV data
- `stock_intraday(symbol, page_size, source)`: Today's trading data
- `stock_price_depth(symbol, source)`: Order book data (⚠ unsupported by current sources)

**Company Tools** (Fundamental information):
- `company_overview(symbol, source)`: Company overview
- `company_shareholders(symbol, source)`: Major shareholders list
- `company_officers(symbol, source)`: Management team
- `company_news(symbol, source)`: Latest company news
- `company_events(symbol, source)`: Dividends, AGM, earnings events

**Financial Tools** (Accounting statements):
- `financial_balance_sheet(symbol, period, source)`: Balance sheet (quarter/annual)
- `financial_income_statement(symbol, period, source)`: Income statement
- `financial_cash_flow(symbol, period, source)`: Cash flow statement
- `financial_ratio(symbol, period, source)`: Financial ratios (P/E, P/B, ROE, etc.)

**Listing Tools** (Market data and securities):
- `listing_all_symbols(source)`: All listed Vietnamese stocks
- `listing_symbols_by_group(group, source)`: Group symbols (VN30, HNX30, HOSE, etc.)
- `listing_symbols_by_exchange(source)`: Symbols by exchange
- `listing_industries(source)`: ICB industry classification

**Trading Tools**:
- `trading_price_board(symbols, source)`: Real-time price board for multiple symbols

**Global Market Tools** (⚠ Known upstream timezone bugs):
- `fx_history(symbol, start, end, interval)`: Forex data
- `crypto_history(symbol, start, end, interval)`: Cryptocurrency data
- `world_index_history(symbol, start, end, interval)`: World market indices

**Fund Tools**:
- `fund_listing()`: Open-ended mutual fund listing

**Error Handling**: All functions use `_safe_call()` to catch exceptions and return `[{"error": str(e)}]` instead of crashing.

**Dependencies**:
- vnstock (market data provider)
- pandas (DataFrame manipulation, type checking)
- datetime (default date calculations)
- logging (suppress verbose vnstock logging)

---

### `src/vnstock_agent/server.py` (363 LOC)
**Purpose**: FastMCP server exposing all 21 tools via MCP protocol. Supports stdio, SSE, and HTTP transports.

**FastMCP Server Configuration**:
```python
mcp = FastMCP(
    "vnstock-agent",
    instructions="Vietnamese stock market data - historical prices, financials, company info, and more"
)
```

**MCP Tools** (21 total):
Each tool wraps a core.py function and returns JSON string. All follow same pattern:
```python
@mcp.tool()
def tool_name(param1: str, param2: Optional[str] = None) -> str:
    """Docstring describing tool."""
    data = core.function_name(param1, param2)
    return json.dumps(data, ensure_ascii=False, default=str)
```

**Tool Categories**:
| Category | Tools | Count |
|----------|-------|-------|
| Quotes | stock_history, stock_intraday, stock_price_depth | 3 |
| Company | company_overview, shareholders, officers, news, events | 5 |
| Financials | balance_sheet, income_statement, cash_flow, ratio | 4 |
| Listings | all_symbols, symbols_by_group, symbols_by_exchange, industries | 4 |
| Trading | price_board | 1 |
| Global Markets | fx_history, crypto_history, world_index_history | 3 |
| Funds | fund_listing | 1 |
| **Total** | | 21 |

**Transport Support**:
- **stdio** (default): For Claude Desktop, Cursor, local use
- **SSE**: HTTP streaming via FastAPI (if TRANSPORT=sse)
- **Streamable HTTP**: POST requests via FastAPI (if TRANSPORT=http)

**Transport Configuration**:
```python
TRANSPORT = os.getenv('VNSTOCK_MCP_TRANSPORT', 'stdio')
SERVER_HOST = os.getenv('VNSTOCK_MCP_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('VNSTOCK_MCP_PORT', '8000'))
```

**Server Entry Point**:
```python
def run():
    if TRANSPORT == "stdio":
        mcp.run()  # Default async stdio
    elif TRANSPORT == "sse":
        # FastAPI SSE implementation
    elif TRANSPORT == "http":
        # FastAPI HTTP implementation
    else:
        mcp.run()
```

**Key Implementation Details**:
- All parameters have type hints for better IDE support
- Docstrings describe purpose, parameters, and examples
- Vietnamese characters handled via `ensure_ascii=False` in JSON serialization
- Default values match CLI defaults (e.g., source="VCI")

**Dependencies**:
- fastmcp (MCP framework)
- vnstock_agent.core (data functions)
- vnstock_agent.config (settings)
- json (serialization)
- sys (stdio handling)

---

### `src/vnstock_agent/cli.py` (299 LOC)
**Purpose**: Click-based command-line interface with 22 commands for direct terminal access.

**CLI Structure**:
```python
@click.group()
@click.version_option(package_name="vnstock-agent")
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def main(ctx, output_format):
    """VNStock Agent CLI - Vietnamese stock market data at your fingertips."""
```

**Output Formatting**:
- `--format table` (default): Pretty-printed via tabulate
- `--format json`: Pretty-printed JSON with 2-space indentation

**Command Groups** (22 commands total):

| Group | Commands | Count |
|-------|----------|-------|
| Quotes | history, intraday, depth | 3 |
| Company | overview, shareholders, officers, news, events | 5 |
| Financials | balance-sheet, income, cashflow, ratio | 4 |
| Listings | symbols, group, exchange, industries | 4 |
| Trading | board (price board) | 1 |
| Global Markets | fx, crypto, index | 3 |
| Funds | funds | 1 |
| Server | serve | 1 |
| **Total** | | 22 |

**Sample Commands**:
```bash
vnstock-agent history VNM --start 2025-01-01 --end 2025-03-31
vnstock-agent overview FPT
vnstock-agent balance-sheet VCB --period quarter
vnstock-agent symbols  # All listed symbols
vnstock-agent group --group VN30  # VN30 stocks
vnstock-agent board "VNM,FPT,ACB"  # Price board for multiple symbols
vnstock-agent --format json history VNM  # JSON output
vnstock-agent fx EURUSD
vnstock-agent crypto BTC
vnstock-agent index DJI
```

**Symbol Case Normalization**:
```python
symbol.upper()  # All symbols converted to uppercase
```

**Date Defaults**:
- If no start/end specified, defaults to last 30 days
- Format: YYYY-MM-DD

**Key Implementation**:
- `_output(data, output_format)`: Helper for formatting and printing results
- Try/except for ImportError on tabulate (fallback to JSON if not installed)
- All commands use `core.*` functions with consistent parameter naming

**Dependencies**:
- click (CLI framework)
- vnstock_agent.core (data functions)
- vnstock_agent.config (default source)
- json (JSON output)
- tabulate (table formatting, optional)

---

## Data Flow

### Query Path (CLI)
```
CLI Command
  → parse arguments (symbol, dates, options)
  → call core.function_name()
    → ensure_api_key() [if needed]
    → initialize Vnstock object
    → call vnstock.method()
    → convert result via _df_to_records()
    → return list[dict]
  → format output (table or JSON)
  → print to stdout
```

### Query Path (MCP Server)
```
MCP Client (Claude Desktop, Cursor, etc.)
  → call MCP tool
  → server.py tool handler
    → call core.function_name()
    → [same as CLI path above]
    → json.dumps() to JSON string
    → return JSON string to client
```

### Data Transformation Pipeline
```
vnstock API Result
  ↓
DataFrame | Series | dict | tuple
  ↓
_df_to_records() convertion
  ↓
- Flatten MultiIndex columns
- NaN → None
- Timestamp → ISO string
- Handle nested structures
  ↓
list[dict] (JSON-serializable)
  ↓
CLI: tabulate → pretty table
MCP: json.dumps() → JSON string
```

## Dependency Graph

```
pyproject.toml
  ├── vnstock >= 3.5.0 (Vietnamese market data)
  ├── fastmcp >= 2.0.0 (MCP framework)
  ├── click >= 8.0 (CLI)
  ├── pandas >= 1.5.0 (DataFrame)
  ├── pydantic-settings >= 2.0 (config)
  ├── tabulate >= 0.9.0 (table formatting)
  └── uvicorn >= 0.20.0 (HTTP server, optional)

src/vnstock_agent/
  ├── __init__.py
  │   └── (metadata only)
  ├── config.py
  │   ├── stdlib: os
  │   └── (no external deps)
  ├── core.py
  │   ├── vnstock
  │   ├── pandas
  │   └── stdlib: datetime, logging
  ├── server.py
  │   ├── fastmcp
  │   ├── vnstock_agent.core
  │   ├── vnstock_agent.config
  │   └── stdlib: json, sys
  └── cli.py
      ├── click
      ├── vnstock_agent.core
      ├── vnstock_agent.config
      ├── tabulate (optional)
      └── stdlib: json, sys
```

## Key Design Patterns

### 1. Shared Core Model
Single `core.py` module provides all business logic. Both `server.py` and `cli.py` import and call core functions. Eliminates duplication, simplifies maintenance.

### 2. Graceful Error Handling
All vnstock calls wrapped in `_safe_call()`. Returns `[{"error": str(e)}]` instead of raising exceptions. Prevents MCP protocol crashes.

### 3. Data Normalization
`_df_to_records()` handles arbitrary pandas output (DataFrame, Series, dict, tuple). Converts to consistent JSON-serializable format. Handles edge cases (NaN, MultiIndex, timestamps).

### 4. Configuration Isolation
All environment variable lookups centralized in `config.py`. Makes testing and configuration management simple. Supports both programmatic defaults and user overrides.

### 5. Transport Abstraction
FastMCP handles transport differences internally. Server code unchanged whether running stdio, SSE, or HTTP. Configuration via environment variable.

## Known Limitations

| Limitation | Root Cause | Impact | Workaround |
|-----------|-----------|--------|-----------|
| price_depth unsupported by VCI/KBS | Upstream limitation | stock_price_depth returns error | Use as expected graceful error |
| MSN forex/crypto/index timezone bugs | vnstock library bug | Shifted timestamps on global markets | Wait for vnstock fix or use VCI |
| stdout capture overhead | Suppress vnstock registration messages | Small performance cost on API key registration | Acceptable for one-time init |
| 30-day default lookback | Design choice | Can't get 1+ years data without specifying dates | Users can specify dates explicitly |

## Testing Strategy

### Coverage Areas
- Core data conversion functions
- Error handling and edge cases
- CLI command parsing and output formatting
- MCP tool invocation (17/21 passing as of v0.1.0)

### Known Test Results
- Domestic stock tools (history, intraday, financials): PASS
- Company data (overview, shareholders, etc.): PASS
- Listings (symbols, groups): PASS
- Forex/Crypto/Index (MSN source): Upstream bugs
- price_depth: Unsupported by current sources

## Security Considerations

### API Key Management
- API key stored in environment variable, not hardcoded
- Cleared from stdout during registration to protect MCP protocol
- `ensure_api_key()` idempotent to avoid re-registration

### Input Validation
- Symbol names automatically uppercased
- Dates passed through to vnstock (vnstock validates format)
- Source parameter restricted to known values (VCI, KBS) in docstrings

### Data Handling
- All data returned by vnstock assumed safe (third-party API)
- JSON serialization with `ensure_ascii=False` for Vietnamese characters
- No user-generated code execution

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| CLI invocation | <100ms | Python startup + import overhead |
| vnstock API call | 500ms-2s | Network dependent |
| DataFrame → dict conversion | <10ms | Typical 100-row result |
| JSON serialization | <1ms | Typical result size |
| MCP server startup | <200ms | Import overhead only |

## Maintenance Notes

- Update vnstock dependency when v3.6+ released (monitor GitHub releases)
- Monitor vnstock issues for timezone bugs affecting MSN source
- Ruff linting configured: E, F, W rules, 120-char line length
- Python 3.10+ required; test with 3.10, 3.11, 3.12, 3.13
