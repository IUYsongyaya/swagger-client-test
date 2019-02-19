# -*- coding: utf-8 -*-
# @File :  test_stoploss_cancel_buy_order.py
# @Author : lh
import time

import pytest

from swagger_client.main.api.entrust_api import EntrustApi  # NOQA: F401
from swagger_client.main.api.account_api import AccountApi
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .profitloss_data import (FIELDS, stopprofit_cancel_buy_order, get_random_price_and_volume)

main_entrust_api = EntrustApi()
main_ac_api = AccountApi()


# 止盈买单单委托成功,并撤单成功
class TestTakeProfitSell:
    # def teardown_method(self):
    #     """
    #     这个类里面的每个test方法执行后都会执行此函数,清理现场数据
    #     """
    #     result = main_entrust_api.entrusts_get(status=["entrusting"])
    #     for i in result.items:
    #         main_entrust_api.entrusts_id_cancel_post(i.order_id)

    @pytest.mark.parametrize(FIELDS, stopprofit_cancel_buy_order)
    def test_takeprofit_sell(self, market_id, price, entrust_type, trade_type,
                             volume, trigger_price, auto_cancel_at, entrust_special_login):
        # login
        special_info = entrust_special_login([main_entrust_api, main_ac_api])
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        payload.trigger_price = trigger_price
        payload.volume = 100000_00
        payload.auto_cancel_at = auto_cancel_at
        # login
        payload.market_id = market_id

        # 清空
        main_entrust_api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        main_entrust_api.entrusts_post(body=payload)

        # 恢复限价
        price, volume = get_random_price_and_volume(special_info['precision'])

        # 构造entrust_post请求对象
        payload = PostEntrustsRequest()
        payload.market_id = market_id
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.trigger_price = trigger_price
        payload.volume = volume
        payload.auto_cancel_at = auto_cancel_at

        # 1.先下一买一卖,构造最新成交价
        first_result = main_entrust_api.entrusts_post(body=payload)
        buy1_id = first_result.order_id
        payload.trade_type = 'buy'
        result = main_entrust_api.entrusts_post(body=payload)
        sell1_id = result.order_id
        # 1.1 检查成交记录列表,委托交易列表
        time.sleep(5)
        # entrust_res = main_entrust_api.entrusts_get(status=['done'])
        entrust_res = main_entrust_api.entrusts_get()
        print('交易委托列表拍:', entrust_res)
        assert entrust_res.items
        entrust_list = [res.order_id for res in entrust_res.items]
        assert buy1_id in entrust_list
        assert sell1_id in entrust_list
        # 1.2 检查委托交易列表
        trade_res = main_entrust_api.trades_get(order_id=buy1_id)
        assert trade_res.items
        # 获取最新成交价
        new_price = trade_res.items[0].price
        # 2.下委托单(类型:止损 如果当前价小于触发价)
        payload.trigger_price = float(new_price) + 0.01
        payload.price = float(new_price) + 0.01
        payload.trade_type = 'buy'
        payload.entrust_type = 'profit_loss'
        tri_price = float(new_price) + 0.01
        buy_res = main_entrust_api.entrusts_post(body=payload)
        commission_order_id = buy_res.order_id
        # 3.再下一买一卖,达到触发价
        payload.trade_type = 'buy'
        payload.trigger_price = None
        payload.price = str(float(new_price) + 0.04)
        buy2_price = str(float(new_price) + 0.04)
        payload.entrust_type = 'limit'
        # 3.1先下一笔买单
        buy2_res = main_entrust_api.entrusts_post(body=payload)
        buy2_id = buy2_res.order_id
        # 3.2再下一笔卖单
        payload.trade_type = 'sell'
        payload.price = buy2_price
        sell2_res = main_entrust_api.entrusts_post(body=payload)
        sell2_id = sell2_res.order_id
        # 3.3检查委托交易列表
        time.sleep(5)
        check_res = main_entrust_api.entrusts_get(status=['done'])
        print('已完成委托交易列表:', check_res)
        assert check_res.items
        check_list = [res.order_id for res in check_res.items]
        assert buy2_id in check_list
        assert sell2_id in check_list
        # 3.4获取成交记录列表
        ch_trade_res = main_entrust_api.trades_get(order_id=buy2_id)
        assert ch_trade_res.items[0]
        latest_price = ch_trade_res.items[0].price
        # 4.当前成交价价变动时,当前价小于等于触发价，开始委托,检查委托列表是否有委托订单记录
        if round(float(latest_price), 8) >= tri_price:
            order_lists = main_entrust_api.entrusts_get(status=["entrusting"], trade_type='buy')
            assert order_lists.items
            order_list = [order_res.order_id for order_res in order_lists.items]
            assert commission_order_id in order_list
        # 5.在委托记录中选择需要撤单的订单，点击撤销按钮撤单成功，生成一笔历史委托订单，订单状态为撤销
        main_entrust_api.entrusts_id_cancel_post(order_list[0])
        time.sleep(5)
        cancel_res = main_entrust_api.entrusts_get(status=['cancelled'])
        cancel_list = [i.order_id for i in cancel_res.items]
        assert commission_order_id in cancel_list
