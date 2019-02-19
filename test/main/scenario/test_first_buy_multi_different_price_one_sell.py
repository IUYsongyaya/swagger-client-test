# @author: lj
import time
import pytest

from swagger_client.main.api.entrust_api import EntrustApi  # noqa: E501
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .data import (FIELDS, get_random_price_and_volume, test_data22,
                   test_data23, test_data24, test_data27, test_data25,
                   test_data28, test_data26, test_data29)

api = EntrustApi()


class TestFirstBuyMultiDifferentPriceOneSell:
    @pytest.mark.parametrize(FIELDS, [test_data22, test_data23])
    def test_multi_sell_volume_eq(self, market_id, price, entrust_type,
                                  trade_type, volume, trigger_price,
                                  auto_cancel_at, volume_flag, special_login):

        payload = PostEntrustsRequest()
        payload.price = 1000_0
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        # payload.trigger_price = trigger_price
        payload.volume = 1000_0
        # payload.auto_cancel_at = auto_cancel_at
        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        # 清空

        before_market_buy = api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        before_makret_sell = api.entrusts_post(body=payload)
        # 恢复限价

        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.volume = volume

        # 添加多笔买单和一笔卖单
        buy_trades = []
        inc_range = 1
        for i in range(5):
            payload.trade_type = 'buy'
            payload.price, payload.volume = get_random_price_and_volume(special_info['precision'])
            r = api.entrusts_post(body=payload)
            buy_trades.append({
                'order_id': r.order_id,
                'price': payload.price,
                'volume': payload.volume
            })

        payload.trade_type = 'sell'
        if volume_flag == 'sell_price_eq_min_buy':
            # 卖单与买单最低价格一致
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            payload.price = sorted_buy_trades[0]['price']
            # 卖单出售数量等于所有买单总数量
        else:
            # 限价卖单价格高于买单最高价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            payload.price = sorted_buy_trades[-1]['price'] + inc_range
        # 卖单出售数量等于所有买单总数量
        payload.volume = round(
            sum([i['volume'] for i in sorted_buy_trades]), 8-int(special_info['precision']))

        r = api.entrusts_post(body=payload)
        sell_trade_id = r.order_id

        ids = [i['order_id'] for i in sorted_buy_trades]
        time.sleep(5)
        if volume_flag == 'sell_price_eq_min_buy':
            # 卖单应都成交了
            for i in sorted_buy_trades:
                result = api.trades_get(order_id=i['order_id'])
                assert result.items
                assert hasattr(result.items[0], 'volume')
                assert float(
                    result.items[0].volume) <= float(i['volume'])
        else:
            # 买卖单剩余,测试剩余单撤销
            for i in ids + [sell_trade_id]:
                api.entrusts_id_cancel_post(i)

    @pytest.mark.parametrize(FIELDS, [test_data24, test_data27])
    def test_multi_buy_volume_eq_one_sell(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.volume = 1000_00

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
        buy_trades = []
        payload.trade_type = 'buy'
        for i in range(5):
            payload.price, payload.volume = get_random_price_and_volume(special_info['precision'])
            r = api.entrusts_post(body=payload)
            buy_trades.append({
                'order_id': r.order_id,
                'price': payload.price,
                'volume': payload.volume
            })

        payload.trade_type = 'sell'
        if volume_flag == 'eq_buy_price':
            # 限价卖单价格低于买单最高价格,且高于买单最低价格,且等于某一中间买单价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            payload.price = sorted_buy_trades[2]['price']
            # 卖单出售数量等于,高于卖单价格的所有买单总数量
            payload.volume = round(
                sum([i['volume'] for i in sorted_buy_trades[3:]]), 8-int(special_info['precision']))
        else:
            # 限价卖单价格低于买单最高价格,且高于买单最低价格,且等且不等于任何买单价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            sell_price = (sorted_buy_trades[2]['price'] +
                          sorted_buy_trades[3]['price']) / 2
            payload.price = round(sell_price, int(special_info['precision']))
            # 卖单出售数量等于,高于卖单价格的所有买单总数量
            payload.volume = round(
                sum([i['volume'] for i in sorted_buy_trades[3:]]), 8-int(special_info['precision']))

        r = api.entrusts_post(body=payload)
        p_res = r.to_dict()
        sell_trade_id = p_res['order_id']


        time.sleep(6)
        sell_entrust_result = api.entrusts_get(status=['done'])
        sell_entrusts = sell_entrust_result.to_dict()
        done_ids = [i['order_id'] for i in sell_entrusts['items']]
        assert sell_trade_id in done_ids
        # 卖单应都成交了
        sell_result = api.trades_get(order_id=sell_trade_id)
        assert hasattr(sell_result.items[0], 'volume')
        assert hasattr(sell_result.items[0], 'fee')
        for i in sell_result.items:
            print(i.volume)
        assert round(sum([float(i.volume) for i in sell_result.items]), 8-int(special_info['precision'])) == float(payload.volume)

        # 买单剩余,测试剩余单撤销
        # 这里碰巧都是到index等于2
        ids = [i['order_id'] for i in sorted_buy_trades[:3]]

        for i in ids:
            api.entrusts_id_cancel_post(i)

    @pytest.mark.parametrize(FIELDS, [test_data25, test_data28])
    def test_multi_sell_volume_lt_buy(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000_0
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.volume = 1000_0
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
        buy_trades = []
        sub_range = 0.001
        payload.trade_type = 'buy'
        for i in range(5):
            payload.price, payload.volume = get_random_price_and_volume(special_info['precision'])
            r = api.entrusts_post(body=payload)
            buy_trades.append({
                'order_id': r.order_id,
                'price': payload.price,
                'volume': payload.volume
            })

        payload.trade_type = 'sell'
        if volume_flag == 'eq_buy_price':
            # 限价卖单价格低于买单最高价格,且高于买单最低价格,且等于某一中间买单价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            payload.price = sorted_buy_trades[2]['price']
            # 卖单出售数量小于,高于卖单价格的所有买单总数量
            payload.volume = round(
                sum([i['volume'] for i in sorted_buy_trades[3:]]) - sub_range,
                8-int(special_info['precision']))
        else:
            # 限价卖单价格低于买单最高价格,且高于买单最低价格,且不等于任何买单价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            sell_price = (sorted_buy_trades[2]['price'] +
                          sorted_buy_trades[3]['price']) / 2
            payload.price = round(sell_price, int(special_info['precision']))
            # 卖单出售数量小于,高于卖单价格的所有买单总数量
            payload.volume = round(
                sum([i['volume'] for i in sorted_buy_trades[3:]]) - sub_range,
                8-int(special_info['precision']))
        r = api.entrusts_post(body=payload)
        sell_trade_id = r.order_id

        time.sleep(5)
        entrust_res = api.entrusts_get(status=['done'])
        done_ids = [i.order_id for i in entrust_res.items]
        assert sell_trade_id in done_ids
        # 卖单应都成交了
        sell_result = api.trades_get(order_id=sell_trade_id)
        assert hasattr(sell_result.items[0], 'volume')
        assert hasattr(sell_result.items[0], 'fee')
        assert round(sum([float(i.volume) for i in sell_result.items]), 8-int(special_info['precision'])) == float(payload.volume)

        # 买单剩余,测试剩余单撤销，卖单小于，所以下标为3的买单没买完
        ids = [i['order_id'] for i in sorted_buy_trades[:4]]
        for i in ids:
            api.entrusts_id_cancel_post(i)

    @pytest.mark.parametrize(FIELDS, [test_data26, test_data29])
    def test_multi_sell_volume_gt_buy(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.volume = 1000
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
        # 精度
        buy_trades = []
        inc_range = 1
        payload.trade_type = 'buy'
        for i in range(5):
            payload.price, payload.volume = get_random_price_and_volume(special_info['precision'])
            r = api.entrusts_post(body=payload)
            buy_trades.append({
                'order_id': r.order_id,
                'price': payload.price,
                'volume': payload.volume
            })

        payload.trade_type = 'sell'
        if volume_flag == 'eq_buy_price':
            # 限价卖单价格低于买单最高价格,且高于买单最低价格,且等于某一中间买单价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            payload.price = sorted_buy_trades[2]['price']
            # 卖单出售数量大于,高于卖单价格的所有买单总数量,等于的也要算上，不然没法剩
            payload.volume = round(
                sum([i['volume'] for i in sorted_buy_trades[2:]]) + inc_range,
                8-int(special_info['precision']))
        else:
            # 限价卖单价格低于买单最高价格,且高于买单最低价格,且等且不等于任何买单价格
            sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
            payload.price = round(
                (sorted_buy_trades[2]['price'] + sorted_buy_trades[3]['price'])
                / 2, int(special_info['precision']))
            # 卖单出售数量大于,高于卖单价格的所有买单总数量
            payload.volume = round(
                sum([i['volume'] for i in sorted_buy_trades[3:]]) + inc_range,
                8-int(special_info['precision']))
        r = api.entrusts_post(body=payload)
        sell_trade_id = r.order_id

        time.sleep(5)

        done_res = api.entrusts_get(status=['done'])
        done_ids = [i.order_id for i in done_res.items]
        # 卖单量大于买单价格区间的数目，不完全成交
        assert sell_trade_id not in done_ids
        # 买单剩
        sell_result = api.trades_get(order_id=sell_trade_id)
        trade_ids = [i.order_id for i in sell_result.items]
        assert sell_trade_id in trade_ids
        assert hasattr(sell_result.items[0], 'volume')
        assert hasattr(sell_result.items[0], 'fee')

        # 买单剩余,测试剩余单撤销
        if volume_flag == 'eq_buy_price':
            ids = [i['order_id'] for i in sorted_buy_trades[:2]]
        else:
            ids = [i['order_id'] for i in sorted_buy_trades[:3]]

        for i in ids:
            api.entrusts_id_cancel_post(i)
