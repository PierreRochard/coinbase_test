from decimal import Decimal
from sqlalchemy import alias, func, case

from quote_service.errors import UnsupportedActionError
from quote_service.extensions import db
from quote_service.models.orders import Orders


def calculate_quote(pair_id: int, action: str, amount: Decimal,
                    is_inverted: bool):
    Orders.insert_orders(pair_id)

    orders_1 = alias(Orders)
    orders_2 = alias(Orders)

    if action == 'buy':
        side = 'ask'
        cumulative_filter = orders_1.c.price >= orders_2.c.price
        cumulative_sorting = orders_2.c.price.asc()
        price_sorting = Orders.price.asc()
    elif action == 'sell':
        side = 'bid'
        cumulative_filter = orders_1.c.price <= orders_2.c.price
        cumulative_sorting = orders_2.c.price.desc()
        price_sorting = Orders.price.desc()
    else:
        raise UnsupportedActionError()

    subquery = (
        db.session.query(orders_1.c.price.label('price'),
                         func.sum(orders_2.c.size * orders_2.c.price).label('inverse_size'),
                         func.sum(orders_2.c.size).label('size'))
            .filter(cumulative_filter)
            .filter(orders_2.c.side == side)
            .filter(orders_2.c.pair_id == pair_id)
            .order_by(cumulative_sorting)
            .group_by(orders_1.c.price, orders_1.c.size)
            .subquery()
    )

    if is_inverted:
        cumulative_size = subquery.c.inverse_size
        size = Orders.inverse_size
        multiplier = Orders.size
    else:
        cumulative_size = subquery.c.size
        size = Orders.size
        multiplier = Orders.price

    price = (
        db.session.query(
            # func.sum(
                case(
                    [
                        (
                            cumulative_size - amount <= 0,
                            size
                        ),
                        (
                            cumulative_size - amount > 0,
                            size - cumulative_size + amount
                        )
                    ],
                    else_=0)
                * multiplier
            # ) / amount
        )
            .join(subquery,
                  subquery.c.price == Orders.price)
            .filter(Orders.side == side)
            .filter(cumulative_size - amount < size)
            .order_by(price_sorting)
            .scalar()
    )
    # Orders.delete_orders()
    return price
