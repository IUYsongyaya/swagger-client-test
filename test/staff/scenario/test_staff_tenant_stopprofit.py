# -*- coding: utf-8 -*-
# @File :  test_staff_tenant_stopprofit.py
# @Author : lh
import pytest

from swagger_client.main.api.entrust_api import EntrustApi  # NOQA: F401
from swagger_client.main.api.account_api import AccountApi
from swagger_client.staff.api.entrust_api import EntrustApi as StaffEntrustApi
from swagger_client.tenant.api.exchange_entrust_api import ExchangeEntrustApi
from swagger_client.main.rest import ApiException
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from test.main.scenario.profitloss_data import (FIELDS, staff_tenant_stopprofit)

api = EntrustApi()
account_api = AccountApi()
staff_api = StaffEntrustApi()  # 管理后台
tenant_api = ExchangeEntrustApi()  # 租户平台


# 止损卖单
class TestStaffTenantStopProfit:
    def setup_method(self):
        result = api.entrusts_get(status="entrusting", async_req=True)
        for i in result['items']:
            api.entrusts_id_cancel_post(i["id"], async_req=True)

    def teardown_method(self):
        result = api.entrusts_get(status="entrusting", async_req=True)
        for i in result['items']:
            api.entrusts_id_cancel_post(i["id"], async_req=True)

    @pytest.mark.parametrize(FIELDS.replace(",volume_flag", ""), staff_tenant_stopprofit)
    def test_takeprofit_sell(self, market_id, price, entrust_type, trade_type,
                             volume, trigger_price, auto_cancel_at, special_login, with_login):
        # 构造entrust_post请求对象
        payload = PostEntrustsRequest()
        payload.market_id = market_id
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.trigger_price = trigger_price
        payload.volume = volume
        payload.auto_cancel_at = auto_cancel_at
        # special_login
        special_login([api])
        # login
        with_login('staff', [staff_api], 'account', 'password')  # TODO add account
        # 1.先下一买一卖,构造最新成交价
        try:
            first_result = api.entrusts_post(body=payload, async_req=True)
            buy1_id = first_result.get('orderid', '')
            payload.trade_type = 'sell'
            result = api.entrusts_post(body=payload, async_req=True)
            sell1_id = result.get('orderid', '')
            # 1.1 检查成交记录列表,委托交易列表
            entrust_res = api.entrusts_get(status=['done'], async_req=True)
            assert entrust_res['items']
            entrust_list = [res["orderid"] for res in entrust_res['items']]
            assert buy1_id in entrust_list
            assert sell1_id in entrust_list
            # 1.2 检查委托交易列表
            trade_res = api.trades_get(order_id=buy1_id, async_req=True)
            assert trade_res['items']
            # 获取最新成交价
            new_price = trade_res['items'][0]['price']
        except ApiException as e:
            if market_id == "" or price == "":
                assert e.status == 500
            return
        # 2.下委托单(类型:止损 如果当前价小于触发价)
        try:
            payload.trigger_price = new_price + 0.001
            payload.price = payload.trigger_price
            payload.trade_type = 'buy'
            payload.entrust_type = 'profitLoss'
            tri_price = new_price + 0.001
            commi_price = tri_price
            buy_res = api.entrusts_post(body=payload, async_req=True)
            commission_order_id = buy_res.get('orderid', '')
        except ApiException as e:
            if market_id == "" or price == "":
                assert e.status == 500
            return
        # 3.再下一买一卖,达到触发价
        try:
            payload.trade_type = 'buy'
            payload.trigger_price = ''
            payload.price = new_price + 0.004
            buy2_price = payload.price
            payload.entrust_type = 'limit'
            # 3.1先下一笔买单
            buy2_res = api.entrusts_post(body=payload, async_req=True)
            buy2_id = buy2_res.get('orderid', '')
            # 3.2再下一笔卖单
            payload.trade_type = 'sell'
            payload.price = buy2_price
            sell2_res = api.entrusts_post(body=payload, async_req=True)
            sell2_id = sell2_res.get('orderid', '')
            # 3.3检查委托交易列表
            check_res = api.entrusts_get(status=['done'], async_req=True)
            assert check_res['items']
            check_list = [res.id for res in entrust_res['items']]
            assert buy2_id in check_list
            assert sell2_id in check_list
            # 3.4获取成交记录列表
            ch_trade_res = api.trades_get(order_id=buy2_id, async_req=True)
            assert ch_trade_res['items'][0]
            latest_price = ch_trade_res['items'][0]['price']
        except ApiException as e:
            if market_id == "" or price == "":
                assert e.status == 500
            return
        # 4.当前成交价价变动时,当前价小于等于触发价，开始委托,检查委托列表是否有委托订单记录
        if latest_price >= tri_price:
            order_lists = api.entrusts_get(status=["entrusting"], tradeType='buy', async_req=True)
            assert order_lists['items']
            order_list = [order_res.id for order_res in order_lists['items']]
            assert commission_order_id in order_list
        # 5.下一个与第2步方向相反的单,促成第二步的单成交
        try:
            payload.trade_type = 'sell'
            # 委托价>=卖一时,撮合成功
            payload.price = commi_price
            result = api.entrusts_post(body=payload, async_req=True)
            sell_id = result.get('orderid', '')
        except ApiException as e:
            if price == '' or market_id == '':
                assert e.status == 500
            return
        result = api.trades_get(async_req=True)
        ids = [i.id for i in result['items']]
        assert sell_id in ids
        assert commission_order_id in ids

        user_info = account_api.accounts_account_info_get()
        assert user_info['account_info'].get('account_id')
        result = staff_api.entrusts_get(uid=user_info['account_info'].get('account_id'), status="done", async_req=True)
        ids = [i.id for i in result['items']]
        assert sell_id in ids

        # 测试交易所获取委托列表
        result = staff_api.entrusts_get(entrust_id=sell_id, status="done", async_req=True)
        assert result.items.id == sell_id

        fee_result = staff_api.fee_history_get(uid=user_info['account_info'].get('account_id'), status="done")
        fee_ids_map = {i.trade_history_id: i.fee_yield_amount for i in fee_result['items']}
        for k, v in fee_ids_map.items():
            r = staff_api.trade_history_get(trade_history_id=k, async_req=True)
            assert r.items.buyer_fee == v
            r2 = tenant_api.exchanges_trade_history_get(trade_id=k, async_req=True)
            assert r2.items.buyerFee == v
            tenant_fee_r = tenant_api.exchanges_fee_history_get(trade_id=k, async_req=True)
            assert tenant_fee_r.items.fee_yield_amount == v

        payload.price = 10 ** 8
        payload.trade_type = 'sell'
        result = api.entrusts_post(body=payload, async_req=True)
        buy_id = result.order_id
        staff_api.entrusts_id_cancel_post(buy_id, async_req=True)
