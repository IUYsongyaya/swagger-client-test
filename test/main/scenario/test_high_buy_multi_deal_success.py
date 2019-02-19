# @author: lj
import random
import time

import pytest

import swagger_client.main
from swagger_client.main.api.entrust_api import EntrustApi  # NOQA: F401
from swagger_client.main.rest import ApiException
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .data import (high_buy_multi_deal, get_random_price_and_volume)

api = swagger_client.main.api.entrust_api.EntrustApi()


class TestHighBuyMultiDealSuccess:
    @pytest.mark.parametrize("entrust_type,trade_type,volume_flag", high_buy_multi_deal)
    def test_high_buy_multi_deal_success(self, entrust_type, trade_type, volume_flag, special_login):
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


        # login
        special_info = special_login([api])
        payload.market_id = special_info['market_id']
        precision = special_info['precision']
        inc_range = 1 / (10 ** (int(precision) - 1))
        sub_range = 1 / (10 ** (8-int(precision) - 1))

        sell_ids = []
        sell_volume = []
        buy_ids = []
        buy_volume = []
        buy_id = ''
        sell_id = ''
        try:
            if trade_type == 'sell':
                # 多个卖单与单个买单
                sell_price, _ = get_random_price_and_volume()
                payload.price = sell_price
                for i in range(5):
                    _, volume = get_random_price_and_volume()
                    sell_volume.append(volume)
                    payload.volume = volume
                    result = api.entrusts_post(body=payload)
                    sell_ids.append(result.order_id)
            else:
                # 多个买单与单个卖单
                buy_price, _ = get_random_price_and_volume(precision)
                payload.price = round(buy_price + inc_range, int(precision))  # 买高
                for i in range(5):
                    _, volume = get_random_price_and_volume()
                    buy_volume.append(volume)
                    payload.volume = volume
                    result = api.entrusts_post(body=payload)
                    buy_ids.append(result.order_id)

            if trade_type == 'buy':
                # 单卖
                payload.trade_type = 'sell'  # 卖低
                payload.volume = sum(buy_volume)
                result = api.entrusts_post(body=payload)
                sell_id = result.order_id  # NOQA: F841
            else:
                # 单买
                payload.trade_type = 'buy'
                # sell_id = first_result['id']
                payload.price += inc_range  # 买高
                payload.volume = sum(sell_volume)  # sell_multi_eq_buy
                # 买量大于卖单多笔相加总量
                if volume_flag in ('sell_multi_lt_buy',):
                    payload.volume = round(sum(sell_volume) + (1 / (8-int(precision))), 8-int(precision))

                # 买量小于卖单多笔相加总量
                if volume_flag in ('sell_multi_gt_buy',):
                    payload.volume = round(sum(sell_volume) - sub_range, 8-int(precision))
                result = api.entrusts_post(body=payload)
                buy_id = result.order_id

        except ApiException as e:
            return

        # 获取已成交委托单
        time.sleep(3)
        result = api.entrusts_get(status=['done'])
        ids = [i.order_id for i in result.items]

        # 买单多，所以买单剩
        if volume_flag in ('sell_multi_lt_buy',):
            assert buy_id not in ids
            # 测试撤回多余单
            api.entrusts_id_cancel_post(buy_id)

        # 卖单多所以卖单剩
        if volume_flag in ('sell_multi_gt_buy',):
            need_cancel_sell_ids = [i for i in sell_ids if i not in ids]
            assert buy_id in ids
            # 测试撤回多余单
            for i in need_cancel_sell_ids:
                api.entrusts_id_cancel_post(i)
