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

buy_sell_test_cases = [
    # # Simple case of taking out one order
    ('buy', 'BTC', 'USD', '50', '2500.00', '125000.00'),
    ('sell', 'BTC', 'USD', '50', '2000.00', '100000.00'),
    # # Taking out one and a half orders
    ('buy', 'BTC', 'USD', '75', '2666.67', '200000.00'),
    ('sell', 'BTC', 'USD', '75', '1833.33', '137500.00'),
    # Inverted
    # Todo: fix SQLite float imprecision by using PostgreSQL or int multiplication
    ('buy', 'USD', 'BTC', '137500.00', '0.00054545', '74.99999375'),
    ('sell', 'USD', 'BTC', '200000.00', '0.00037500', '75.00000000'),

]
buy_sell_params = 'action,base,quote,amount,expected_price,expected_total'


@pytest.mark.parametrize(buy_sell_params, buy_sell_test_cases)
def test_buy_sell(action, base, quote, amount, expected_price, expected_total):
    payload = payload_fixture(action, base, quote, amount)
    response = requests.post(test_url, json=payload)
    response_data = response.json()
    assert response_data['currency'] == quote
    assert response_data['price'] == expected_price
    assert response_data['total'] == expected_total


too_much_params = 'action,base,quote,amount,expected_message'
too_much_test_cases = [
    ('buy', 'BTC', 'USD', '151', 'Amount must be less than 150.00000000'),
    ('sell', 'BTC', 'USD', '151', 'Amount must be less than 150.00000000'),
    ('buy', 'USD', 'BTC', '225000.01', 'Amount must be less than 225000.00'),
    ('sell', 'USD', 'BTC', '450000.01', 'Amount must be less than 450000.00'),
]


@pytest.mark.parametrize(too_much_params, too_much_test_cases)
def test_buy_sell__too_much(action, base, quote, amount, expected_message):
    payload = payload_fixture(action, base, quote, amount)
    response = requests.post(test_url, json=payload)
    response_data = response.json()
    assert response_data['message']['amount'] == expected_message
