# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-23
import random

market_items = [
    [('GUSD', 'USDT'), ('BTC', 'USDT'), ('TRX', 'USDT'), ('BAT', 'USDT'), ('ADA', 'USDT'), ('XUC', 'USDT'),
     ('ZEC', 'USDT'), ('LTC', 'USDT'), ('ETC', 'USDT'), ('LSK', 'USDT')],
    [('EOS', 'USDT'), ('ETH', 'USDT'), ('BTC', 'USDT'), ('TRX', 'USDT'), ('XLM', 'USDT'), ('LSK', 'USDT')],
    [('ADA', 'USDT'), ('XLM', 'USDT'), ('ETH', 'USDT'), ('GUSD', 'USDT')],
    [('ETC', 'USDT'), ('XLM', 'USDT'), ('VET', 'USDT'), ('LSK', 'USDT'), ('XUC', 'USDT'), ('BCH', 'USDT')],
    [('BNB', 'USDT'), ('EOS', 'USDT'), ('TRX', 'USDT'), ('LTC', 'USDT'), ('BCN', 'USDT'), ('ETH', 'USDT'),
     ('ADA', 'USDT'), ('BTC', 'USDT')],
    [('XLM', 'USDT'), ('BTC', 'USDT'), ('XUC', 'USDT'), ('ETC', 'USDT'), ('XLM', 'USDT'), ('ETH', 'USDT'),
     ('GUSD', 'USDT'), ('XLM', 'USDT'), ('HT', 'USDT'), ('ZEC', 'USDT'), ('XRP', 'USDT'), ('LTC', 'USDT'),
     ('VET', 'USDT'), ('BAT', 'USDT'), ('BNB', 'USDT')],
    [('TRX', 'USDT'), ('LSK', 'USDT'), ('ZEC', 'USDT')],
    [('BCH', 'USDT')],
    [('BCH', 'USDT'), ('EOS', 'USDT')],
    [('ETC', 'USDT'), ('BTC', 'USDT'), ('BAT', 'USDT'), ('HT', 'USDT'), ('TRX', 'USDT'), ('XLM', 'USDT'), (
        'EOS', 'USDT'), ('XUC', 'USDT'), ('ADA', 'USDT'), ('BCH', 'USDT'), ('ETH', 'USDT'), ('GUSD', 'USDT')],
    [('VET', 'USDT'), ('HT', 'USDT'), ('LSK', 'USDT'), ('EOS', 'USDT'), ('XRP', 'USDT'), ('BTC', 'USDT'),
     ('BCH', 'USDT'), ('ETC', 'USDT'), ('TRX', 'USDT'), ('BCN', 'USDT'), ('ZEC', 'USDT'), ('ETH', 'USDT'),
     ('LTC', 'USDT'), ('GUSD', 'USDT')],
    [('BNB', 'USDT'), ('ZEC', 'USDT'), ('BAT', 'USDT'), ('HT', 'USDT'), ('VET', 'USDT'), ('EOS', 'USDT'),
     ('XRP', 'USDT'), ('ETH', 'USDT'), ('GUSD', 'USDT'), ('BTC', 'USDT'), ('LSK', 'USDT'), ('XUC', 'USDT'),
     ('LTC', 'USDT'), ('ETC', 'USDT'), ('BCH', 'USDT'), ('BCN', 'USDT'), ('XLM', 'USDT')],
    [('EOS', 'USDT'), ('BTC', 'USDT'), ('ETH', 'USDT'), ('BNB', 'USDT')],
    [('BNB', 'USDT'), ('XLM', 'USDT'), ('ETH', 'USDT')],
    [('BCH', 'USDT'), ('VET', 'USDT'), ('TRX', 'USDT'), ('ZEC', 'USDT'), ('LSK', 'USDT')],
    [('TRX', 'USDT'), ('BCN', 'USDT'), ('GUSD', 'USDT')],
    [('ETC', 'USDT'), ('XUC', 'USDT')],
    [('HT', 'USDT')],
    [('VET', 'USDT'), ('XUC', 'USDT'), ('LTC', 'USDT'), ('XRP', 'USDT')],
    [('BCN', 'USDT'), ('GUSD', 'USDT'), ('XUC', 'USDT'), ('HT', 'USDT'), ('ZEC', 'USDT'), ('XRP', 'USDT'),
     ('ETH', 'USDT'), ('XLM', 'USDT'), ('ADA', 'USDT')],
]

COINS = (
    "USDT", "BTC", "XRP", "ETH", "BCH", "XLM", "EOS", "LTC", "TRX", "BNB", "HT", "ETC", "ADA", "VET", "BAT", "LSK",
    "ZEC", "XUC", "BCN", "GUSD")


def rand_markets(num):
    markets = list()
    if num > len(COINS[1:]):
        assert "Market num is too large"
    while True:
        market = (random.choice(COINS[1:]), "USDT")
        if market not in markets:
            markets.append(market)
        if len(markets) >= num:
            break
    return markets
