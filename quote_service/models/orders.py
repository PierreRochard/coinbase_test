from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, UniqueConstraint

from ..extensions import db

from .currency_pairs import CurrencyPairs


class Orders(db.Model):
    """
        price: in quote_currency of pair_id
        size: quantity of base_currency
        side: 'bid' or 'ask'
    """

    __tablename__ = 'orders'
    __table_args__ = (
        UniqueConstraint('price',
                         'pair_id',
                         name='orders_unique_constraint'),
    )

    id = Column(Integer, primary_key=True)
    price = Column(Numeric)
    size = Column(Numeric)
    side = Column(String)

    pair_id = Column(Integer,
                     ForeignKey(CurrencyPairs.id),
                     nullable=False)
