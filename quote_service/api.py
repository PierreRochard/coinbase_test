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
        req_amount = args['amount']
        req_base_currency = args['base_currency']
        req_quote_currency = args['quote_currency']

        pair_id, is_inverted = invert_pair(req_base_currency,
                                           req_quote_currency)



        price, total = calculate_quote(pair_id, req_action, req_amount)

        return dict(price='', total='', currency=req_quote_currency), 200
