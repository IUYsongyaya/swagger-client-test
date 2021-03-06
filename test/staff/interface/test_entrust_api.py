# coding: utf-8

"""
    crush 平台接口（用户管理后台端）

    `crush` 平台接口（后台端）  当前接口为 `staff` 端  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: api@crush.team
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""
from datetime import datetime, timedelta
import pytest

import swagger_client.staff
from swagger_client.staff.api.entrust_api import EntrustApi  # noqa: E501
from swagger_client.staff.rest import ApiException

START = 0
SUCCESS_ID = '111'
api = swagger_client.staff.api.entrust_api.EntrustApi()


def pytest_namespace():
    return {'email': "", "password": "", "base_token": "", "phone": ""}


class TestEntrustApi:
    """EntrustApi pytest stubs"""

    @pytest.mark.parametrize("page", [i for i in range(1, 10)])
    @pytest.mark.parametrize("start_at",
                             [(datetime.now() - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M") for i in
                              range(-2, START)])
    @pytest.mark.parametrize("end_at", [datetime.now().strftime("%Y-%m-%d %H:%M")])
    @pytest.mark.parametrize("exchange_id", [])
    @pytest.mark.parametrize("exchange_name", [])
    @pytest.mark.parametrize("entrust_id", [])
    @pytest.mark.parametrize("uid", [])
    @pytest.mark.parametrize("entrust_type", ["all", "limit", "market", "profitLoss", "timeLimit"])
    @pytest.mark.parametrize("trade_type", ["all", "buy", "sell", ""])
    @pytest.mark.parametrize("trading_pair", [])
    @pytest.mark.parametrize("entrust_channel", ["Manual", "API", ""])
    def test_entrusts_get(self, page, start_at, end_at, exchange_id, exchange_name, entrust_id, uid, entrust_type,
                          trade_type, trading_pair, entrust_channel):
        """Test case for entrusts_get
        """
        payload = {
            "async_req": True,
            "page": page,
            "start_at": start_at,
            "end_at": end_at,
            "exchange_id": exchange_id,
            "exchange_name": exchange_name,
            "entrust_id": entrust_id,
            "uid": uid,
            "entrust_type": entrust_type,
            "trade_type": trade_type,
            "trading_pair": trading_pair,
            "entrust_channel": entrust_channel
        }
        result = api.entrusts_get(**payload)
        assert result['items']

    @pytest.mark.parametrize("entrust_id", [SUCCESS_ID, SUCCESS_ID, ""])
    def test_entrusts_id_cancel_post(self, entrust_id):
        """Test case for entrusts_id_cancel_post

        撤消委托单  # noqa: E501
        """
        try:
            api.entrusts_id_cancel_post(entrust_id)
        except ApiException as e:
            if entrust_id:
                assert e.status == 500  # 撤销过的ID会撤销失败
            else:
                assert e.status == 404  # 指定的委托单不存在

    @pytest.mark.parametrize("page", [i for i in range(1, 10)])
    @pytest.mark.parametrize("start_at",
                             [(datetime.now() - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M") for i in
                              range(-2, START)])
    @pytest.mark.parametrize("end_at", [datetime.now().strftime("%Y-%m-%d %H:%M")])
    @pytest.mark.parametrize("trade_history_id", [])
    @pytest.mark.parametrize("account_id", [])
    @pytest.mark.parametrize('market_id', [])
    def test_fee_history_get(self, page, start_at, end_at, market_id, trade_history_id, account_id):
        """Test case for fee_history_get

        获取手续费记录列表  # noqa: E501
        """
        payload = {
            "async_req": True,
            "page": page,
            "start_at": start_at,
            "end_at": end_at,
            "trade_history_id": trade_history_id,
            "account_id": account_id,
            "market_id": market_id,
        }
        result = api.fee_history_get(**payload)
        assert result['items']

    @pytest.mark.parametrize("page", [i for i in range(1, 10)])
    @pytest.mark.parametrize("start_at",
                             [(datetime.now() - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M") for i in
                              range(-2, START)])
    @pytest.mark.parametrize("end_at", [datetime.now().strftime("%Y-%m-%d %H:%M")])
    @pytest.mark.parametrize("trade_history_id", [])
    @pytest.mark.parametrize("exchange_id", [])
    @pytest.mark.parametrize("exchange_name", [])
    @pytest.mark.parametrize("uid", [])
    @pytest.mark.parametrize('trading_pair', [])
    def test_trade_history_get(self, page, start_at, end_at, trade_history_id, exchange_id, exchange_name, uid,
                               trading_pair):
        """Test case for trade_history_get
        """
        payload = {
            "async_req": True,
            "page": page,
            "start_at": start_at,
            "end_at": end_at,
            "exchange_id": exchange_id,
            "exchange_name": exchange_name,
            "trade_history_id": trade_history_id,
            "uid": uid,
            "trading_pair": trading_pair,
        }
        try:
            result = api.trade_history_get(**payload)
            assert result['items']
        except ApiException as e:
            assert e.status == 404


if __name__ == '__main__':
    pytest.main()
