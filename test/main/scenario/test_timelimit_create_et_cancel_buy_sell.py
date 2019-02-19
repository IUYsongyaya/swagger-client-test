# -*- coding: utf-8 -*-
# @File :  test_timelimit_create_et_cancel_buy_sell.py
# @Author : lh
import time
import pytest
import logging
from datetime import datetime
from swagger_client.main.api import QuotationApi
from swagger_client.main.api import EntrustApi
from swagger_client.main.api import AccountApi
from swagger_client.tenant.api.quotation_api import QuotationApi as TenantQuotationApi
from swagger_client.venture.api.quotation_api import QuotationApi as VentureQuotationApi
from swagger_client.main.rest import ApiException
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .profitloss_data import (FIELDS, data22, data25)

logger = logging.getLogger('test_timelimit_create_lt_cancel_buy')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

main_entrust_api = EntrustApi()
main_ac_api = AccountApi()


class TestSamePriceVolumeDealSuccess:
    # def teardown_method(self):
    #     entrust_order_res = main_entrust_api.entrusts_get(status=['entrusting'])
    #     for i in entrust_order_res:
    #         logger.error(f'canceling: {i}')
    #         try:
    #             main_entrust_api.entrusts_id_cancel_post(i.order_id)
    #         except Exception as e:
    #             logger.error(e)

    # 下单时间>=撤单时间，下买单无法下单
    # 下单时间>=撤单时间，下卖单无法下单
    @pytest.mark.parametrize(FIELDS, [data22, data25])
    def test_timelimit_create_et_cancel_buy_sell(self, market_id, price, entrust_type, trade_type,
                                                 volume, trigger_price, auto_cancel_at, special_login):
        payload = PostEntrustsRequest()
        payload.market_id = market_id
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.trigger_price = trigger_price
        payload.volume = volume
        payload.auto_cancel_at = auto_cancel_at
        # login
        special_login([main_entrust_api, main_ac_api])

        # 清空
        main_entrust_api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        main_entrust_api.entrusts_post(body=payload)

        try:
            first_result = main_entrust_api.entrusts_post(body=payload)
            logger.info(f"{trade_type} id: {first_result.order_id}")
        except ApiException as e:
            if e.status == 400:
                logger.error('下单失败，没钱')
            raise e

        # 如果first_result的post参数trade_type是'buy'那么就要创建'sell'单
        if trade_type == 'buy':
            buy_id = first_result.order_id
            payload.trade_type = 'sell'
            result = main_entrust_api.entrusts_post(body=payload)
            sell_id = result.order_id
            logger.info(f"sell id :{sell_id}")
        # 如果first_result的post参数trade_type是'sell'那么就要创建'sell'单
        else:
            payload.trade_type = 'buy'
            sell_id = first_result.order_id
            result = main_entrust_api.entrusts_post(body=payload)
            buy_id = result.order_id
            logger.info(f"buy id :{buy_id}")

        time.sleep(5)
        result = main_entrust_api.entrusts_get(status=['done'])
        ids = [i.order_id for i in result.items]
        assert sell_id in ids
        assert buy_id in ids

        result_sell = main_entrust_api.trades_get(order_id=sell_id)
        logger.info(f"get result sell trades: {result}")
        result_buy = main_entrust_api.trades_get(order_id=buy_id)
        logger.info(f"get result buy trades:  {result}")
        assert hasattr(result_sell.items[0], 'price')
        assert hasattr(result_buy.items[0], 'price')
        assert float(result_buy.items[0].price) == price
        assert float(result_sell.items[0].price) == price
        logger.info('ending order')
        # 获取本地下单时间
        local_tm = datetime.fromtimestamp(0)
        # 本地时间转换为utc时间
        local_to_utc_time = datetime.utcfromtimestamp(local_tm.timestamp())
        #  下单时间>=撤单时间，下买单无法下单

        #  下单时间>=撤单时间，下卖单无法下单
