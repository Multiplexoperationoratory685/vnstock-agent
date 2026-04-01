"""FastMCP server for VNStock - supports stdio, SSE, and Streamable HTTP transports."""

import json
import sys
from typing import Optional

from fastmcp import FastMCP

from vnstock_agent import core
from vnstock_agent.config import TRANSPORT, SERVER_HOST, SERVER_PORT

mcp = FastMCP(
    "vnstock-agent",
    instructions="Vietnamese stock market data - historical prices, financials, company info, and more",
)


# --- Quote tools ---


@mcp.tool()
def stock_history(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
    source: str = "VCI",
) -> str:
    """Get historical OHLCV price data for a Vietnamese stock.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB, VCB)
        start: Start date YYYY-MM-DD (default: 30 days ago)
        end: End date YYYY-MM-DD (default: today)
        interval: Time interval - 1m, 5m, 15m, 30m, 1H, 1D, 1W, 1M (default: 1D)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.stock_history(symbol, start, end, interval, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def stock_intraday(
    symbol: str,
    page_size: int = 100,
    source: str = "VCI",
) -> str:
    """Get intraday (today's) trading data for a stock.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        page_size: Number of records to return (default: 100)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.stock_intraday(symbol, page_size, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def stock_price_depth(
    symbol: str,
    source: str = "VCI",
) -> str:
    """Get order book / price depth (bid/ask levels) for a stock.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.stock_price_depth(symbol, source)
    return json.dumps(data, ensure_ascii=False, default=str)


# --- Company tools ---


@mcp.tool()
def company_overview(symbol: str, source: str = "VCI") -> str:
    """Get company overview information (industry, market cap, description, etc).

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.company_overview(symbol, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def company_shareholders(symbol: str, source: str = "VCI") -> str:
    """Get major shareholders of a company.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.company_shareholders(symbol, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def company_officers(symbol: str, source: str = "VCI") -> str:
    """Get company officers / management team.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.company_officers(symbol, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def company_news(symbol: str, source: str = "VCI") -> str:
    """Get latest news about a company.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.company_news(symbol, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def company_events(symbol: str, source: str = "VCI") -> str:
    """Get company events (dividends, AGM, earnings, etc).

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.company_events(symbol, source)
    return json.dumps(data, ensure_ascii=False, default=str)


# --- Financial tools ---


@mcp.tool()
def financial_balance_sheet(
    symbol: str,
    period: str = "quarter",
    source: str = "VCI",
) -> str:
    """Get balance sheet data for a company.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        period: Reporting period - quarter or annual (default: quarter)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.financial_balance_sheet(symbol, period, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def financial_income_statement(
    symbol: str,
    period: str = "quarter",
    source: str = "VCI",
) -> str:
    """Get income statement data for a company.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        period: Reporting period - quarter or annual (default: quarter)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.financial_income_statement(symbol, period, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def financial_cash_flow(
    symbol: str,
    period: str = "quarter",
    source: str = "VCI",
) -> str:
    """Get cash flow statement for a company.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        period: Reporting period - quarter or annual (default: quarter)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.financial_cash_flow(symbol, period, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def financial_ratio(
    symbol: str,
    period: str = "quarter",
    source: str = "VCI",
) -> str:
    """Get financial ratios (P/E, P/B, ROE, ROA, etc) for a company.

    Args:
        symbol: Stock ticker symbol (e.g. VNM, FPT, ACB)
        period: Reporting period - quarter or annual (default: quarter)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.financial_ratio(symbol, period, source)
    return json.dumps(data, ensure_ascii=False, default=str)


# --- Listing tools ---


@mcp.tool()
def listing_all_symbols(source: str = "VCI") -> str:
    """Get all listed stock symbols on Vietnamese exchanges (HOSE, HNX, UPCOM).

    Args:
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.listing_all_symbols(source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def listing_symbols_by_group(group: str = "VN30", source: str = "VCI") -> str:
    """Get stock symbols in a market group.

    Args:
        group: Market group - VN30, HNX30, HOSE, HNX, UPCOM, VN100, VNALL, etc (default: VN30)
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.listing_symbols_by_group(group, source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def listing_symbols_by_exchange(source: str = "VCI") -> str:
    """Get stock symbols grouped by exchange (HOSE, HNX, UPCOM).

    Args:
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.listing_symbols_by_exchange(source)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def listing_industries(source: str = "VCI") -> str:
    """Get ICB industry classification for Vietnamese stocks.

    Args:
        source: Data source - VCI or KBS (default: VCI)
    """
    data = core.listing_industries(source)
    return json.dumps(data, ensure_ascii=False, default=str)


# --- Trading tools ---


@mcp.tool()
def trading_price_board(
    symbols: str,
    source: str = "VCI",
) -> str:
    """Get real-time price board for multiple stocks.

    Args:
        symbols: Comma-separated stock symbols (e.g. "VNM,FPT,ACB,VCB")
        source: Data source - VCI or KBS (default: VCI)
    """
    symbols_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    data = core.trading_price_board(symbols_list, source)
    return json.dumps(data, ensure_ascii=False, default=str)


# --- Global market tools ---


@mcp.tool()
def fx_history(
    symbol: str = "EURUSD",
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
) -> str:
    """Get forex (currency pair) historical price data.

    Args:
        symbol: Currency pair (e.g. EURUSD, GBPUSD, USDJPY)
        start: Start date YYYY-MM-DD (default: 30 days ago)
        end: End date YYYY-MM-DD (default: today)
        interval: Time interval - 1D, 1W, 1M (default: 1D)
    """
    data = core.fx_history(symbol, start, end, interval)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def crypto_history(
    symbol: str = "BTC",
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
) -> str:
    """Get cryptocurrency historical price data.

    Args:
        symbol: Crypto symbol (e.g. BTC, ETH, SOL)
        start: Start date YYYY-MM-DD (default: 30 days ago)
        end: End date YYYY-MM-DD (default: today)
        interval: Time interval - 1D, 1W, 1M (default: 1D)
    """
    data = core.crypto_history(symbol, start, end, interval)
    return json.dumps(data, ensure_ascii=False, default=str)


@mcp.tool()
def world_index_history(
    symbol: str = "DJI",
    start: Optional[str] = None,
    end: Optional[str] = None,
    interval: str = "1D",
) -> str:
    """Get world market index historical data.

    Args:
        symbol: Index symbol (e.g. DJI for Dow Jones, IXIC for NASDAQ, GSPC for S&P 500)
        start: Start date YYYY-MM-DD (default: 30 days ago)
        end: End date YYYY-MM-DD (default: today)
        interval: Time interval - 1D, 1W, 1M (default: 1D)
    """
    data = core.world_index_history(symbol, start, end, interval)
    return json.dumps(data, ensure_ascii=False, default=str)


# --- Fund tools ---


@mcp.tool()
def fund_listing() -> str:
    """Get list of open-ended mutual funds available in Vietnam."""
    data = core.fund_listing()
    return json.dumps(data, ensure_ascii=False, default=str)


# --- Server entry point ---


def run():
    """Run the MCP server with configured transport."""
    transport = TRANSPORT.lower()
    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "sse":
        mcp.run(transport="sse", host=SERVER_HOST, port=SERVER_PORT)
    elif transport == "http":
        mcp.run(transport="streamable-http", host=SERVER_HOST, port=SERVER_PORT)
    else:
        print(f"Unknown transport: {transport}. Use stdio, sse, or http.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run()
