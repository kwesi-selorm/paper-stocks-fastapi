from typing import List

import yfinance as yf
from fastapi import HTTPException


def verify_symbol(symbol):
    try:
        ticker = yf.Ticker(symbol)
        print(ticker.fast_info["symbol"])
    except AttributeError:
        raise HTTPException(status_code=400, detail={"message": f"'{symbol}' is not a valid NASDAQ-listed stock"})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": f"Something went wrong verifying the requested stock "
                                                                "symbol: " + str(e)})


def get_stock_prices(symbols: List[str]):
    last_prices: dict[str, int] = {}
    for symbol in symbols:
        verify_symbol(symbol)
        try:
            ticker = yf.Ticker(symbol)
            last_price = ticker.fast_info["lastPrice"]
            last_prices[symbol] = last_price
        except:
            raise HTTPException(status_code=500,
                                detail={"message": f"Something went wrong fetching the market data for {symbol}"})
