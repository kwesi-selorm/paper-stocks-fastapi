from pydantic import BaseModel


class Asset(BaseModel):
    symbol: str
    name: str
    position: int
    amountInvested: float
    averagePrice: float
    userId: str
    marketPrice: float
