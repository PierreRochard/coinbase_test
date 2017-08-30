from flask_restful import Resource, reqparse


class QuoteService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str)
        parser.add_argument('base_currency', type=str)
        parser.add_argument('quote_currency', type=str)
        parser.add_argument('amount', type=str)
        args = parser.parse_args()

        return dict(price='', total='', currency=args['quote_currency']), 200
