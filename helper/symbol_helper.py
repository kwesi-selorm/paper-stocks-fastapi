from typing import List

import yfinance as yf
from fastapi.responses import JSONResponse


def verify_symbol(symbol):
    try:
        ticker = yf.Ticker(symbol)
        print(ticker.fast_info["symbol"])
    except AttributeError:
        return JSONResponse(status_code=400, content={"message": f"'{symbol}' is not a valid NASDAQ-listed stock"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Something went wrong verifying the requested stock "
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
            return JSONResponse(status_code=500,
                                content={"message": f"Something went wrong fetching the market data for {symbol}"})
