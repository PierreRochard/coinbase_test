from mock import MagicMock, patch as mock_patch
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

test_data = [
    ('buy', 'BTC', 'USD', '50'),
    ('sell', 'BTC', 'USD', '50'),
]


class TestQuoteService(object):

    @pytest.mark.parametrize('action,base,quote,amount', test_data)
    def test_buy_sell(self, action, base, quote, amount):
        with mock_patch('coinbase_test.exchange_service.ExchangeService') as MockExchangeService:
            MockExchangeService.get_orders.return_value = mock_account
            mock_account.owns = MagicMock(return_value=expected_value)
            assert bool(auth(request, response, 'cb6847c45b4411e2bf0612313930ed44')) == expected_value

    payload = payload_fixture(action, base, quote, amount)
        api_response = requests.post(test_url, json=payload)

        cb_response =
        print(pformat(payload))
        print(response.status_code)
        print(pformat(response.text))
        print(pformat(response.json()))



req_payloads = [
    {
        'action': 'buy',
        'base_currency': 'BTC',
        'quote_currency': 'USD',
        'amount': '50'
    },
    {
        'action': 'buy',
        'base_currency': 'USD',
        'quote_currency': 'BTC',
        'amount': '50000.00'
    },
    {
        'action': 'sell',
        'base_currency': 'USD',
        'quote_currency': 'BTC',
        'amount': '50000000.00'
    },
    {
        'action': 'sell',
        'base_currency': 'BTC',
        'quote_currency': 'USD',
        'amount': '50.00000000'
    },
    {
        'action': 'sell',
        'base_currency': 'BTC',
        'quote_currency': 'USD',
        'amount': '50.00000000'
    }
]

# for payload in req_payloads:
#     response = requests.post(test_url, json=payload)
#     print(pformat(payload))
#     print(response.status_code)
#     print(pformat(response.text))
#     print(pformat(response.json()))
