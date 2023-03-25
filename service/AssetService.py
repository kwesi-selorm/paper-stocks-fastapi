from typing import Any, Mapping

from bson import ObjectId

from config.database_config import db
from model.AssetModel import Asset

assets_collection = db['assets']


class AssetService:
    def __init__(self, symbol: str, name: str, position: int, amount_invested: float, average_price: float,
                 user_id: str):
        self.symbol = symbol
        self.name = name
        self.position = position
        self.amount_invested = amount_invested
        self.average_price = average_price
        self.user_id = user_id
        pass

    @staticmethod
    def find_by_user_id_and_symbol(user_id: str, symbol: str):
        return assets_collection.find_one({'user_id': user_id, 'symbol': symbol})

    @staticmethod
    def find_position_and_average_on_buy(old_position: int, old_amount_invested: float, new_position: int,
                                         new_amount_invested: float):
        total_position = old_position + new_position
        total_amount_invested = old_amount_invested + new_amount_invested
        average_price = total_amount_invested / total_position
        return {total_position, average_price}

    @staticmethod
    def find_position_and_average_on_sell(old_position: int, old_average_price: float, positions_sold: int,
                                          unit_price: float):
        cost_basis = positions_sold * old_average_price
        net_proceeds = positions_sold * unit_price
        gain_or_loss = net_proceeds - cost_basis
        remaining_position = old_position - positions_sold
        return {remaining_position, gain_or_loss}
