from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from quote_service.extensions import db
from quote_service.models.currency_pairs import CurrencyPairs


def invert_pair(req_base_currency: str, req_quote_currency: str):
    try:
        pair = (
            db.session.query(CurrencyPairs)
                .filter(and_(CurrencyPairs.base_currency == req_base_currency,
                             CurrencyPairs.quote_currency == req_quote_currency))
                .one()
        )
        return pair.id, False
    except NoResultFound:
        pair = (
            db.session.query(CurrencyPairs)
                .filter(and_(CurrencyPairs.base_currency == req_quote_currency,
                             CurrencyPairs.quote_currency == req_base_currency))
                .one()
        )
        return pair.id, True
