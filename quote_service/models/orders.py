from sqlite3 import IntegrityError

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, \
    UniqueConstraint

from quote_service.exchange_service import ExchangeService
from quote_service.extensions import db

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

    @classmethod
    def insert_orders(cls, pair_id):
        """
        Retrieves limit orders from GDAX and inserts them into the orders table.
        """
        base, quote = (
            db.session.query(CurrencyPairs.base_currency,
                             CurrencyPairs.quote_currency)
            .filter(CurrencyPairs.id == pair_id)
                .one()
        )
        orders = ExchangeService.get_orders(base, quote)
        for order in orders:
            new_order_record = cls(**order)
            new_order_record.pair_id = pair_id
            db.session.add(new_order_record)
            try:
                db.session.commit()
            except IntegrityError:
                continue

    @classmethod
    def delete_orders(cls):
        db.session.query(cls).delete()
        db.session.commit()
