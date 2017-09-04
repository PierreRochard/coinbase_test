from pprint import pformat

import pytest
import requests

test_url = 'http://127.0.0.1:5000/'


def payload_fixture(action, base, quote, amount):
    return {
        'action': action,
        'base_currency': base,
        'quote_currency': quote,
        'amount': amount
    }

test_cases = [
    # Simple case of taking out one order
    # ('buy', 'BTC', 'USD', '50', '2500.00', '125000.00'),
    # ('sell', 'BTC', 'USD', '50', '2000.00', '100000.00'),
    # Taking out one and a half orders
    ('buy', 'BTC', 'USD', '75', '2500.00', '125000.00'),
    ('sell', 'BTC', 'USD', '75', '2000.00', '100000.00'),

]
params = 'action,base,quote,amount,expected_price,expected_total'

class TestQuoteService(object):
    @pytest.mark.parametrize(params, test_cases)
    def test_buy_sell(self, action, base, quote, amount, expected_price,
                      expected_total):
        payload = payload_fixture(action, base, quote, amount)
        response = requests.post(test_url, json=payload)
        response_data = response.json()

        print(pformat(payload))
        print(pformat(response.json()))

        # assert response_data['currency'] == quote
        # assert response_data['price'] == expected_price
        # assert response_data['total'] == expected_total
