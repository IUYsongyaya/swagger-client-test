# @author: lj
import time
import pytest

from swagger_client.main.api.entrust_api import EntrustApi  # noqa: E501
from swagger_client.main.rest import ApiException
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .data import (FIELDS, high_buy_test_success_data1, high_buy_test_success_data2, get_random_price_and_volume)

api = EntrustApi()


class TestHighBuyDealSuccess:
    # 数据里写一条来代表两条，写buy说明先买，写sell说明先卖
    @pytest.mark.parametrize(FIELDS, high_buy_test_success_data1)
    def test_high_buy_deal_success(self, market_id, price, entrust_type, trade_type,
                                   volume, trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        # payload.trigger_price = trigger_price
        payload.volume = 1000_00
        # payload.auto_cancel_at = auto_cancel_at
        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        # 清空

        before_market_buy = api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        before_makret_sell = api.entrusts_post(body=payload)
        # 恢复限价

        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        # 符合精度的价格和数目
        price, volume = get_random_price_and_volume(special_info['precision'])
        payload.price = price
        payload.volume = volume
        price_range = (1 / (10 ** (int(special_info['precision'])-1)))
        sub_range = (1 / (10 ** (int(special_info['precision'])-1)))
        inc_range = (1 / (10 ** (int(special_info['precision'])-1)))
        sell_id = ''
        buy_id = ''
        try:
            # 不管是sell还是buy，只有less或者more两种情况，所以忽略sell或者buy
            if volume_flag in ('sell_less', 'buy_less'):
                payload.volume = round(payload.volume - sub_range, int(special_info['precision']))
            if volume_flag in ('buy_more', 'sell_more'):
                payload.volume = round(payload.volume + inc_range, int(special_info['precision']))
            print(f"{volume_flag}payload{payload}")
            first_result = api.entrusts_post(body=payload)
            if trade_type == 'buy':
                buy_id = first_result.order_id
                payload.trade_type = 'sell'
                payload.volume = volume
                payload.price = round(payload.price - price_range, int(special_info['precision']))
                print(f"{trade_type}payload{payload}")
                result = api.entrusts_post(body=payload)
                sell_id = result.order_id
            else:
                payload.trade_type = 'buy'
                sell_id = first_result.order_id
                payload.price = round(payload.price + price_range, int(special_info['precision']))
                payload.volume = volume
                print(f"{trade_type}payload{payload}")
                result = api.entrusts_post(body=payload)
                buy_id = result.order_id

        except ApiException as e:
            assert e.status == 400

        time.sleep(5)
        # 最新的default 的pagesize估计能够把刚下的单捞出来
        result = api.entrusts_get(status=['done'])
        print(result)
        ids = [i.order_id for i in result.items]

        # 买单多或着卖单少，所以买单剩
        if volume_flag in ('buy_more', 'sell_less'):
            assert sell_id in ids  # 买单多卖完全部成交
            # 测试撤回多余单
            api.entrusts_id_cancel_post(buy_id)
        # 卖单多或者买单少所以卖单剩
        if volume_flag in ('sell_more', 'buy_less'):
            assert buy_id in ids  # 卖单多买单全部成交
            # 测试撤回多余单
            api.entrusts_id_cancel_post(sell_id)

    # 数据里写一条来代表两条，写buy说明先买，写sell说明先卖
    @pytest.mark.parametrize(FIELDS, high_buy_test_success_data2)
    def test_high_buy_same_volume_deal_success(self, market_id, price, entrust_type, trade_type,
                                               volume, trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.volume = 1000_00
        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        # 清空

        before_market_buy = api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        before_makret_sell = api.entrusts_post(body=payload)
        # 恢复限价

        payload.entrust_type = entrust_type
        payload.trade_type = trade_type


        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        price, volume = get_random_price_and_volume(special_info['precision'])
        payload.volume = volume
        payload.price = price
        price_range = (1 / (10 ** int(special_info["precision"])))

        try:
            assert 'same' in volume_flag
            first_result = api.entrusts_post(body=payload)
            if trade_type == 'buy':
                buy_id = first_result.order_id
                payload.trade_type = 'sell'
                payload.price -= price_range
                result = api.entrusts_post(body=payload)
                sell_id = result.order_id
            else:
                payload.trade_type = 'buy'
                sell_id = first_result.order_id
                payload.price += price_range
                result = api.entrusts_post(body=payload)
                buy_id = result.order_id

        except ApiException as e:
            assert e.status == 400
            raise e

        time.sleep(5)
        result = api.trades_get()
        ids = [i.order_id for i in result.items]
        assert sell_id in ids
        assert buy_id in ids
