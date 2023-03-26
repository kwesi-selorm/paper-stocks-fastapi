import yfinance as yf
from fastapi import HTTPException


def verify_symbol(symbol):
    try:
        ticker = yf.Ticker(symbol)
        print(ticker.info.get("symbol"))
    except AttributeError:
        raise HTTPException(status_code=400, detail={"message": f"'{symbol}' is not a valid NASDAQ-listed stock"})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message": f"Something went wrong verifying the requested stock "
                                                                "symbol: " + str(e)})
