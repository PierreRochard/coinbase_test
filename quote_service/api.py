from decimal import Decimal
from flask_restful import Resource, reqparse

from quote_service.queries.calculate_quote import calculate_quote
from quote_service.queries.invert_pair import invert_pair


class QuoteService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str)
        parser.add_argument('amount', type=str)
        parser.add_argument('base_currency', type=str)
        parser.add_argument('quote_currency', type=str)

        args = parser.parse_args()
        req_action = args['action']
        req_amount = Decimal(args['amount'])
        req_base_currency = args['base_currency']
        req_quote_currency = args['quote_currency']

        pair_id, is_inverted = invert_pair(req_base_currency,
                                           req_quote_currency)

        price = calculate_quote(pair_id, req_action, req_amount)

        if is_inverted:
            price = 1/price

        is_crypto = req_quote_currency in ['BTC', 'LTC', 'ETH']
        if is_crypto:
            rounding = 8
        else:
            rounding = 2

        total = price * req_amount

        price = str(round(price, rounding))
        total = str(round(total, rounding))
        return dict(price=price,
                    total=total,
                    currency=req_quote_currency), 200
