from pydantic import BaseModel, validator


class Asset(BaseModel):
    symbol: str
    name: str
    position: int
    amountInvested: float
    averagePrice: float
    userId: str


class BuyAssetInput(BaseModel):
    name: str
    symbol: str
    position: int
    amountInvested: float

    @validator('name')
    def name_required(cls, v):
        if v is None:
            raise ValueError('The stock name is required')
        return v

    @validator('symbol')
    def symbol_required(cls, v):
        if v is None:
            raise ValueError('The stock symbol/ticker is required')
        return v

    @validator('position')
    def position_required(cls, v):
        if v is None:
            raise ValueError('The purchase position is required')
        return v

    @validator('amountInvested')
    def amount_invested_required(cls, v):
        if v is None:
            raise ValueError('The amount invested is required')
        return v
