from typing import Any

from bson import ObjectId
from pymongo import ReturnDocument

from config.DatabaseConfig import DatabaseConfig
from model.AssetModel import Asset

assets_collection = DatabaseConfig().get_collection("assets")


class AssetService:
    def __init__(self, symbol: str | None = None, name: str | None = None, position: int | None = None,
                 amount_invested: float | None = None,
                 average_price: float | None = None,
                 user_id: str = None):
        self.symbol = symbol
        self.name = name
        self.position = position
        self.amount_invested = amount_invested
        self.average_price = average_price
        self.user_id = user_id

    @staticmethod
    def save_new(asset: Asset):
        assets_collection.insert_one(asset.dict())

    @staticmethod
    def update_on_buy(asset_id: str, update: dict[str, Any]):
        return assets_collection.find_one_and_update(
            {"_id": ObjectId(asset_id)},
            {"$set": update},
            return_document=ReturnDocument.AFTER)

    @staticmethod
    def find_by_user_id_and_symbol(user_id: str, symbol: str):
        return assets_collection.find_one({'userId': user_id, 'symbol': symbol})

    @staticmethod
    def find_position_and_average_on_buy(old_position: int, old_amount_invested: float, new_position: int,
                                         new_amount_invested: float):
        total_position = old_position + new_position
        total_amount_invested = old_amount_invested + new_amount_invested
        average_price = total_amount_invested / total_position
        return {"position": total_position, "averagePrice": average_price}

    @staticmethod
    def find_position_and_average_on_sell(old_position: int, old_average_price: float, positions_sold: int,
                                          unit_price: float):
        cost_basis = positions_sold * old_average_price
        net_proceeds = positions_sold * unit_price
        gain_or_loss = net_proceeds - cost_basis
        remaining_position = old_position - positions_sold
        return {remaining_position, gain_or_loss}

    @staticmethod
    def find_by_user_id(user_id: str):
        asset_docs = assets_collection.find({'userId': user_id})
        return asset_docs
