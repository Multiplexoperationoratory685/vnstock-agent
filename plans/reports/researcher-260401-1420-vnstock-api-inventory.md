# VNStock API Inventory for MCP Tools & CLI Commands

## Entry Point Classes (Main API)

### 1. Vnstock (Main Orchestrator)
**File:** `vnstock/common/client.py`

```python
Vnstock(symbol: Optional[str] = None, source: str = "KBS", show_log: bool = True)
├── .stock(symbol: Optional[str] = None, source: Optional[str] = None) → StockComponents
├── .fx(symbol: Optional[str] = 'EURUSD', source: Optional[str] = "MSN") → MSNComponents
├── .crypto(symbol: Optional[str] = 'BTC', source: Optional[str] = "MSN") → MSNComponents
├── .world_index(symbol: Optional[str] = 'DJI', source: Optional[str] = "MSN") → MSNComponents
└── .fund(source: str = "FMARKET") → Fund
```

---

## API Module Classes (via `vnstock/api/`)

### 2. Quote (Historical & Intraday Data)
**File:** `vnstock/api/quote.py` | Sources: VCI, MSN, KBS

```python
Quote(source: str = "KBS", symbol: str = "", random_agent: bool = False, show_log: bool = False)
├── .history(symbol: Optional[str] = None, start: str = None, end: str = None, interval: str = "D", **kwargs) → pd.DataFrame
├── .intraday(symbol: Optional[str] = None, page_size: int = 100, page: int = 1, **kwargs) → pd.DataFrame
└── .price_depth(symbol: Optional[str] = None, **kwargs) → pd.DataFrame
```

### 3. Company (Corporate Data)
**File:** `vnstock/api/company.py` | Sources: VCI, KBS

```python
Company(source: str = "KBS", symbol: str = None, random_agent: bool = False, show_log: bool = False)
├── .overview(*args, **kwargs) → Any
├── .shareholders(*args, **kwargs) → Any
├── .officers(filter_by: str = 'all'|'working'|'resigned', **kwargs) → Any
├── .subsidiaries(filter_by: str = 'all'|'subsidiary', **kwargs) → Any
├── .affiliate(*args, **kwargs) → Any
├── .news(*args, **kwargs) → Any
└── .events(*args, **kwargs) → Any
```

### 4. Finance (Financial Statements)
**File:** `vnstock/api/financial.py` | Sources: VCI, KBS

```python
Finance(source: str, symbol: str, period: str = "quarter", get_all: bool = True, show_log: bool = False)
├── .balance_sheet(period: str = None, lang: str = None, dropna: bool = None, **kwargs) → pd.DataFrame
├── .income_statement(lang: str = None, **kwargs) → pd.DataFrame
├── .cash_flow(period: str = None, **kwargs) → pd.DataFrame
└── .ratio(flatten_columns: bool = None, separator: str = None, **kwargs) → Any
```

### 5. Listing (Market Symbols & Indices)
**File:** `vnstock/api/listing.py` | Sources: KBS, VCI, MSN

```python
Listing(source: str = "kbs", random_agent: bool = False, show_log: bool = False)
├── .all_symbols(to_df: bool = None, **kwargs) → Any
├── .symbols_by_industries(**kwargs) → Any
├── .symbols_by_exchange(lang: str = None, **kwargs) → Any
├── .industries_icb(**kwargs) → Any
├── .symbols_by_group(group: str = None, **kwargs) → Any
├── .all_future_indices(**kwargs) → Any
├── .all_government_bonds(**kwargs) → Any
├── .all_covered_warrant(**kwargs) → Any
└── .all_bonds(**kwargs) → Any
```

### 6. Trading (Trading Stats & Order Book)
**File:** `vnstock/api/trading.py` | Sources: VCI, KBS

```python
Trading(source: str = "kbs", symbol: str = None, random_agent: bool = False, show_log: bool = False)
├── .trading_stats(start: str = None, end: str = None, limit: int = None, **kwargs) → Any
├── .side_stats(dropna: bool = None, **kwargs) → (pd.DataFrame, pd.DataFrame)
├── .price_board(symbols_list: List[str] = None, **kwargs) → pd.DataFrame
├── .price_history(symbols_list: List[str] = None, **kwargs) → Any
├── .foreign_trade(**kwargs) → Any
├── .prop_trade(**kwargs) → Any
├── .insider_deal(**kwargs) → Any
└── .order_stats(**kwargs) → Any
```

### 7. Fund (Mutual Fund Data)
**File:** `vnstock/explorer/fmarket/fund.py` | Source: FMARKET

```python
Fund(source: str = "FMARKET", random_agent: bool = False)
└── .listing(**kwargs) → Any
```

---

## Data Container Classes (Returned by Vnstock)

### 8. StockComponents
**File:** `vnstock/common/data.py`

```python
StockComponents(symbol: str, source: str = "KBS", show_log: bool = False)
├── .quote: Quote  # Historical & intraday data
├── .company: Company  # Corporate info
├── .finance: Finance  # Financial statements
├── .trading: Trading  # Trading stats
└── .listing: Listing  # Market data
```

### 9. MSNComponents & CryptoComponents
**File:** `vnstock/common/data.py`

```python
MSNComponents(symbol: str, source: str = "MSN")
└── .quote: Quote  # History & intraday for FX/crypto/indices
```

---

## Utility Functions (Authentication & Market Data)

### 10. Authentication & Configuration
**File:** `vnstock/core/utils/auth.py`

```python
register_user(email: str, full_name: str, **kwargs) → Dict
change_api_key(api_key: str, **kwargs) → Dict
check_status(**kwargs) → Dict
```

### 11. Indices & Market Constants
**File:** `vnstock/common/indices.py` & `vnstock/constants.py`

```python
get_all_indices() → pd.DataFrame  # All available indices
INDICES_INFO: Dict  # Index metadata
INDICES_MAP: Dict  # Symbol → Index mapping
INDEX_GROUPS: Dict  # Group-based indices (VN30, HNX30, etc.)
SECTOR_IDS: Dict  # Sector identifiers
EXCHANGES: Dict  # Exchange information
```

---

## Key Constants

### Data Sources
- **Domestic:** KBS, VCI
- **International:** MSN
- **Funds:** FMARKET

### Time Intervals
`1m`, `5m`, `15m`, `30m`, `1H`, `D` (daily), `1W` (weekly), `1M` (monthly)

### Return Types
- `pd.DataFrame` - Primary return for market/financial data
- `Dict` - Configuration/metadata
- `Tuple[pd.DataFrame, pd.DataFrame]` - Bid/ask pairs
- `Any` - Dynamic based on provider (pass-through)

---

## Summary Statistics

**Total Public Classes:** 7 (Quote, Company, Finance, Listing, Trading, Fund, Vnstock)  
**Total Methods:** 50+  
**Retry Policy:** Exponential backoff (2-10s, 3 attempts by default)  
**Default Timeout:** 30 seconds

**Status:** Research complete. All public APIs documented from source inspection.
