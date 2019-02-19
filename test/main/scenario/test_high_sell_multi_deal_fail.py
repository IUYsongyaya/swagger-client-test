# @author: lj
import pytest
import random
import swagger_client.main
from swagger_client.main.api.entrust_api import EntrustApi  # NOQA: F401
from swagger_client.main.rest import ApiException
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .data import FIELDS, test_data18, test_data13, get_random_price_and_volume

api = swagger_client.main.api.entrust_api.EntrustApi()


class TestHighSellMultiDealFail:
    # 18 多笔卖单一笔买单，卖高，买单总数与卖单数目一致， 不成交
    @pytest.mark.parametrize("entrust_type,trade_type,volume_flag", test_data18)
    def test_high_sell_multi_sell_first(self, entrust_type, trade_type, volume_flag, special_login):
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

        sell_volume = []
        inc_range = round(1 / 10 ** (int(precision) - 1))
        buy_id = ''
        sell_ids = []
        try:
            assert volume_flag == 'multi_sell'
            # 多个卖单与单个买单
            sell_price, _ = get_random_price_and_volume(precision)
            payload.price = round(sell_price + inc_range, int(precision))  # 卖高
            for i in range(5):
                _, volume = get_random_price_and_volume(precision)
                sell_volume.append(volume)
                payload.volume = volume
                result = api.entrusts_post(body=payload)
                sell_ids.append(result.order_id)

            # 单买
            payload.trade_type = 'buy'
            # sell_id = first_result['id']
            payload.volume = round(sum(sell_volume), int(precision))
            result = api.entrusts_post(body=payload)
            buy_id = result.order_id

        except ApiException as e:
            if price == '' or market_id == '':
                assert e.status == 400

        # 获取已成交委托单
        result = api.entrusts_get(status=['done'])
        ids = [i.id for i in result.items]

        # 交易不成功
        assert buy_id not in ids

        # 撤回
        for i in sell_ids + [buy_id]:
            api.entrusts_id_cancel_post(i)

    # 13 多笔买单一笔卖单，卖高，买单总数与卖单数目一致， 不成交
    @pytest.mark.parametrize("entrust_type,trade_type,volume_flag", test_data13)
    def test_high_sell_multi_buy_first(self, entrust_type, trade_type, volume_flag, special_login):
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
        inc_range = round(1 / (10 ** (int(precision) - 1)), int(precision))

        buy_ids = []
        buy_volume = []
        try:
            assert volume_flag == 'multi_buy'
            # 多个买单与单个卖单
            buy_price, _ = get_random_price_and_volume(precision)
            payload.price = buy_price
            for i in range(5):
                _, volume = get_random_price_and_volume(precision)
                buy_volume.append(volume)
                payload.volume = volume
                result = api.entrusts_post(body=payload)
                buy_ids.append(result.order_id)

            # 单卖
            payload.trade_type = 'sell'
            payload.volume = round(sum(buy_volume), int(precision))
            payload.price = round(payload.price + inc_range, int(precision))  # 卖高
            result = api.entrusts_post(body=payload)
            sell_id = result.order_id

        except ApiException as e:
            return

        # 获取已成交委托单
        result = api.entrusts_get(status=['done'])
        ids = [i.id for i in result.items]

        # 交易不成功
        assert sell_id not in ids

        # 撤回
        for i in buy_ids + [sell_id]:
            api.entrusts_id_cancel_post(i)
