# System Architecture

## High-Level Overview

VNStock Agent is a dual-interface application providing access to Vietnamese stock market data through:
1. **MCP Server**: Exposes 21 tools for AI assistants (Claude, GPT, Cursor)
2. **CLI**: Command-line interface with 22 commands for terminal users

Both interfaces share a common data layer (`core.py`) that wraps the `vnstock` library.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interfaces                          │
├──────────────────────────┬──────────────────────┬────────────────┤
│   MCP Clients            │   CLI (Terminal)     │  Future: API   │
│                          │                      │  (HTTP REST)   │
│  • Claude Desktop        │  • vnstock-agent     │  (Planned)     │
│  • Cursor Editor         │    command           │                │
│  • Other MCP Clients     │  • Shell/Bash        │                │
│                          │  • Automation        │                │
└──────────────┬───────────┴──────────┬───────────┴────────────────┘
               │                      │
┌──────────────▼──────────────────────▼──────────────────────────────┐
│                      Transport Layer                               │
├─────────────────────┬──────────────────────┬──────────────────────┤
│   stdio             │   SSE / HTTP         │   Custom Transports  │
│ (FastMCP default)   │  (FastAPI + uvicorn) │  (Future)            │
│ - Claude Desktop    │  - Long-lived        │                      │
│ - Cursor            │  - Streaming         │                      │
│ - Direct stdin/out  │  - Event-driven      │                      │
└─────────────────────┴──────────────────────┴──────────────────────┘
               │                      │
┌──────────────▼──────────────────────▼──────────────────────────────┐
│                    Application Layer (FastMCP)                     │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  server.py: MCP Tools (21 tools)                                  │
│  ├── Stock Quotes (3)         cli.py: CLI Commands (22)           │
│  │   • stock_history          ├── Quote Commands (3)              │
│  │   • stock_intraday         │   • history                       │
│  │   • stock_price_depth      │   • intraday                      │
│  │                            │   • depth                         │
│  ├── Company (5)              │                                    │
│  │   • company_overview       ├── Company Commands (5)            │
│  │   • company_shareholders   │   • overview, shareholders        │
│  │   • company_officers       │   • officers, news, events        │
│  │   • company_news           │                                    │
│  │   • company_events         ├── Finance Commands (4)            │
│  │                            │   • balance-sheet, income         │
│  ├── Financials (4)           │   • cashflow, ratio               │
│  │   • financial_*_sheet      │                                    │
│  │   • financial_income_stmt  ├── Listing Commands (4)            │
│  │   • financial_cash_flow    │   • symbols, group                │
│  │   • financial_ratio        │   • exchange, industries          │
│  │                            │                                    │
│  ├── Listings (4)             ├── Trading/Global/Fund (5)         │
│  │   • listing_all_symbols    │   • board, fx, crypto             │
│  │   • listing_symbols_by_*   │   • index, funds, serve           │
│  │   • listing_industries     │                                    │
│  │                            │                                    │
│  ├── Trading (1)              │                                    │
│  │   • trading_price_board    │                                    │
│  │                            │                                    │
│  ├── Global Markets (3)       │                                    │
│  │   • fx_history             │                                    │
│  │   • crypto_history         │                                    │
│  │   • world_index_history    │                                    │
│  │                            │                                    │
│  └── Funds (1)                │                                    │
│      • fund_listing           │                                    │
│                               │                                    │
│  All tools/commands wrap core.py functions and return JSON        │
└────────────────┬──────────────────────────┬──────────────────────┘
                 │                          │
       ┌─────────▼──────────────────────────▼────────┐
       │      Configuration & Data Layer             │
       ├──────────────────────────────────────────────┤
       │                                              │
       │  config.py                                   │
       │  ├── VNSTOCK_API_KEY (env var)              │
       │  ├── VNSTOCK_SOURCE (VCI|KBS)               │
       │  ├── VNSTOCK_MCP_TRANSPORT                  │
       │  ├── VNSTOCK_MCP_HOST / PORT                │
       │  └── ensure_api_key()                       │
       │                                              │
       │  core.py (326 LOC - Shared Logic)           │
       │  ├── _df_to_records()    (Data conversion)  │
       │  ├── _safe_call()        (Error handling)   │
       │  ├── _get_stock()        (Vnstock init)     │
       │  ├── stock_*()           (Quote functions)  │
       │  ├── company_*()         (Company data)     │
       │  ├── financial_*()       (Accounting)       │
       │  ├── listing_*()         (Securities list)  │
       │  ├── trading_*()         (Market data)      │
       │  ├── fx_history()        (Forex)            │
       │  ├── crypto_history()    (Crypto)           │
       │  ├── world_index_history() (Indices)        │
       │  └── fund_listing()      (Mutual funds)     │
       │                                              │
       └──────────────────────────────────────────────┘
                    │
         ┌──────────▼────────────┐
         │   Third-Party APIs    │
         ├───────────────────────┤
         │                       │
         │  vnstock 3.5.0        │
         │  ├── VCI Source       │
         │  ├── KBS Source       │
         │  └── MSN Source       │
         │                       │
         │  Vietnamese Stock     │
         │  Market Data:         │
         │  • HOSE Exchange      │
         │  • HNX Exchange       │
         │  • UPCOM Exchange     │
         │  • Global Markets     │
         │                       │
         └───────────────────────┘
```

## Component Interaction Flow

### MCP Server Request Flow

```
MCP Client (Claude Desktop)
        │
        ▼
  MCP Request
  (tool call: stock_history)
        │
        ▼
  server.py
  @mcp.tool() decorator
  stock_history(...) handler
        │
        ▼
  core.stock_history(symbol, start, end, interval, source)
        │
        ▼
  _get_stock(symbol, source)
        │
        ▼
  vnstock.Vnstock(source=source)
        │
        ▼
  stock.quote.history(start, end, interval)
        │
        ▼
  pandas.DataFrame (OHLCV data)
        │
        ▼
  _df_to_records()
  - Flatten MultiIndex columns
  - Convert NaN → None
  - Convert Timestamp → ISO string
  - Return list[dict]
        │
        ▼
  json.dumps(data, ensure_ascii=False)
        │
        ▼
  MCP Response (JSON string)
        │
        ▼
  MCP Client (Claude Desktop)
```

### CLI Command Flow

```
Terminal User
        │
        ▼
  $ vnstock-agent history VNM --start 2025-01-01
        │
        ▼
  cli.py Click group & command parsing
        │
        ▼
  history() command handler
        │
        ▼
  core.stock_history(symbol.upper(), start, end, interval, source)
        │
        ▼
  [Same as MCP flow above: core → vnstock → DataFrame → list[dict]]
        │
        ▼
  _output(data, format)
  - If format == "table":
    - tabulate(data, headers="keys", tablefmt="simple")
    - click.echo(table_string)
  - If format == "json":
    - json.dumps(data, indent=2, ensure_ascii=False)
    - click.echo(json_string)
        │
        ▼
  Terminal Output
```

## Data Transformation Pipeline

```
vnstock Library Output
    │
    ├── DataFrame
    │   ├── Single or MultiIndex columns
    │   ├── NaN values
    │   ├── Timestamp columns
    │   └── Multiple rows
    │
    ├── Series
    │   └── Single column, multiple rows
    │
    ├── dict
    │   ├── Simple key-value
    │   └── Tuple keys (flattened)
    │
    └── tuple
        └── Multiple DataFrames (bid/ask)

           │
           ▼

   _df_to_records() Function

   [Step 1] Flatten MultiIndex columns
   ("listing", "symbol") → "listing_symbol"

   [Step 2] Replace NaN with None
   np.nan → None (JSON-safe)

   [Step 3] Convert Timestamps to strings
   Timestamp("2025-01-01 10:30:00") → "2025-01-01T10:30:00"

   [Step 4] Handle multiple input types
   DataFrame → list of dicts
   Series → single dict in list
   tuple of DataFrames → concatenated list

           │
           ▼

   list[dict] (JSON-Serializable)
   [
     {"symbol": "VNM", "date": "2025-01-01", "open": 76000, ...},
     {"symbol": "VNM", "date": "2025-01-02", "open": 76500, ...},
     ...
   ]

           │
           ▼

   JSON Serialization
   json.dumps(data, ensure_ascii=False, default=str)
   - ensure_ascii=False preserves Vietnamese characters
   - default=str catches remaining non-serializable types

           │
           ▼

   JSON Output
   {
     "symbol": "VNM",
     "date": "2025-01-01",
     "open": 76000,
     ...
   }
```

## Transport Layer Architecture

### Transport 1: stdio (Default)

```
MCP Client (Claude Desktop)
        │
        ▼
   stdin → FastMCP Server → stdout
   (Text-based protocol)
        │
        ▼
   Process synchronously
   One request at a time
        │
        ▼
   No network overhead
   Direct process communication
```

**Configuration**:
```bash
export VNSTOCK_MCP_TRANSPORT=stdio
vnstock-mcp  # Runs in foreground, listens on stdin
```

**Best For**: Claude Desktop, Cursor, local development

---

### Transport 2: SSE (Server-Sent Events)

```
MCP Client (HTTP)
        │
        ▼
   HTTP GET /sse
   (Establish connection)
        │
        ▼
   FastAPI + uvicorn
   └─ FastMCP SSE transport
   (Long-lived HTTP connection)
        │
        ▼
   Server streams events
   data: {json response}
        │
        ▼
   Client reads streamed events
```

**Configuration**:
```bash
export VNSTOCK_MCP_TRANSPORT=sse
export VNSTOCK_MCP_PORT=8000
vnstock-mcp  # Starts HTTP server on 0.0.0.0:8000
```

**Best For**: Remote MCP clients, multi-client scenarios

---

### Transport 3: Streamable HTTP

```
MCP Client (HTTP)
        │
        ▼
   HTTP POST /mcp
   {json request}
        │
        ▼
   FastAPI + uvicorn
   └─ FastMCP HTTP transport
   (Request-response model)
        │
        ▼
   Process request
   Return JSON response
        │
        ▼
   HTTP 200
   {json response}
```

**Configuration**:
```bash
export VNSTOCK_MCP_TRANSPORT=http
export VNSTOCK_MCP_PORT=8000
vnstock-mcp  # Starts HTTP server on 0.0.0.0:8000
```

**Best For**: REST API integrations, custom clients

## Configuration Management

### Environment Variables (Centralized in config.py)

```
┌─────────────────────────────────────────┐
│      Environment Variables              │
├─────────────────────────────────────────┤
│                                         │
│ VNSTOCK_API_KEY                         │
│ └─ Required for some operations         │
│    Stored securely, never logged        │
│                                         │
│ VNSTOCK_SOURCE                          │
│ └─ Default: "VCI"                       │
│    Values: VCI, KBS, MSN                │
│                                         │
│ VNSTOCK_MCP_TRANSPORT                   │
│ └─ Default: "stdio"                     │
│    Values: stdio, sse, http             │
│                                         │
│ VNSTOCK_MCP_HOST                        │
│ └─ Default: "0.0.0.0"                   │
│    Only for sse/http transports         │
│                                         │
│ VNSTOCK_MCP_PORT                        │
│ └─ Default: "8000"                      │
│    Only for sse/http transports         │
│                                         │
└─────────────────────────────────────────┘
         │
         ▼
    config.py
    (Load on import)
         │
         ▼
    Global variables
    VNSTOCK_API_KEY, DEFAULT_SOURCE, etc.
         │
         ▼
    Used by core, server, cli
```

## Module Dependency Graph

```
Dependency Direction: A imports B

config.py
└─ (no external imports, stdlib only)

core.py
├─ config.py (settings)
├─ vnstock (market data)
└─ pandas (DataFrame)

server.py
├─ core.py (business logic)
├─ config.py (settings)
├─ fastmcp (MCP framework)
└─ stdlib (json, sys)

cli.py
├─ core.py (business logic)
├─ config.py (settings)
├─ click (CLI framework)
├─ tabulate (optional, table formatting)
└─ stdlib (json, sys)

__init__.py
└─ (no imports, metadata only)
```

**No Circular Imports**: Each module depends on modules below it (acyclic).

## Error Handling Architecture

```
vnstock API Call
        │
        ▼
  _safe_call(fn, *args, **kwargs)
        │
        ├─ Try:
        │   └─ result = fn(*args, **kwargs)
        │       └─ _df_to_records(result)
        │
        └─ Except Exception as e:
            └─ [{"error": str(e)}]

              ▼

  Return: list[dict]
  
  Always:
  - Never raise exceptions
  - Always return list[dict]
  - Error object: {"error": "description"}
  - Success objects: {"field1": value1, "field2": value2, ...}

              ▼

  MCP Server:
  json.dumps() → JSON string

  CLI:
  _output(data, format) → Pretty-printed output
```

## Concurrency & Async Handling

### Current Architecture
- **Synchronous**: All functions are synchronous (blocking)
- **Single-threaded CLI**: CLI processes one command at a time
- **Async MCP Server**: FastMCP handles async internally for stdio/SSE/HTTP

### Future Considerations
- For high-concurrency scenarios, consider async core.py functions
- FastMCP supports both sync and async tool handlers
- CLI remains synchronous (CLI interactions are inherently sequential)

## Security Architecture

```
User Input
    │
    ├─ CLI: Symbol arguments
    │  └─ Converted to uppercase (normalize)
    │
    ├─ CLI: Date arguments
    │  └─ Passed to vnstock (vnstock validates format)
    │
    └─ MCP: Tool parameters
       └─ Type hints + validation by FastMCP

         ▼

    API Key Management
    ├─ Stored in environment variable (not in code)
    ├─ Registered once with vnstock
    ├─ Stdout suppressed during registration
    │  (prevents leaking into MCP protocol)
    └─ Never logged or printed

         ▼

    Data Handling
    ├─ All data from vnstock assumed safe
    ├─ JSON serialization with ensure_ascii=False
    │  (no code injection risk)
    └─ No eval(), exec(), or dynamic code execution

         ▼

    Output
    ├─ CLI: Terminal output (safe)
    ├─ MCP: JSON response (safe)
    └─ No HTML escaping needed (not web-facing)
```

## Scalability Considerations

### Current Limits
- **Requests/second**: Limited by vnstock API rate limits (not vnstock-agent)
- **Response size**: Limited by available memory (pandas DataFrames)
- **Concurrent connections**: Limited by FastMCP transport (stdio is single-process, SSE/HTTP scales with uvicorn workers)

### Bottlenecks
1. **vnstock API**: 3-5 second response time typical
2. **DataFrame conversion**: <10ms for typical 100-row result
3. **JSON serialization**: <1ms for typical result size

### Scaling Strategy (Future)
- Caching layer for frequently accessed data (v0.2.0)
- Connection pooling for HTTP transport
- Async core functions for concurrent API calls
- Database backend for historical caching

## Deployment Architecture

### Development
```
Developer Workstation
└─ python -m pip install -e ".[dev]"
└─ pytest  # Run tests
└─ vnstock-agent --help  # CLI usage
└─ vnstock-mcp  # Start MCP server (stdio)
```

### Production: Claude Desktop
```
User's Machine
├─ pip install vnstock-agent
└─ Claude Desktop config
    └─ mcpServers > vnstock
        └─ command: vnstock-mcp
        └─ env: VNSTOCK_API_KEY
```

### Production: Docker (Future)
```
Docker Container
├─ Python 3.10+
├─ vnstock-agent installed
└─ Environment variables injected
└─ Port 8000 exposed for SSE/HTTP
```

### Production: Cloud (Future)
```
AWS Lambda / Google Cloud Run
├─ Serverless function
├─ HTTP transport
└─ Auto-scaling on demand
```

## Observability & Monitoring (Future)

```
Application
├─ Logging
│  └─ DEBUG: Function calls, arguments
│  └─ WARNING: API errors, retries
│  └─ ERROR: Exceptions caught
│
├─ Metrics
│  └─ Request count by tool
│  └─ Response time by tool
│  └─ Error rate
│  └─ Cache hit rate (future)
│
└─ Tracing (OpenTelemetry)
   └─ Distributed tracing for multi-service
   └─ Performance profiling
```

## Maintenance Touchpoints

### When Updating vnstock Dependency
1. Check vnstock release notes for breaking changes
2. Test affected tools with new version
3. Update pyproject.toml version constraint
4. Run full test suite
5. Update CHANGELOG

### When Adding New Stock Tool
1. Implement in core.py
2. Add MCP tool wrapper in server.py
3. Add CLI command in cli.py
4. Write unit tests in tests/test_core.py
5. Write integration tests in tests/test_cli.py
6. Update docs/codebase-summary.md

### When Changing Output Format
1. Update data transformation in core._df_to_records()
2. Ensure backward compatibility or bump major version
3. Update all tools/commands
4. Update CLI table formatting if needed
5. Update test expectations
6. Document changes in CHANGELOG
