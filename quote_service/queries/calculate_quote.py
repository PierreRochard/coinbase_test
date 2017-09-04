from decimal import Decimal

from sqlalchemy import alias, case, func

from quote_service.errors import UnsupportedActionError, UnsupportedAmountError
from quote_service.extensions import db
from quote_service.models.orders import Orders


def calculate_quote(pair_id: int, action: str, amount: Decimal,
                    is_inverted: bool):
    """
    :param pair_id: the ID of the currency pair
    :param action: Buy or Sell
    :param amount: base currency amount to be bought or sold
    :param is_inverted: flag for when a quote is needed for reverse of pair_id's base and quote currencies
    :return: The weighted average price at which the market order would be executed
    """
    Orders.insert_orders(pair_id)

    orders_1 = alias(Orders)
    orders_2 = alias(Orders)

    # Setup subquery params based on what side of the order book we are querying
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

    # Subquery to calculate the cumulative size by price
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
    # Check if the requested amount exceeds the Level 2 order book's capacity
    # and set up params the price query
    _, max_inverted, max_ = db.session.query(subquery).order_by(subquery.c.size.desc()).first()
    if is_inverted:
        if amount > max_inverted:
            raise UnsupportedAmountError(max_inverted)
        cumulative_size = subquery.c.inverse_size
        size = Orders.inverse_size
        multiplier = 1.0 / Orders.price
    else:
        if amount > max_:
            raise UnsupportedAmountError(max_)
        cumulative_size = subquery.c.size
        size = Orders.size
        multiplier = Orders.price

    # Query joins the cumulative price subquery and uses a case statement to
    # determine how much of each order layer to consume
    # Total consumed is then divided by the ordered amount to determine WA price
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
    Orders.delete_orders()
    return price
