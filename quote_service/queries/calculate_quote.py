from decimal import Decimal
from sqlalchemy import alias, func, case

from quote_service.errors import UnsupportedActionError, UnsupportedAmountError
from quote_service.extensions import db
from quote_service.models.orders import Orders


def calculate_quote(pair_id: int, action: str, amount: Decimal,
                    is_inverted: bool):
    Orders.insert_orders(pair_id)

    orders_1 = alias(Orders)
    orders_2 = alias(Orders)

    if (action == 'buy' and not is_inverted) or (action == 'sell' and is_inverted):
        side = 'ask'
        cumulative_filter = orders_1.c.price >= orders_2.c.price
        cumulative_sorting = orders_1.c.price.asc()
        price_sorting = Orders.price.asc()
    elif (action == 'sell' and not is_inverted) or (action == 'buy' and is_inverted):
        side = 'bid'
        cumulative_filter = orders_1.c.price <= orders_2.c.price
        cumulative_sorting = orders_1.c.price.desc()
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
            .group_by(orders_1.c.price)
            .subquery()
    )
    _, max_inverted, max_ = db.session.query(subquery).order_by(subquery.c.size.desc()).first()

    if is_inverted:
        if amount > max_inverted:
            raise UnsupportedAmountError(max_inverted)
        cumulative_size = subquery.c.inverse_size
        size = Orders.inverse_size
        multiplier = 1 / Orders.price
    else:
        if amount > max_:
            raise UnsupportedAmountError(max_)
        cumulative_size = subquery.c.size
        size = Orders.size
        multiplier = Orders.price

    price = (
        db.session.query(
            func.sum(
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
            ) / amount
        )
            .select_from(Orders)
            .join(subquery, subquery.c.price == Orders.price)
            .filter(Orders.side == side)
            .filter(cumulative_size - amount < size)
            .order_by(price_sorting)
            .scalar()
    )
    return price
