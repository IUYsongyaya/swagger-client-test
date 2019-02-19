# @author: lj
import random
import time
import pytest
import requests
import logging

from swagger_client.main.api.entrust_api import EntrustApi  # noqa: E501
from swagger_client.main.configuration import Configuration
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .data import (FIELDS, get_random_price_and_volume, test_data30,
                   test_data31, test_data32, test_data35, test_data33,
                   test_data36, test_data34, test_data37)

api = EntrustApi()
configuration = Configuration()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class TestFirstSellMultiDifferentPriceOneBuy:
    @pytest.mark.parametrize(FIELDS, [test_data30, test_data31])
    def test_multi_sell_volume_eq(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000000
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.volume = 1000000
        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        # 清空
        api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        api.entrusts_post(body=payload)

        # 恢复限价
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.volume = volume
        # 添加多笔买单和一笔卖单
        sell_trades = []
        sub_range = 1 / (10**int(special_info['precision']))
        payload.trade_type = 'sell'

        for i in range(5):
            payload.price, payload.volume = get_random_price_and_volume(special_info['precision'])
            r = api.entrusts_post(body=payload)
            sell_trades.append({
                'order_id': r.order_id,
                'price': payload.price,
                'volume': payload.volume
            })

        payload.trade_type = 'buy'
        if volume_flag == 'buy_price_eq_max_sell':
            # 买单与卖单最高价格一致
            sorted_sell_trades = sorted(sell_trades, key=lambda x: x['price'])
            payload.price = sorted_sell_trades[-1]['price']
        else:
            # 限价买单价格低于于卖单最低价格
            sorted_sell_trades = sorted(sell_trades, key=lambda x: x['price'])
            payload.price = round(sorted_sell_trades[0]['price'] - sub_range,
                                  int(special_info['precision']))
        # 卖单出售数量等于所有买单总数量
        payload.volume = round(
            sum([i['volume'] for i in sorted_sell_trades]), 8 - int(special_info['precision']))

        r = api.entrusts_post(body=payload)
        buy_entrust_id = r.order_id

        # print(f"{volume_flag}: {sorted_sell_trades}")
        time.sleep(5)

        total = []
        all_buy_id = [i['order_id'] for i in sell_trades]
        if volume_flag == 'buy_price_eq_max_sell':
            entrust_res = api.entrusts_get(trade_type="done")
            done_entrust_ids = [i.order_id for i in entrust_res.items]
            total = [float(i.volume) for i in entrust_res.items if i.order_id in all_buy_id]
            assert buy_entrust_id in done_entrust_ids

        result = api.trades_get()
        logger.info(sum([float(i.volume) for i in result.items]))
        done_trade_ids = [i.order_id for i in result.items]

        if volume_flag == 'buy_price_eq_max_sell':
            #  买卖单应都成交了
            assert buy_entrust_id in done_trade_ids
            assert payload.volume == round(sum(total), 8 - int(special_info['precision']))
            assert len(
                set(done_trade_ids) -
                set([i['order_id'] for i in sorted_sell_trades])) >= 0
        else:
            # 买卖单都剩余,测试剩余单撤销
            # print(f"payload: {payload}")
            # print(f"done_trade_ids: {done_trade_ids}")
            # print(f"buy_entrust_id: {buy_entrust_id}")
            # print(f"{sorted_sell_trades}")
            ids = [i['order_id'] for i in sorted_sell_trades]
            for i in ids + [buy_entrust_id]:
                print(f"canceling {i}")
                api.entrusts_id_cancel_post(i)

    @pytest.mark.parametrize(FIELDS, [test_data32, test_data35])
    def test_multi_sell_volume_eq_buy(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000000
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.volume = 1000000
        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        # 清空
        api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        api.entrusts_post(body=payload)

        # 恢复限价
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.volume = volume
        # 添加多笔卖单和一笔买单
        sell_trades = []
        payload.trade_type = 'sell'
        for i in range(5):
            payload.price, payload.volume = get_random_price_and_volume(special_info["precision"])
            r = api.entrusts_post(body=payload)
            sell_trades.append({
                'order_id': r.order_id,
                'price': payload.price,
                'volume': payload.volume
            })

        payload.trade_type = 'buy'
        if volume_flag == 'eq_buy_price':
            # 限价买单价格高于卖单最低价格,且低于卖单最高价格,且等于某一中间卖单价格
            sorted_sell_trades = sorted(sell_trades, key=lambda x: x['price'])
            payload.price = sorted_sell_trades[2]['price']
        else:
            # 限价买单价格高于卖单最低价格,且低于卖单最高价格,且不等于某一中间卖单价格
            sorted_sell_trades = sorted(sell_trades, key=lambda x: x['price'])
            payload.price = round((sorted_sell_trades[2]['price'] +
                                   sorted_sell_trades[3]['price']) / 2,
                                  int(special_info['precision']))

        # 买单购买数量等于,低于买单价格的所有卖单总数量
        payload.volume = round(
            sum([i['volume'] for i in sorted_sell_trades[:3]]), 8 - int(special_info['precision']))

        r = api.entrusts_post(body=payload)
        buy_trade_id = r.order_id
        time.sleep(10)

        # 买单应都成交了
        r = api.trades_get(order_id=buy_trade_id)
        assert r.items
        assert hasattr(r.items[0], 'volume')
        assert hasattr(r.items[0], 'fee')
        assert round(sum([float(i.volume) for i in r.items]), 8-int(special_info['precision'])) == float(
            payload.volume)
        # 卖单剩余,测试剩余单撤销
        ids = [i['order_id'] for i in sorted_sell_trades[3:]]
        for i in ids:
            api.entrusts_id_cancel_post(i)

    @pytest.mark.parametrize(FIELDS, [test_data33, test_data36])
    def test_multi_sell_volume_gt_buy(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000000
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.volume = 1000000
        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        # 清空
        api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        api.entrusts_post(body=payload)

        # 恢复限价
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.volume = volume
        # 添加多笔卖单和一笔买单
        buy_trades = []
        sub_range = 0.001
        payload.trade_type = 'sell'
        for i in range(5):
            payload.price, payload.volume = get_random_price_and_volume(special_info['precision'])
            r = api.entrusts_post(body=payload)
            buy_trades.append({
                'order_id': r.order_id,
                'price': payload.price,
                'volume': payload.volume
            })

        payload.trade_type = 'buy'
        if volume_flag == 'eq_sell_price':
            # 限价买单价格低于卖单最高价格,且高于卖单最低价格,且等于某一中间卖单价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            payload.price = sorted_buy_trades[2]['price']
        else:
            # 限价卖单价格低于买单最高价格,且高于买单最低价格,且等且不等于任何买单价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            sell_price = (sorted_buy_trades[2]['price'] +
                          sorted_buy_trades[3]['price']) / 2
            payload.price = round(sell_price, int(special_info['precision']))
        # 买单购买数量小于,低于买单价格的卖单总数量,均应以卖单价格成交[0～2]
        payload.volume = round(
            sum([i['volume'] for i in sorted_buy_trades[:3]]) - sub_range,
            8 - int(special_info['precision']))
        r = api.entrusts_post(body=payload)
        buy_trade_id = r.order_id

        time.sleep(3)
        # 买单应成交
        r = api.trades_get(order_id=buy_trade_id)
        assert hasattr(r.items[0], "volume")
        assert hasattr(r.items[0], "fee")
        assert round(sum([float(i.volume) for i in r.items]), 8-int(special_info['precision'])) == float(
            payload.volume)
        # 卖单剩余,测试剩余单撤销 index为2的卖单会剩余，所以从2开始算
        ids = [i['order_id'] for i in sorted_buy_trades[2:]]
        for i in ids:
            api.entrusts_id_cancel_post(i)

    @pytest.mark.parametrize(FIELDS, [test_data34, test_data37])
    def igtest_multi_sell_volume_lt_buy(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000_000
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.volume = 1000_000
        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        # 清空
        sell_clear_order = api.entrusts_post(body=payload)
        print(f"sell clear: {sell_clear_order}")
        payload.trade_type = 'buy'
        buy_clear_order = api.entrusts_post(body=payload)
        print(f"buy clear: {buy_clear_order}")

        # 恢复限价
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.volume = volume
        # 添加多笔卖单和一笔买单
        sell_trades = []
        inc_range = 20
        payload.trade_type = 'sell'
        for i in range(5):
            payload.price, payload.volume = get_random_price_and_volume(special_info['precision'])
            r = api.entrusts_post(body=payload)
            sell_trades.append({
                'order_id': r.order_id,
                'price': payload.price,
                'volume': payload.volume
            })

        payload.trade_type = 'buy'
        if volume_flag == 'eq_sell_price':
            # 买单价格高于卖单最低价格,且低于卖单最高价格,且等于某一中间卖单价格,
            sorted_sell_entrusts = sorted(sell_trades, key=lambda x: x['price'])
            payload.price = sorted_sell_entrusts[2]['price']
        else:
            # 买单价格高于卖单最低价格,且低于卖单最高价格,且不等于任何卖单价格
            sorted_sell_entrusts = sorted(sell_trades, key=lambda x: x['price'])
            sell_price = (sorted_sell_entrusts[2]['price'] +
                          sorted_sell_entrusts[3]['price']) / 2
            payload.price = round(sell_price, int(special_info['precision']))

        # 买单购买数量大于,低于买单价格的卖单总数量,均应以卖单价格成交,
        payload.volume = round(
            sum([i['volume'] for i in sorted_sell_entrusts[:3]]) + inc_range,
            8 - int(special_info['precision']))
        r = api.entrusts_post(body=payload)
        buy_trade_id = r.order_id
        time.sleep(5)

        entrust_res = api.entrusts_get(status=['done'])
        # 买单没有完全成交
        assert buy_trade_id not in [i.order_id for i in entrust_res.items]

        trades = api.trades_get(order_id=buy_trade_id)
        assert buy_trade_id in [i.order_id for i in trades.items]

        # 买卖单剩余,测试剩余单撤销
        for i in [i['order_id']
                  for i in sorted_sell_entrusts[3:]] + [buy_trade_id]:
            api.entrusts_id_cancel_post(i)
