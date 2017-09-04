import os
import requests

from quote_service.exchange_service_fixtures import mock_orders, mock_pairs


class ExchangeService(object):
    api_url = 'https://api.gdax.com/'

    @classmethod
    def get_pairs(cls):

        if os.environ.get('LOCAL_DEV', None):
            return mock_pairs

        get_url = cls.api_url + 'products'
        products = requests.get(get_url).json()
        pairs = [{'base_currency': p['base_currency'],
                  'quote_currency': p['quote_currency']} for p in products]
        return pairs

    @classmethod
    def get_orders(cls, base_currency: str, quote_currency: str):

        if os.environ.get('LOCAL_DEV', None):
            return mock_orders

        path = f'products/{base_currency}-{quote_currency}/book?level=2'
        get_url = cls.api_url + path
        order_book = requests.get(get_url).json()
        orders = []
        for side in ['bids', 'asks']:
            side_orders = [{'price': price, 'size': size, 'side': side[0:3]}
                           for price, size, _ in order_book[side]]
            orders.extend(side_orders)
        return orders
