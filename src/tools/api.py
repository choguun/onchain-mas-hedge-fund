import os
from dotenv import load_dotenv
from typing import Dict, Any, List
import pandas as pd
import requests

# Load environment variables
load_dotenv()

def get_financial_metrics(
    ticker: str,
    report_period: str,
    period: str = 'ttm',
    limit: int = 1
) -> List[Dict[str, Any]]:
    """Fetch financial metrics from the API."""
    headers = {"X-API-KEY": os.environ.get("FINANCIAL_DATASETS_API_KEY")}
    url = (
        f"https://api.financialdatasets.ai/financial-metrics/"
        f"?ticker={ticker}"
        f"&report_period_lte={report_period}"
        f"&limit={limit}"
        f"&period={period}"
    )
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )
    data = response.json()
    financial_metrics = data.get("financial_metrics")
    if not financial_metrics:
        raise ValueError("No financial metrics returned")
    return financial_metrics

def search_line_items(
    ticker: str,
    line_items: List[str],
    period: str = 'ttm',
    limit: int = 1
) -> List[Dict[str, Any]]:
    """Fetch cash flow statements from the API."""
    headers = {"X-API-KEY": os.environ.get("FINANCIAL_DATASETS_API_KEY")}
    url = "https://api.financialdatasets.ai/financials/search/line-items"

    body = {
        "tickers": [ticker],
        "line_items": line_items,
        "period": period,
        "limit": limit
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )
    data = response.json()
    search_results = data.get("search_results")
    if not search_results:
        raise ValueError("No search results returned")
    return search_results

def get_insider_trades(
    ticker: str,
    end_date: str,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """
    Fetch insider trades for a given ticker and date range.
    """
    headers = {"X-API-KEY": os.environ.get("FINANCIAL_DATASETS_API_KEY")}
    url = (
        f"https://api.financialdatasets.ai/insider-trades/"
        f"?ticker={ticker}"
        f"&filing_date_lte={end_date}"
        f"&limit={limit}"
    )
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )
    data = response.json()
    insider_trades = data.get("insider_trades")
    if not insider_trades:
        raise ValueError("No insider trades returned")
    return insider_trades

def get_market_cap(
    ticker: str,
) -> List[Dict[str, Any]]:
    """Fetch market cap from the API."""
    headers = {"X-API-KEY": os.environ.get("FINANCIAL_DATASETS_API_KEY")}
    url = (
        f'https://api.financialdatasets.ai/company/facts'
        f'?ticker={ticker}'
    )

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )
    data = response.json()
    company_facts = data.get('company_facts')
    if not company_facts:
        raise ValueError("No company facts returned")
    return company_facts.get('market_cap')

def get_prices(
    ticker: str,
    start_date: str,
    end_date: str
) -> List[Dict[str, Any]]:
    """Fetch price data from the API."""
    headers = {"X-API-KEY": os.environ.get("FINANCIAL_DATASETS_API_KEY")}
    url = (
        f"https://api.financialdatasets.ai/prices/"
        f"?ticker={ticker}"
        f"&interval=day"
        f"&interval_multiplier=1"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
    )
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )
    data = response.json()
    prices = data.get("prices")
    if not prices:
        raise ValueError("No price data returned")
    return prices

def prices_to_df(prices: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert prices to a DataFrame."""
    df = pd.DataFrame(prices)
    df["Date"] = pd.to_datetime(df["time"])
    df.set_index("Date", inplace=True)
    numeric_cols = ["open", "close", "high", "low", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.sort_index(inplace=True)
    return df

# Update the get_price_data function to use the new functions
def get_price_data(
    ticker: str,
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    prices = get_prices(ticker, start_date, end_date)
    return prices_to_df(prices)

def get_crypto_ohlcv(
    contract_address: str,
    start_date: str,
    end_date: str,
    interval: str = 'daily',
    count: int = 500
) -> List[Dict[str, Any]]:
    """Mock OHLCV data for demonstration"""
    # Mock data for BTC prices
    mock_data = [
        {
            "timestamp": "2024-03-01T00:00:00.000Z",
            "quote": {
                "USD": {
                    "open": 62000.0,
                    "high": 63500.0,
                    "low": 61800.0,
                    "close": 63000.0,
                    "volume": 25000000000,
                    "market_cap": 1230000000000
                }
            }
        },
        {
            "timestamp": "2024-03-02T00:00:00.000Z",
            "quote": {
                "USD": {
                    "open": 63000.0,
                    "high": 64800.0,
                    "low": 62900.0,
                    "close": 64500.0,
                    "volume": 28000000000,
                    "market_cap": 1250000000000
                }
            }
        },
        {
            "timestamp": "2024-03-03T00:00:00.000Z",
            "quote": {
                "USD": {
                    "open": 64500.0,
                    "high": 67000.0,
                    "low": 64200.0,
                    "close": 66800.0,
                    "volume": 32000000000,
                    "market_cap": 1280000000000
                }
            }
        },
        {
            "timestamp": "2024-03-04T00:00:00.000Z",
            "quote": {
                "USD": {
                    "open": 66800.0,
                    "high": 69000.0,
                    "low": 66500.0,
                    "close": 68500.0,
                    "volume": 35000000000,
                    "market_cap": 1320000000000
                }
            }
        },
        {
            "timestamp": "2024-03-05T00:00:00.000Z",
            "quote": {
                "USD": {
                    "open": 68500.0,
                    "high": 71000.0,
                    "low": 68200.0,
                    "close": 70800.0,
                    "volume": 38000000000,
                    "market_cap": 1350000000000
                }
            }
        }
    ]
    
    return mock_data

def crypto_ohlcv_to_df(ohlcv_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert CoinMarketCap OHLCV data to DataFrame."""
    df = pd.DataFrame([
        {
            'Date': quote['timestamp'],  # Changed from time_open to timestamp
            'open': quote['quote']['USD']['open'],
            'high': quote['quote']['USD']['high'],
            'low': quote['quote']['USD']['low'],
            'close': quote['quote']['USD']['close'],
            'volume': quote['quote']['USD']['volume'],
            'market_cap': quote['quote']['USD']['market_cap']
        }
        for quote in ohlcv_data
    ])
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    return df
