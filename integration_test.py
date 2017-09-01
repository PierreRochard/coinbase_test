from pprint import pformat

import requests

test_url = 'http://127.0.0.1:5000/'

req_payloads = [
    {
        'action': 'buy',
        'base_currency': 'BTC',
        'quote_currency': 'USD',
        'amount': '5000000000'
    },
    # {
    #     'action': 'buy',
    #     'base_currency': 'USD',
    #     'quote_currency': 'BTC',
    #     'amount': '50.00000000'
    # },
    # {
    #     'action': 'sell',
    #     'base_currency': 'BTC',
    #     'quote_currency': 'USD',
    #     'amount': '50.00000000'
    # }
]

for payload in req_payloads:
    response = requests.post(test_url, json=payload)
    print(pformat(payload))
    print(response.status_code)
    print(pformat(response.text))
    print(pformat(response.json()))
