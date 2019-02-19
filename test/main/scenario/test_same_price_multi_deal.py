# @author: lj
import pytest
import time
import logging

from swagger_client.main.rest import ApiException
from swagger_client.main.api import EntrustApi
from swagger_client.tenant.api import ExchangeEntrustApi
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .data import (FIELDS, test_data17, test_data12,
                   get_random_price_and_volume, TENANT, TENANTPWD)

tenant_api = ExchangeEntrustApi()
api = EntrustApi()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class TestSamePriceMultiDeal:
    def teardown_method(self):
        result = api.entrusts_get(status=["entrusting"])
        for i in result.items:
            api.entrusts_id_cancel_post(i.order_id)

    @pytest.mark.parametrize(FIELDS, test_data17)
    def igtest_same_price_volume_multi_sell_first(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login,
            with_login):
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

        price, _ = get_random_price_and_volume(special_info['precision'])  # 精度
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.volume = volume

        sell_ids = []
        sell_volume = []
        buy_id = ''
        try:
            assert volume_flag == 'multi_sell'
            # 多个卖单与单个买单
            for i in range(5):
                _, volume = get_random_price_and_volume(special_info['precision'])  # 精度
                sell_volume.append(volume)
                payload.volume = volume
                result = api.entrusts_post(body=payload)
                sell_ids.append(result.order_id)

            # 单买
            payload.trade_type = 'buy'
            # sell_id = first_result['id']
            payload.volume = sum(sell_volume)
            result = api.entrusts_post(body=payload)
            buy_id = result.order_id
        except ApiException as e:
            if e.status == 400:
                raise e

        # 获取已成交委托单
        time.sleep(5)
        logger.info(f"sell_ids: {sell_ids}, buy_id: {buy_id}")
        result = api.entrusts_get(status=['done'])
        ids = [i.order_id for i in result.items]
        assert buy_id in ids

        result_sell = api.trades_get(order_id=buy_id)
        assert hasattr(result_sell.items[0], "price")
        assert float(result_sell.items[0].price) == price

        with_login('tenant', [tenant_api], account=TENANT, password=TENANTPWD)
        tenant_entrusts = tenant_api.exchange_entrusts_get(
            status=['done'], uid=special_info['account_id'])
        ids = [i.order_id for i in tenant_entrusts.items]
        assert buy_id in ids

        tenant_trades = tenant_api.exchange_trade_history_get(order_id=buy_id)
        assert hasattr(tenant_trades.items[0], "price")
        assert float(tenant_trades.items[0].price) == price

    @pytest.mark.parametrize(FIELDS, test_data12)
    def test_same_price_volume_multi_buy(
            self, market_id, price, entrust_type, trade_type, volume,
            trigger_price, auto_cancel_at, volume_flag, special_login,
            with_login):
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
        price, _ = get_random_price_and_volume(special_info['precision'])  # 精度
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.volume = volume

        buy_ids = []
        buy_volume = []
        # login
        sell_id = ''
        try:
            assert volume_flag == 'multi_buy'
            # 多个买单与单个卖单
            for i in range(5):
                _, volume = get_random_price_and_volume(special_info['precision'])  # 精度
                buy_volume.append(volume)
                payload.volume = volume
                result = api.entrusts_post(body=payload)
                buy_ids.append(result.order_id)

            # 单卖
            payload.trade_type = 'sell'
            # sell_id = first_result['id']
            payload.volume = sum(buy_volume)
            result = api.entrusts_post(body=payload)
            sell_id = result.order_id

        except ApiException as e:
            if e.status == 400:
                raise e

        time.sleep(5)
        # 获取已成交委托单
        result = api.entrusts_get(status=['done'])
        ids = [i.order_id for i in result.items]
        assert sell_id in ids

        result_sell = api.trades_get(order_id=sell_id)
        assert hasattr(result_sell.items[0], "price")
        assert float(result_sell.items[0].price) == price

        with_login('tenant', [tenant_api], account=TENANT, password=TENANTPWD)
        tenant_trades = tenant_api.exchange_trade_history_get(order_id=sell_id)
        assert hasattr(tenant_trades.items[0], "price")
        assert float(tenant_trades.items[0].price) == price

        my_exchange = api.entrusts_list_exchange_get()
        assert special_info['exchange_id'] in [
            i.id for i in my_exchange.items
        ]
