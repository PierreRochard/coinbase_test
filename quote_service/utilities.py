
cryptos = ['BTC', 'LTC', 'ETH']


def get_rounding(currency):
    if currency in cryptos:
        return 8
    else:
        return 2
