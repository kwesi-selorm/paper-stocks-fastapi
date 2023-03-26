from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Body
from starlette import status

from auth.jwt_fns import verify_access_token
from helper.symbol_helper import verify_symbol
from model.AssetModel import BuyAssetInput, Asset
from router.user_router import ReturnedAsset
from service.AssetService import AssetService
from service.UserService import UserService

user_service = UserService()
asset_service = AssetService()

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.post("/buy-asset/{user_id}", dependencies=[Depends(verify_access_token)], status_code=status.HTTP_201_CREATED)
async def buy_asset(user_id: str, buy_asset_input: Annotated[BuyAssetInput, Body(required=True)]):
    symbol = buy_asset_input.dict().get("symbol")
    name = buy_asset_input.dict().get("name")
    new_position = buy_asset_input.dict().get("position")
    new_amount_invested = buy_asset_input.dict().get("amountInvested")

    user_doc = user_service.find_by_id(user_id)

    verify_symbol(symbol)
    remaining_buying_power = user_doc.get("buyingPower") - new_amount_invested
    already_owned_asset = asset_service.find_by_user_id_and_symbol(user_id, symbol)

    if already_owned_asset is None:
        asset_dict = {"symbol": symbol, "name": name, "position": new_position, "amountInvested": new_amount_invested,
                      "averagePrice": new_amount_invested / new_position, "userId": user_id}
        new_asset = Asset(**asset_dict)

        try:
            asset_service.save_new(new_asset)
            user_service.update_on_buy(user_id, {"buyingPower": remaining_buying_power})
            return new_asset
        except Exception as e:
            raise HTTPException(status_code=500, detail={"message": "Error completing the transaction" + str(e)})

    else:
        asset_id = already_owned_asset.get("_id")
        old_position = already_owned_asset.get("position")
        old_amount_invested = already_owned_asset.get("amountInvested")
        update = asset_service.find_position_and_average_on_buy(
            old_position, old_amount_invested, new_position, new_amount_invested)

        try:
            updated_asset = asset_service.update_on_buy(asset_id, update)
            user_service.update_on_buy(user_id, {"buyingPower": remaining_buying_power})
            return ReturnedAsset(symbol=updated_asset.get("symbol"), position=updated_asset.get("position"))
        except Exception as e:
            raise HTTPException(status_code=500, detail={"message": "Error completing the transaction" + str(e)})
