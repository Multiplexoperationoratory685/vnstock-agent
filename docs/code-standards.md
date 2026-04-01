# Code Standards & Conventions

## Overview
This document outlines the coding standards, patterns, and conventions used throughout the VNStock Agent codebase. All contributors must follow these standards to maintain consistency and quality.

## Language & Python Version

**Language**: Python 3.10+
**Target Versions**: 3.10, 3.11, 3.12, 3.13

Code must be compatible with Python 3.10 as minimum. Use standard library features available in 3.10; avoid 3.11+ only features.

## Linting & Code Quality

### Ruff Configuration
```
[tool.ruff]
line-length = 120
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W"]
```

**Rules Enforced**:
- **E**: PEP 8 errors (whitespace, indentation, naming)
- **F**: Pyflakes (undefined names, unused imports)
- **W**: PEP 8 warnings (whitespace)

**Run Linting**:
```bash
ruff check src/
ruff format src/  # Auto-format if needed
```

**Line Length**: Maximum 120 characters (generous for readability).

### No Additional Formatters
Do not use black, isort, or other formatters. Ruff is sole authority for code style.

## File Organization

### Module Structure
```
src/vnstock_agent/
├── __init__.py      # Package metadata (minimal)
├── config.py        # Configuration (environment variables)
├── core.py          # Business logic (data functions)
├── server.py        # MCP server (FastMCP tools)
└── cli.py           # CLI (Click commands)
```

### Principle: Single Responsibility
Each module has one clear responsibility:
- **config.py**: Configuration loading and API key management
- **core.py**: Data transformation and vnstock integration
- **server.py**: MCP protocol and tool exposure
- **cli.py**: CLI interface and output formatting

### No Circular Imports
- config.py imports: stdlib only
- core.py imports: config, stdlib, third-party libs
- server.py imports: core, config, fastmcp, stdlib
- cli.py imports: core, config, click, stdlib

## Naming Conventions

### Modules & Files
- Use snake_case: `config.py`, `core.py`, `server.py`, `cli.py`
- Descriptive names that indicate purpose
- No abbreviations (use `configuration` not `conf`)

### Functions & Methods
- Use snake_case: `get_stock()`, `_df_to_records()`, `ensure_api_key()`
- Private functions prefixed with underscore: `_safe_call()`, `_suppress_stdout()`
- Public functions have no underscore prefix
- Verb-first naming: `ensure_api_key()`, `get_stock()`, not `api_key_ensure()`

### Constants
- Use UPPER_SNAKE_CASE: `VNSTOCK_API_KEY`, `DEFAULT_SOURCE`, `SERVER_HOST`
- Module-level constants at top of file
- Document origin (config.py, environment variable, etc.)

### Variables
- Use snake_case: `symbol`, `start_date`, `page_size`
- Avoid single-letter names except in loops: `for i in range(...)` acceptable
- Meaningful names preferred: `stock_data` over `data`

### Classes (Future Use)
- Use PascalCase: `VnstockClient`, `PriceBoard`
- Not currently used in v0.1.0 (all functions)

## Type Hints

### Required For Public Functions
All functions exposed in `core.py`, `server.py`, `cli.py` must have type hints:
```python
def stock_history(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
```

### Benefits
- Better IDE autocomplete and error detection
- Self-documenting code
- Catches type errors early

### Import Guidelines
```python
from typing import Optional
from datetime import datetime, timedelta
```

Use `Optional[T]` for nullable types, not `Union[T, None]`.

## Docstrings

### Function Docstrings Required For
- All public functions in core.py (exposed by server.py and cli.py)
- All MCP tool functions in server.py
- Internal functions with complex logic

### Format: Google Style
```python
def stock_history(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get historical OHLCV price data for a Vietnamese stock.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB, VCB)
        start: Start date YYYY-MM-DD (default: 30 days ago)
        end: End date YYYY-MM-DD (default: today)
        interval: Time interval - 1m, 5m, 15m, 30m, 1H, 1D, 1W, 1M (default: 1D)
        source: Data source - VCI or KBS (default: VCI)

    Returns:
        List of dicts with OHLCV data and metadata.

    Raises:
        Exception: If vnstock API call fails (wrapped in error dict).
    """
```

### Guidelines
- One-line summary first (period required)
- Blank line before Args/Returns/Raises
- Parameter descriptions include type and valid values
- Document exceptions only if not caught by `_safe_call()`

## Comments

### When To Add Comments
- **Complex logic**: Non-obvious algorithms or transformations
- **Workarounds**: Document why a hack is needed (with issue link if available)
- **Assumptions**: Document expected data shapes, invariants
- **Gotchas**: Flag dangerous operations or surprising behaviors

### When NOT To Add Comments
- **Obvious code**: `symbol = symbol.upper()` needs no comment
- **Docstrings covered**: Don't repeat docstring info inline
- **Over-commenting**: Code should be self-explanatory first

### Comment Style
```python
# Initialize Vnstock with suppressed logging
vs = Vnstock(source=source, show_log=False)

# Flatten MultiIndex columns (e.g. ('listing', 'symbol') -> 'listing_symbol')
if isinstance(df.columns, pd.MultiIndex):
    df.columns = ["_".join(str(c) for c in col).strip("_") for col in df.columns]

# Suppress vnstock/vnai registration messages from polluting stdout
# See: https://github.com/thinh-vu/vnstock/issues/XXX
old_stdout = sys.stdout
sys.stdout = io.StringIO()
```

## Error Handling

### Pattern: Graceful Failure
All vnstock calls must use `_safe_call()`:
```python
def _safe_call(fn, *args, **kwargs) -> list[dict]:
    """Safely call a vnstock function, returning error message on failure."""
    try:
        result = fn(*args, **kwargs)
        return _df_to_records(result)
    except Exception as e:
        return [{"error": str(e)}]
```

This prevents MCP protocol crashes and CLI crashes. Always returns list[dict].

### When To Catch Exceptions
- Wrap all external API calls (vnstock)
- Wrap all file I/O operations (future)
- Wrap all network operations
- Don't catch `KeyError`, `AttributeError`, `TypeError` (catch bugs, not features)

### When NOT To Catch
- `KeyError`: Indicates code bug (wrong key access)
- `AttributeError`: Indicates code bug (wrong attribute)
- `TypeError`: Indicates code bug (wrong argument type)
- Let these propagate to catch programming errors

### Error Messages
- Be specific: `"API key not set"` not `"error"`
- Include context: `"Invalid symbol 'XYZ' - must be uppercase"`
- No sensitive data: Don't log API keys or full tracebacks

## Data Handling

### DataFrame to Dict Conversion
Always use `_df_to_records()` for consistency:
```python
def _df_to_records(df) -> list[dict]:
    """Handle NaN, Timestamps, MultiIndex, Series, dicts, tuples."""
    # ... handles all edge cases
```

This function:
- Converts NaN → None (JSON-serializable)
- Converts Timestamp → ISO string
- Flattens MultiIndex columns
- Returns list[dict] (JSON-safe)

### Timestamp Handling
Convert all timestamps to ISO format string:
```python
if pd.api.types.is_datetime64_any_dtype(df[col]):
    df[col] = df[col].astype(str)  # ISO format: "2025-01-01T10:30:00"
```

### JSON Serialization
Always use:
```python
json.dumps(data, ensure_ascii=False, default=str)
```

- `ensure_ascii=False`: Preserve Vietnamese characters (ầ, ũ, etc.)
- `default=str`: Fallback for non-serializable types

## Testing

### Test File Organization
```
tests/
├── test_core.py      # Unit tests for core.py functions
└── test_cli.py       # Integration tests for CLI commands
```

### Test Naming
- Test files: `test_*.py`
- Test functions: `test_<function>_<scenario>`, e.g. `test_stock_history_default_dates()`
- Test classes: `Test<Module>`, e.g. `TestCore`

### Test Patterns
```python
def test_stock_history_default_dates():
    """Test that missing dates default to last 30 days."""
    result = core.stock_history("VNM")
    assert isinstance(result, list)
    assert all(isinstance(r, dict) for r in result)

def test_stock_history_error_handling():
    """Test that API errors return graceful error dict."""
    result = core.stock_history("INVALID_SYMBOL")
    assert len(result) == 1
    assert "error" in result[0]
```

### Async Tests
Use pytest-asyncio for async functions:
```python
@pytest.mark.asyncio
async def test_async_tool():
    """Test async MCP tool."""
    result = await some_async_function()
    assert result is not None
```

### Test Configuration
```
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

## Dependencies

### Dependency Management
Maintain minimal dependencies. All dependencies in `pyproject.toml`:
```
vnstock>=3.5.0          # Core data provider
fastmcp>=2.0.0          # MCP framework
click>=8.0              # CLI
pandas>=1.5.0           # Data processing
pydantic-settings>=2.0  # Config
tabulate>=0.9.0         # Table formatting
uvicorn>=0.20.0         # HTTP server (optional)
```

### Pinning Strategy
- Use `>=` for minimum version (compatible)
- Don't pin exact versions (allow patch updates)
- Update major versions consciously

### Avoiding Dependency Creep
Before adding a new dependency:
- Check if stdlib already provides functionality
- Consider if benefit outweighs import overhead
- Document why the dependency is necessary

## Entry Points

### CLI Entry Point
```
[project.scripts]
vnstock-agent = "vnstock_agent.cli:main"
```

The `main` function must be a Click group that handles all CLI logic.

### MCP Server Entry Point
```
[project.scripts]
vnstock-mcp = "vnstock_agent.server:run"
```

The `run` function must initialize FastMCP server and select transport based on `VNSTOCK_MCP_TRANSPORT` env var.

## Version Management

### Version Bumping
Update version in two places:
1. `src/vnstock_agent/__init__.py`: `__version__ = "0.1.0"`
2. `pyproject.toml`: `version = "0.1.0"`

Keep them in sync.

### Semantic Versioning
- **Major (X)**: Breaking changes to API or output format
- **Minor (Y)**: New features, new tools, new commands
- **Patch (Z)**: Bug fixes, dependency updates, documentation

## Logging

### Logging Configuration
Suppress verbose third-party logging:
```python
logging.getLogger("vnstock").setLevel(logging.WARNING)
logging.getLogger("vnai").setLevel(logging.WARNING)
```

### When To Log
- Use logging for debugging complex flows
- Not for user-facing messages (use CLI output or error dicts)
- Log at DEBUG level for development info

### Logging Pattern
```python
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Processing symbol {symbol}")
```

## Configuration

### Environment Variables
All configuration via env vars, read in `config.py`:
```python
VNSTOCK_API_KEY = os.environ.get("VNSTOCK_API_KEY", "")
VNSTOCK_SOURCE = os.environ.get("VNSTOCK_SOURCE", "VCI")
VNSTOCK_MCP_TRANSPORT = os.environ.get("VNSTOCK_MCP_TRANSPORT", "stdio")
VNSTOCK_MCP_HOST = os.environ.get("VNSTOCK_MCP_HOST", "0.0.0.0")
VNSTOCK_MCP_PORT = int(os.environ.get("VNSTOCK_MCP_PORT", "8000"))
```

### No Hardcoded Defaults In Source
Defaults set in `config.py` only. Other modules import from config.

## Future-Proofing

### Deprecation Pattern
When removing a function/parameter:
1. Add warning comment for 1 version
2. Document in CHANGELOG
3. Remove in next major version

### Backward Compatibility
All output formats (table, JSON) must remain consistent. Breaking output format changes require major version bump.

## Commit Messages

### Format: Conventional Commits
```
<type>: <description>

<body> (optional)
```

**Types**:
- `feat`: New feature (new tool, new command)
- `fix`: Bug fix
- `refactor`: Code reorganization (no feature change)
- `test`: Test additions or fixes
- `docs`: Documentation updates
- `chore`: Dependency updates, build config (not allowed in .claude/)

**Examples**:
```
feat: add crypto_history tool for cryptocurrency data
fix: handle MultiIndex columns in DataFrame conversion
test: add test_stock_history_error_handling
docs: update deployment guide with SSE transport setup
```

## Code Review Checklist

Before submitting code, ensure:
- [ ] Ruff linting passes: `ruff check src/`
- [ ] Type hints on all public functions
- [ ] Docstrings for public functions
- [ ] Error handling with `_safe_call()` or try/except
- [ ] No hardcoded API keys or secrets
- [ ] No circular imports
- [ ] Tests pass: `pytest`
- [ ] Conventional commit message ready

## Anti-Patterns (DO NOT)

| Anti-Pattern | Why | Alternative |
|--------------|-----|-------------|
| Bare `except:` | Catches everything, hides bugs | Specific exception types |
| Global mutable state | Hard to test, side effects | Pass data through functions |
| Inline API keys | Security risk | Environment variables via config.py |
| Magic numbers | Unclear intent | Named constants or config |
| Huge functions (>50 lines) | Hard to test, hard to understand | Extract helper functions |
| `.format()` over f-strings | Older, less readable | f-strings (Python 3.6+) |
| Commented-out code | Confuses readers, bloats file | Delete or use version control |
| No type hints | IDE doesn't help, bugs hide | Always add type hints |
| Prints instead of logging | Can't control verbosity | Use logging module |
| Test data hardcoding | Tests break when data changes | Use fixtures or mocks |
