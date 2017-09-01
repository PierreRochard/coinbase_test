from decimal import Decimal
from sqlalchemy import alias, func, case

from quote_service.errors import UnsupportedActionError
from quote_service.extensions import db
from quote_service.models.orders import Orders


def calculate_quote(pair_id: int, action: str, amount: Decimal):
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

    cumulative_subquery = (
        db.session.query(orders_1.c.price.label('price'),
                         orders_1.c.size.label('size'),
                         func.sum(orders_2.c.size).label('cumulative_size'))
            .filter(cumulative_filter)
            .filter(orders_2.c.side == side)
            .filter(orders_2.c.pair_id == pair_id)
            .order_by(cumulative_sorting)
            .group_by(orders_1.c.price, orders_1.c.size)
            .subquery()
    )

    price = (
        db.session.query(
            func.sum(
                case(
                    [
                        (cumulative_subquery.c.cumulative_size - amount <= 0,
                         Orders.size),
                        (cumulative_subquery.c.cumulative_size - amount > 0,
                         Orders.size - cumulative_subquery.c.cumulative_size + amount)
                    ],
                    else_=0)
                * Orders.price
            ) / amount
        )
            .join(cumulative_subquery,
                  cumulative_subquery.c.price == Orders.price)
            .filter(Orders.side == side)
            .filter(cumulative_subquery.c.cumulative_size - amount < Orders.size)
            .order_by(price_sorting)
            .scalar()
    )
    Orders.delete_orders()
    return price
