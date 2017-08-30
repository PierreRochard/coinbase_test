import requests


class ExchangeService(object):
    api_url = 'https://api.gdax.com/'

    @classmethod
    def get_pairs(cls):
        get_url = cls.api_url + 'products'
        products = requests.get(get_url).json()
        pairs = [{'base_currency': p['base_currency'],
                  'quote_currency': p['quote_currency']} for p in products]
        return pairs

    def get_orders(self, base_currency: str, quote_currency: str):
        get_url = self.api_url + f'products/{base_currency}-{quote_currency}/book?level=2'
        order_book = requests.get(get_url).json()
        orders = []
        for side in ['bids', 'asks']:
            side_orders = [{'price': price, 'size': size, 'side': side[0:3]}
                           for price, size, _ in order_book[side]]
            orders.extend(side_orders)
        return orders
