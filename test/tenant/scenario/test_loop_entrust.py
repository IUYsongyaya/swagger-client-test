# -*- coding: utf-8 -*-
# @File :  test_loop_entrust.py
# @Author : lh
import time
import pytest
import logging
import random

from test.tenant.main import Main
from test.tenant.tenant import Tenant
from test.tenant.id_settings import *

logger = logging.getLogger('test_loop_entrust')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@pytest.fixture(scope="session")
def setup(request):
    _main = Main(CONFIG.MAIN_INDEX)
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    markets = _tenant.list_markets()
    _main.free_charge(8, 100000000000)
    _main.free_charge(417, 100000000000)
    assert markets, "No markets!"
    print("market:", markets[0])
    market_id = markets[0].id
    precision = int(_main.get_market_details(market_id=market_id).price_places)
    trading_pair = markets[0].trading_pair
    print(_tenant.get_market_details(market_id=market_id))
    
    def finalize():
        time.sleep(5)
        orders = _main.get_orders(status=["entrusting"])
        for i in orders:
            logger.error(f"canceling: {i}")
            try:
                _main.withdraw(i.order_id)
            except Exception as e:
                logger.error(e)
        else:
            print("No entrusting orders")
        
        orders = _main.get_orders(status=["entrusting"])
        for i in orders:
            logger.error(f"cancel failed: {i}")
        else:
            print("No entrusting orders")
            
    request.addfinalizer(finalize)
    
    return _main, market_id, trading_pair, precision


def get_random_price_and_volume(precision=2, price_start=100, volume_start=1):
    price_range = (price_start+100, price_start*100)
    volume_range = (volume_start+100, volume_start*100)
    if precision:
        return round(random.uniform(*price_range), int(precision)), round(random.uniform(*volume_range), 8-int(precision))
    else:
        return int(random.uniform(*price_range)), int(random.uniform(*volume_range))
    

def test_1_min_trading(setup):
    _main, market_id, pair_name, precision = setup
    start_st = time.time()
    while True:
        if time.time() - start_st > 10:
            print("10 second, done!")
            break
        price, volume = get_random_price_and_volume(precision=precision)
        trade_type = random.choice(["buy", "sell"])
        if trade_type == "buy":
            print("buy ===> price:%u, volume:%u" % (price, volume))
            first_result = _main.buy(market_id, price, volume)
        elif trade_type == "sell":
            print("sell ===> price:%u, volume:%u" % (price, volume))
            first_result = _main.sell(market_id, price, volume)
            logger.info(f"{trade_type} id: {first_result.order_id}")
        else:
            assert 0, "Invalid trade type:%s" % trade_type
        print('第一次下单result:', first_result)
        if trade_type == 'buy':
            buy_id = first_result.order_id
            print("buy ===> price:%u, volume:%u" % (price, volume))
            result = _main.sell(market_id, price, volume)
            print('第二次下买单:', result)
            sell_id = result.order_id
            logger.info(f"sell id :{sell_id}")
        else:
            sell_id = first_result.order_id
            print('*' * 20)
            print("sell ===> price:%u, volume:%u" % (price, volume))
            result = _main.buy(market_id, price, volume)
            print('第二次下买单:', result)
            buy_id = result.order_id
            logger.info(f"buy id: {buy_id}")
        # time.sleep(2)
        result_sell = _main.get_trades(order_id=sell_id, pair=pair_name)
        logger.info(f"get result sell trades: {result_sell}")
        result_buy = _main.get_trades(order_id=buy_id, pair=pair_name)
        logger.info(f"get result buy trades:  {result_buy}")
