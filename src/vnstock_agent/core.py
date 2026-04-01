"""Core wrapper around vnstock library - shared by MCP server and CLI."""

import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from vnstock_agent.config import DEFAULT_SOURCE, ensure_api_key

logger = logging.getLogger(__name__)

# Suppress vnstock verbose logging
logging.getLogger("vnstock").setLevel(logging.WARNING)
logging.getLogger("vnai").setLevel(logging.WARNING)


def _df_to_records(df) -> list[dict]:
    """Convert DataFrame to list of dicts, handling NaN, Timestamps, and MultiIndex columns."""
    if df is None or (isinstance(df, pd.DataFrame) and df.empty):
        return []
    if isinstance(df, pd.DataFrame):
        # Flatten MultiIndex columns (e.g. ('listing', 'symbol') -> 'listing_symbol')
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ["_".join(str(c) for c in col).strip("_") for col in df.columns]
        df = df.where(pd.notnull(df), None)
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
        return df.to_dict(orient="records")
    if isinstance(df, dict):
        # Handle tuple keys in dicts too
        clean = {}
        for k, v in df.items():
            key = "_".join(str(c) for c in k) if isinstance(k, tuple) else str(k)
            clean[key] = v
        return [clean]
    if isinstance(df, pd.Series):
        return _df_to_records(df.to_frame())
    if isinstance(df, (list, tuple)):
        # Handle tuple of DataFrames (e.g. side_stats returns bid, ask pair)
        results = []
        for item in df:
            results.extend(_df_to_records(item))
        return results
    return [{"result": str(df)}]


def _default_dates(start: Optional[str], end: Optional[str]) -> tuple[str, str]:
    """Default to last 30 days if dates not provided."""
    if not end:
        end = datetime.now().strftime("%Y-%m-%d")
    if not start:
        start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    return start, end


def _safe_call(fn, *args, **kwargs) -> list[dict]:
    """Safely call a vnstock function, returning error message on failure."""
    try:
        result = fn(*args, **kwargs)
        return _df_to_records(result)
    except Exception as e:
        return [{"error": str(e)}]


def _get_stock(symbol: str, source: str = DEFAULT_SOURCE):
    """Get stock components for a symbol."""
    ensure_api_key()
    from vnstock import Vnstock
    vs = Vnstock(source=source, show_log=False)
    return vs.stock(symbol=symbol, source=source)


# --- Quote tools ---

def stock_history(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get historical OHLCV data for a stock symbol."""
    start, end = _default_dates(start, end)
    stock = _get_stock(symbol, source)
    df = stock.quote.history(start=start, end=end, interval=interval)
    return _df_to_records(df)


def stock_intraday(
    symbol: str,
    page_size: int = 100,
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get intraday trading data for a stock symbol."""
    stock = _get_stock(symbol, source)
    df = stock.quote.intraday(page_size=page_size)
    return _df_to_records(df)


def stock_price_depth(
    symbol: str,
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get order book / price depth data."""
    stock = _get_stock(symbol, source)
    return _safe_call(stock.quote.price_depth)


# --- Company tools ---

def company_overview(symbol: str, source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get company overview information."""
    stock = _get_stock(symbol, source)
    result = stock.company.overview()
    return _df_to_records(result)


def company_shareholders(symbol: str, source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get major shareholders of a company."""
    stock = _get_stock(symbol, source)
    result = stock.company.shareholders()
    return _df_to_records(result)


def company_officers(symbol: str, source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get company officers / management team."""
    stock = _get_stock(symbol, source)
    result = stock.company.officers()
    return _df_to_records(result)


def company_news(symbol: str, source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get company news."""
    stock = _get_stock(symbol, source)
    result = stock.company.news()
    return _df_to_records(result)


def company_events(symbol: str, source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get company events (dividends, AGM, etc)."""
    stock = _get_stock(symbol, source)
    result = stock.company.events()
    return _df_to_records(result)


# --- Finance tools ---

def financial_balance_sheet(
    symbol: str,
    period: str = "quarter",
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get balance sheet data."""
    stock = _get_stock(symbol, source)
    result = stock.finance.balance_sheet(period=period)
    return _df_to_records(result)


def financial_income_statement(
    symbol: str,
    period: str = "quarter",
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get income statement data."""
    stock = _get_stock(symbol, source)
    result = stock.finance.income_statement(period=period)
    return _df_to_records(result)


def financial_cash_flow(
    symbol: str,
    period: str = "quarter",
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get cash flow statement data."""
    stock = _get_stock(symbol, source)
    result = stock.finance.cash_flow(period=period)
    return _df_to_records(result)


def financial_ratio(
    symbol: str,
    period: str = "quarter",
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get financial ratios."""
    stock = _get_stock(symbol, source)
    result = stock.finance.ratio(period=period)
    return _df_to_records(result)


# --- Listing tools ---

def listing_all_symbols(source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get all listed stock symbols."""
    ensure_api_key()
    from vnstock.api.listing import Listing
    lst = Listing(source=source.lower())
    df = lst.all_symbols()
    return _df_to_records(df)


def listing_symbols_by_group(group: str = "VN30", source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get symbols by market group (VN30, HNX30, HOSE, etc)."""
    ensure_api_key()
    from vnstock.api.listing import Listing
    lst = Listing(source=source.lower())
    df = lst.symbols_by_group(group=group)
    return _df_to_records(df)


def listing_symbols_by_exchange(source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get symbols grouped by exchange."""
    ensure_api_key()
    from vnstock.api.listing import Listing
    lst = Listing(source=source.lower())
    df = lst.symbols_by_exchange()
    return _df_to_records(df)


def listing_industries(source: str = DEFAULT_SOURCE) -> list[dict]:
    """Get ICB industry classification."""
    ensure_api_key()
    from vnstock.api.listing import Listing
    lst = Listing(source=source.lower())
    df = lst.industries_icb()
    return _df_to_records(df)


# --- Trading tools ---

def trading_price_board(
    symbols: list[str],
    source: str = DEFAULT_SOURCE,
) -> list[dict]:
    """Get price board for multiple symbols."""
    ensure_api_key()
    from vnstock.api.trading import Trading
    t = Trading(source=source.lower())
    df = t.price_board(symbols_list=symbols)
    return _df_to_records(df)


# --- Global market tools ---

def _suppress_stdout(fn, *args, **kwargs):
    """Call function with stdout suppressed (vnstock/vnai prints to stdout)."""
    import sys
    import io
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        return fn(*args, **kwargs)
    finally:
        sys.stdout = old_stdout


def fx_history(
    symbol: str = "EURUSD",
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
) -> list[dict]:
    """Get forex historical data."""
    ensure_api_key()
    start, end = _default_dates(start, end)
    try:
        from vnstock import Vnstock
        vs = _suppress_stdout(Vnstock, source="MSN", show_log=False)
        pair = vs.fx(symbol=symbol)
        df = pair.quote.history(start=start, end=end, interval=interval)
        return _df_to_records(df)
    except Exception as e:
        return [{"error": str(e)}]


def crypto_history(
    symbol: str = "BTC",
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
) -> list[dict]:
    """Get cryptocurrency historical data."""
    ensure_api_key()
    start, end = _default_dates(start, end)
    try:
        from vnstock import Vnstock
        vs = _suppress_stdout(Vnstock, source="MSN", show_log=False)
        coin = vs.crypto(symbol=symbol)
        df = coin.quote.history(start=start, end=end, interval=interval)
        return _df_to_records(df)
    except Exception as e:
        return [{"error": str(e)}]


def world_index_history(
    symbol: str = "DJI",
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
) -> list[dict]:
    """Get world market index historical data."""
    ensure_api_key()
    start, end = _default_dates(start, end)
    try:
        from vnstock import Vnstock
        vs = _suppress_stdout(Vnstock, source="MSN", show_log=False)
        idx = vs.world_index(symbol=symbol)
        df = idx.quote.history(start=start, end=end, interval=interval)
        return _df_to_records(df)
    except Exception as e:
        return [{"error": str(e)}]


# --- Fund tools ---

def fund_listing() -> list[dict]:
    """Get list of open-ended mutual funds."""
    ensure_api_key()
    from vnstock import Vnstock
    vs = Vnstock(show_log=False)
    f = vs.fund()
    df = f.listing()
    return _df_to_records(df)
