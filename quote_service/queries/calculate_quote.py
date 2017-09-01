from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from quote_service.errors import UnsupportedActionError
from quote_service.extensions import db
from quote_service.models.currency_pairs import CurrencyPairs
from quote_service.models.orders import Orders


def calculate_quote(pair_id, action, amount):
    Orders.insert_orders(pair_id)
    if action == 'buy':
        side = 'ask'
    elif action == 'sell':
        side = 'bid'
    else:
        raise UnsupportedActionError()

    # SELECT p1.ID, p1.ProductName, p1.Price,
    # (SELECT SUM(p2.Price) FROM Products p2 WHERE p1.ID >= p2.ID  ORDER BY p2.ID ) as RunningTotal
    # FROM Products p1
    # WHERE RunningTotal <= 5
    # ORDER BY p1.ID

    # Orders.delete_orders()
    return 0, 0
