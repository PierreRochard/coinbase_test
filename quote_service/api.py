import decimal
from flask_restful import Resource, reqparse

from quote_service.errors import UnsupportedAmountError
from quote_service.queries.calculate_quote import calculate_quote
from quote_service.queries.invert_pair import invert_pair
from quote_service.utilities import get_rounding


class QuoteService(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True, trim=True)
        parser.add_argument('action', type=str, required=True,
                            choices=('buy', 'sell'),
                            help='Action must be "buy" or "sell"')
        parser.add_argument('amount', type=str, required=True)
        parser.add_argument('base_currency', type=str, required=True)
        parser.add_argument('quote_currency', type=str, required=True)

        args = parser.parse_args()
        req_action = args['action']
        amount_error = dict(message={
            'amount': 'Amount must be a number and greater than zero'}), 400
        try:
            req_amount = decimal.Decimal(args['amount'])
        except decimal.InvalidOperation:
            return amount_error

        if req_amount <= 0:
            return amount_error

        req_base_currency = args['base_currency']
        req_quote_currency = args['quote_currency']
        base_rounding = get_rounding(req_base_currency)
        quote_rounding = get_rounding(req_quote_currency)

        pair_id, is_inverted = invert_pair(req_base_currency,
                                           req_quote_currency)

        try:
            price = calculate_quote(pair_id, req_action, req_amount, is_inverted)
        except UnsupportedAmountError as e:
            max_amount = round(e.max_amount, base_rounding)
            return dict(message={'amount': f'Amount must be less than {max_amount}'}), 400

        total = price * req_amount

        price = str(round(price, quote_rounding))
        total = str(round(total, quote_rounding))
        return dict(price=price,
                    total=total,
                    currency=req_quote_currency), 200
