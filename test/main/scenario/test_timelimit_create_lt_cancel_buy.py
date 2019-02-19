# -*- coding: utf-8 -*-
# @File :  test_timelimit_create_lt_cancel_buy.py
# @Author : lh
import time
import pytest
import logging

from swagger_client.main.api import QuotationApi
from swagger_client.main.api import EntrustApi
from swagger_client.main.api import AccountApi
from swagger_client.tenant.api.quotation_api import QuotationApi as TenantQuotationApi
from swagger_client.venture.api.quotation_api import QuotationApi as VentureQuotationApi
from swagger_client.main.rest import ApiException
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .profitloss_data import (FIELDS, data22)

logger = logging.getLogger('test_timelimit_create_lt_cancel_buy')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

api = EntrustApi()
main_quota_api = QuotationApi()
main_ac_api = AccountApi()
tenant_quota_api = TenantQuotationApi()
venture_quota_api = VentureQuotationApi()


class TestTimeLimitCreateLtCancelBuy:
    # def teardown_method(self):
    #     result = api.entrusts_get(status=["entrusting"])
    #     for i in result.items:
    #         logger.error(f"canceling: {i}")
    #         try:
    #             api.entrusts_id_cancel_post(i.order_id)
    #         except Exception as e:
    #             logger.error(e)

    @pytest.mark.parametrize(FIELDS, data22)
    def test_timelimit_create_lt_cancel_buy(self, market_id, price, entrust_type, trade_type,
                                            volume, trigger_price, auto_cancel_at, special_login):
        payload = PostEntrustsRequest()
        payload.market_id = market_id
        payload.price = 1000
        payload.entrust_type = 'market'
        payload.trade_type = trade_type
        payload.trigger_price = trigger_price
        payload.volume = 100000
        payload.auto_cancel_at = auto_cancel_at
        # login
        special_login([api, main_ac_api, main_quota_api, tenant_quota_api, venture_quota_api])

        # 清空
        api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        api.entrusts_post(body=payload)

        # 恢复限价

        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.volume = volume

        try:
            first_result = api.entrusts_post(body=payload)
            logger.info(f"{trade_type} id: {first_result.order_id}")
        except Exception as e:
            if e.status == 400:
                logger.error('下单失败，没钱')
            raise e

        # 如果first_result的post参数trade_type是'buy'那么就要创建'sell'单
        if trade_type == 'buy':
            buy_id = first_result.order_id
            payload.trade_type = 'sell'
            result = api.entrusts_post(body=payload)
            sell_id = result.order_id
            logger.info(f"sell id :{sell_id}")
        # 如果first_result的post参数trade_type是'sell'那么就要创建'sell'单
        else:
            payload.trade_type = 'buy'
            sell_id = first_result.order_id
            result = api.entrusts_post(body=payload)
            buy_id = result.order_id
            logger.info(f"buy id :{buy_id}")

        time.sleep(5)
        result = api.entrusts_get(status=['done'])
        ids = [i.order_id for i in result.items]
        assert sell_id in ids
        assert buy_id in ids

        result_sell = api.trades_get(order_id=sell_id)
        logger.info(f"get result sell trades: {result}")
        result_buy = api.trades_get(order_id=buy_id)
        logger.info(f"get result buy trades:  {result}")
        assert hasattr(result_sell.items[0], 'price')
        assert hasattr(result_buy.items[0], 'price')
        assert float(result_buy.items[0].price) == price
        assert float(result_sell.items[0].price) == price
        logger.info('ending order')
