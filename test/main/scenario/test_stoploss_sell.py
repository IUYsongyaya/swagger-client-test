# -*- coding: utf-8 -*-
# @File :  test_stoploss_sell.py
# @Author : lh
# @time : 18-11-14 下午6:06
import time

import pytest
from swagger_client.main.api.entrust_api import EntrustApi  # NOQA: F401
from swagger_client.main.api.account_api import AccountApi
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .profitloss_data import (FIELDS, stoploss_sell, stoploss_sell_fail, get_random_price_and_volume)

main_entrust_api = EntrustApi()
main_ac_api = AccountApi()


# 止损卖单
class TestStopLossSell:
    @pytest.mark.parametrize(FIELDS, stoploss_sell)
    def test_stoploss_sell(self, market_id, price, entrust_type, trade_type,
                           volume, trigger_price, auto_cancel_at, entrust_special_login):
        # login
        special_info = entrust_special_login([main_entrust_api, main_ac_api])
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        # payload.trigger_price = trigger_price
        payload.volume = 100000_00
        # payload.auto_cancel_at = auto_cancel_at
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
        # entrust_res = main_entrust_api.entrusts_get(status=['done'])
        time.sleep(5)
        entrust_res = main_entrust_api.entrusts_get()
        print('交易委托列表:', entrust_res)
        assert entrust_res.items
        entrust_list = [res.order_id for res in entrust_res.items]
        assert buy1_id in entrust_list
        assert sell1_id in entrust_list
        # 1.2 检查委托交易列表
        trade_res = main_entrust_api.trades_get(order_id=buy1_id)
        assert trade_res.items
        # 获取最新成交价
        new_price = trade_res.items[0].price
        # 2.下委托单(类型:止损 如果当前成交价大于触发价)
        payload.trigger_price = str(float(new_price) - 0.01)
        payload.price = str(float(new_price) - 0.01)
        payload.trade_type = 'sell'
        payload.entrust_type = 'profit_loss'
        tri_price = float(new_price) - 0.01
        commi_price = tri_price
        buy_res = main_entrust_api.entrusts_post(body=payload)
        commission_order_id = buy_res.order_id
        # 3.再下一买一卖,达到触发价
        payload.trade_type = 'buy'
        payload.trigger_price = None
        payload.price = str(float(new_price) - 0.04)
        buy2_price = payload.price
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
        print('已完成交易委托列表:', check_res)
        assert check_res.items
        check_list = [res.order_id for res in check_res.items]
        print('chck_list:', check_list)
        assert buy2_id in check_list
        assert sell2_id in check_list
        # 3.4获取成交记录列表
        ch_trade_res = main_entrust_api.trades_get(order_id=buy2_id)
        assert ch_trade_res.items[0]
        latest_price = ch_trade_res.items[0].price
        # 4.当前成交价价变动时,当前价小于等于触发价，开始委托,检查委托列表是否有委托订单记录
        if round(float(latest_price), 8) <= tri_price:
            order_lists = main_entrust_api.entrusts_get(status=["entrusting"], trade_type='sell')
            assert order_lists.items
            order_list = [order_res.order_id for order_res in order_lists.items]
            assert commission_order_id in order_list
        # 5.下一个与第2步方向相反的单,促成第二步的单成交
        payload.trade_type = 'buy'
        # 委托价<=买一时,撮合成功
        payload.price = commi_price + 0.01
        result = main_entrust_api.entrusts_post(body=payload)
        sell_id = result.order_id
        time.sleep(5)
        result = main_entrust_api.trades_get()
        ids = [i.order_id for i in result.items]
        assert sell_id in ids
        assert commission_order_id in ids

    @pytest.mark.parametrize(FIELDS, stoploss_sell_fail)
    def test_stoploss_sell_fail(self, market_id, price, entrust_type, trade_type,
                                volume, trigger_price, auto_cancel_at, entrust_special_login):
        # login
        special_info = entrust_special_login([main_entrust_api, main_ac_api])
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        # payload.trigger_price = trigger_price
        payload.volume = 100000_00
        # payload.auto_cancel_at = auto_cancel_at
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
        # entrust_res = main_entrust_api.entrusts_get(status=['done'])
        time.sleep(5)
        entrust_res = main_entrust_api.entrusts_get()
        print('交易委托列表:', entrust_res)
        assert entrust_res.items
        entrust_list = [res.order_id for res in entrust_res.items]
        assert buy1_id in entrust_list
        assert sell1_id in entrust_list
        # 1.2 检查委托交易列表
        trade_res = main_entrust_api.trades_get(order_id=buy1_id)
        assert trade_res.items
        # 获取最新成交价
        new_price = trade_res.items[0].price
        # 2.下委托单(类型:止损 如果当前成交价大于触发价)
        payload.trigger_price = str(float(new_price) - 0.01)
        payload.price = str(float(new_price) - 0.01)
        payload.trade_type = 'sell'
        payload.entrust_type = 'profit_loss'
        tri_price = float(new_price) - 0.01
        commi_price = tri_price
        buy_res = main_entrust_api.entrusts_post(body=payload)
        commission_order_id = buy_res.order_id
        # 3.再下一买一卖,达到触发价
        payload.trade_type = 'buy'
        payload.trigger_price = None
        payload.price = str(float(new_price) - 0.04)
        buy2_price = str(float(new_price) - 0.04)
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
        print('已完成交易委托列表:', check_res)
        assert check_res.items
        check_list = [res.order_id for res in check_res.items]
        assert buy2_id in check_list
        assert sell2_id in check_list
        # 3.4获取成交记录列表
        ch_trade_res = main_entrust_api.trades_get(order_id=buy2_id)
        assert ch_trade_res.items
        latest_price = ch_trade_res.items[0].price
        # 4.当前成交价价变动时,当前价小于等于触发价，开始委托,检查委托列表是否有委托订单记录
        if round(float(latest_price), 8) <= tri_price:
            order_lists = main_entrust_api.entrusts_get(status=["entrusting"], trade_type='sell')
            assert order_lists.items
            order_list = [order_res.order_id for order_res in order_lists.items]
            assert commission_order_id in order_list
        # 5.下一个与第2步方向相反的单,促成第二步的单成交
        payload.trade_type = 'buy'
        # 委托价>买一时,撮合不成功,2步下的止损sell单在委托列表
        payload.price = commi_price - 0.01
        result = main_entrust_api.entrusts_post(body=payload)
        sell_id = result.order_id
        time.sleep(5)
        result = main_entrust_api.trades_get()
        ids = [i.order_id for i in result.items]
        assert sell_id not in ids
        assert commission_order_id not in ids
        result = main_entrust_api.entrusts_get(status=["entrusting"])
        result_list = [i.order_id for i in result.items]
        assert commission_order_id in result_list
