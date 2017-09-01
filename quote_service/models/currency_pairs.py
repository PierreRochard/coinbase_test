from sqlalchemy import Column, Integer, String, UniqueConstraint

from quote_service.exchange_service import ExchangeService
from quote_service.extensions import db


class CurrencyPairs(db.Model):
    """
        [base_currency]-[quote_currency]

        base_currency: The currency to be bought or sold
        quote_currency: The currency to quote the price in

    """
    __tablename__ = 'currency_pairs'
    __table_args__ = (
        UniqueConstraint('base_currency',
                         'quote_currency',
                         name='pairs_unique_constraint'),
    )

    id = Column(Integer, primary_key=True)

    base_currency = Column(String, nullable=False)
    quote_currency = Column(String, nullable=False)

    @staticmethod
    def insert_pairs():
        """
        Retrieves the currency pairs (aka products) from GDAX and inserts them
        into the currency_pairs table.
        """
        currency_pairs = ExchangeService.get_pairs()
        for currency_pair in currency_pairs:
            new_currency_pair_record = CurrencyPairs(**currency_pair)
            db.session.add(new_currency_pair_record)
            db.session.commit()
