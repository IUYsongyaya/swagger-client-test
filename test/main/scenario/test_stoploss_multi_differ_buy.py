# -*- coding: utf-8 -*-
# @File :  test_stoploss_multi_differ_buy.py
# @Author : lh

import random
import time

import pytest
from swagger_client.main.api.entrust_api import EntrustApi  # noqa: E501
from swagger_client.main.api.account_api import AccountApi
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from .profitloss_data import FIELDS, stoploss_multi_differ_buy, get_random_price_and_volume

main_entrust_api = EntrustApi()
main_ac_api = AccountApi()


class TestFirstBuyMultiDifferentPriceOneSell:
    @pytest.mark.parametrize(FIELDS, stoploss_multi_differ_buy)
    def test_multi_sell_volume_eq(self, market_id, price, entrust_type, trade_type,
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
        payload = PostEntrustsRequest()
        payload.market_id = market_id
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.trigger_price = trigger_price
        payload.volume = volume
        payload.auto_cancel_at = auto_cancel_at
        deviation = 0.005
        devia_pri = 0.01
        # 添加多笔卖单和一笔买单
        buy_trades = []
        for i in range(5):
            payload.trade_type = 'sell'
            price, volume = get_random_price_and_volume(special_info['precision'])
            payload.price = price
            payload.volume = volume
            r = main_entrust_api.entrusts_post(body=payload)
            buy_trades.append({'order_id': r.order_id,
                               'price': payload.price,
                               'volume': payload.volume})

        # 卖单升序排序
        sorted_buy_trades = sorted(buy_trades, key=lambda x: x['price'])
        payload.price = sorted_buy_trades[0]['price']
        # 下一笔买单将卖一撮合
        payload.trade_type = 'buy'
        payload.price = sorted_buy_trades[0]['price']
        payload.volume = sorted_buy_trades[0]['volume']
        r = main_entrust_api.entrusts_post(body=payload)
        sell_trade_id = r.order_id
        time.sleep(5)
        # sell_res = main_entrust_api.entrusts_get(status='entrusting')
        sell_res = main_entrust_api.entrusts_get()
        print('交易委托列表:', sell_res)
        sell_list = [i.order_id for i in sell_res.items]
        assert sell_trade_id in sell_list
        trade_res = main_entrust_api.trades_get(order_id=sorted_buy_trades[0]['order_id'])
        assert trade_res.items
        # 获取最新成交价
        new_price = [i.price for i in trade_res.items][0]
        # 下一笔止损买单,当前价小于等于触发价，开始委托
        # 2.下委托单(类型:止损 如果当前成交价大于触发价)
        payload.trigger_price = sorted_buy_trades[1]['price']
        payload.price = sorted_buy_trades[2]['price'] + devia_pri
        payload.trade_type = 'buy'
        payload.entrust_type = 'profit_loss'
        tri_price = sorted_buy_trades[1]['price']
        payload.volume = sorted_buy_trades[2]['volume'] + deviation
        commi_price = sorted_buy_trades[2]['price'] + devia_pri
        buy_res = main_entrust_api.entrusts_post(body=payload)
        commission_order_id = buy_res.order_id
        # 3.再下一买一卖,达到触发价
        payload.trade_type = 'buy'
        payload.trigger_price = None
        payload.price = sorted_buy_trades[1]['price']
        payload.volume = sorted_buy_trades[1]['volume']
        payload.entrust_type = 'limit'
        # 3.1先下一笔买单
        buy2_res = main_entrust_api.entrusts_post(body=payload)
        buy2_id = buy2_res.order_id
        # 3.3检查委托交易列表
        time.sleep(5)
        check_res = main_entrust_api.entrusts_get(status=['done'])
        print('已完成的交易委托列表:', check_res)
        assert check_res.items
        check_list = [res.order_id for res in check_res.items]
        assert buy2_id in check_list
        # 3.4获取成交记录列表
        ch_trade_res = main_entrust_api.trades_get(order_id=buy2_id)
        assert ch_trade_res.items
        latest_price = ch_trade_res.items[0].price
        time.sleep(5)
        # 4.当前成交价价变动时,当前价小于等于触发价，开始委托,委托价大于卖一时候,,检查委托列表是否有委托订单记录
        if round(float(latest_price), 8) <= tri_price and round(float(commi_price), 8) > sorted_buy_trades[2]['price']:
            order_lists = main_entrust_api.entrusts_get(status=["entrusting"], trade_type='buy')
            assert order_lists.items
            order_list = [order_res.order_id for order_res in order_lists.items]
            assert commission_order_id in order_list
        result = main_entrust_api.trades_get(order_id=sorted_buy_trades[2]['order_id'])
        result_list = [i.order_id for i in result.items]
        assert commission_order_id not in result_list
        # 5.撤销未成交的止损委托单
        main_entrust_api.entrusts_id_cancel_post(commission_order_id)
        time.sleep(5)
        cancel_res = main_entrust_api.entrusts_get(status=['cancelled'])
        assert cancel_res.items
        cancel_list = [i.order_id for i in cancel_res.items]
        assert commission_order_id in cancel_list
