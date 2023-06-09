from enum import Enum
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from helper.symbol_helper import MarketState, fetch_market_state, verify_symbol


class MarketStateResponse(BaseModel):
    marketState: str


router = APIRouter(prefix="/api/stocks", tags=["stocks"])


@router.get("/market-state/{symbol}")
async def get_market_state(symbol: str):
    try:
        verify_symbol(symbol)
        market_state: MarketState = fetch_market_state(symbol)
        return MarketStateResponse(marketState=market_state.value)
    except AttributeError:
        return JSONResponse(
            content={"message": f"'{symbol}' is not a valid NASDAQ-listed stock"},
            status_code=400,
        )
    except Exception as e:
        return JSONResponse(
            content={
                "message": f"Something went wrong fetching the market data for {symbol}: {str(e)}"
            },
            status_code=500,
        )
