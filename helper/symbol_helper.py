from types import NoneType
from typing import List

from fastapi import HTTPException

import yfinance as yf
from fastapi.responses import JSONResponse


def verify_symbol(symbol):
    try:
        ticker = yf.Ticker(symbol)
        print(ticker.fast_info["symbol"])
    except AttributeError:
        return JSONResponse(
            status_code=400,
            content={"message": f"'{symbol}' is not a valid NASDAQ-listed stock"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Something went wrong verifying the requested stock "
                "symbol: " + str(e)
            },
        )


def get_stock_prices(symbols: str):
    symbol_list: List[str] = symbols.split(" ")
    last_prices: List[dict[str, str | float]] = []
    for symbol in symbol_list:
        verify_symbol(symbol)
        try:
            ticker = yf.Ticker(symbol)
            last_price: float = ticker.fast_info["lastPrice"]
            if last_price is None:
                last_price = 0
            symbol_uppercase = symbol.upper()
            print(type(last_price))
            last_prices.append({"symbol": symbol_uppercase, "lastPrice": last_price})
        except (Exception,):
            return JSONResponse(
                status_code=500,
                content={
                    "message": f"Something went wrong fetching the market data for {symbol}"
                },
            )
    return last_prices


def fetch_market_state(symbol: str):
    data = yf.Ticker(symbol)
    market_state = data.info["marketState"]
    if market_state is None:
        return "CLOSED"
    return market_state
