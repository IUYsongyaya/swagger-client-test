

import pytest

from swagger_client.main.api.entrust_api import EntrustApi  # NOQA: F401
from swagger_client.main.api.account_api import AccountApi
from swagger_client.staff.api.entrust_api import EntrustApi as StaffEntrustApi
from swagger_client.tenant.api.exchange_entrust_api import ExchangeEntrustApi
from swagger_client.main.rest import ApiException
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from test.main.scenario.data import (FIELDS, same_price_volume_entrust_data)

api = EntrustApi()
account_api = AccountApi()
staff_api = StaffEntrustApi()  # 管理后台
tenant_api = ExchangeEntrustApi()


class TestSamePriceVolumeDealSuccess:
    def teardown_method(self):
        result = api.entrusts_get(status="entrusting", async_req=True)
        for i in result['items']:
            api.entrusts_id_cancel_post(i["id"], async_req=True)

    @pytest.mark.parametrize(FIELDS.replace(",volume_flag", ""), same_price_volume_entrust_data)
    def test_entrust(self, market_id, price, entrust_type, trade_type,
                     volume, trigger_price, auto_cancel_at, special_login, with_login):
        payload = PostEntrustsRequest()
        payload.market_id = market_id
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.trigger_price = trigger_price
        payload.volume = volume
        payload.auto_cancel_at = auto_cancel_at
        # login
        special_login([api, tenant_api])
        # login
        with_login('staff', [staff_api], 'account', 'password')  # TODO add account

        try:
            first_result = api.entrusts_post(body=payload, async_req=True)
            # 如果first_result的post参数trade_type是'buy'那么就要创建'sell'单
            if trade_type == 'buy':
                buy_id = first_result['id']
                payload.trade_type = 'sell'
                result = api.entrusts_post(body=payload, async_req=True)
                sell_id = result['id']
            # 如果first_result的post参数trade_type是'sell'那么就要创建'sell'单
            else:
                payload.trade_type = 'buy'
                sell_id = first_result['id']
                result = api.entrusts_post(body=payload, async_req=True)
                buy_id = result.order_id

        except ApiException as e:
            if price == '' or market_id == '':
                assert e.status == 400
            return

        user_info = account_api.accounts_account_info_get()
        assert user_info['account_info'].get('account_id')
        result = staff_api.entrusts_get(uid=user_info['account_info'].get('account_id'), status="done", async_req=True)
        ids = [i.id for i in result['items']]
        assert sell_id in ids
        assert buy_id in ids

        # 测试交易所获取委托列表
        result = staff_api.entrusts_get(entrust_id=buy_id, status="done", async_req=True)
        assert result.items.id == buy_id

        fee_result = staff_api.fee_history_get(uid=user_info['account_info'].get('account_id'), status="done")
        fee_ids_map = {i.trade_history_id: i.fee_yield_amount for i in fee_result['items']}
        for k, v in fee_ids_map.items():
            r = staff_api.trade_history_get(trade_history_id=k, async_req=True)
            assert r.items.buyer_fee == v
            r2 = tenant_api.exchanges_trade_history_get(trade_id=k, async_req=True)
            assert r2.items.buyerFee == v
            tenant_fee_r = tenant_api.exchanges_fee_history_get(trade_id=k, async_req=True)
            assert tenant_fee_r.items.fee_yield_amount == v

        payload.price = 10**8
        payload.trade_type = 'sell'
        result = api.entrusts_post(body=payload, async_req=True)
        buy_id = result.order_id
        staff_api.entrusts_id_cancel_post(buy_id, async_req=True)
