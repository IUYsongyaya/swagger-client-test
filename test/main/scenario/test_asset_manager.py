#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_asset_manager.py
@time: 2018/11/20
"""
import uuid

import pytest
from faker import Faker

from common.utils import PlatformManager, get_random_id_number
from common.certification_verify import individual_verify
from common.account_sign import register_with_login, get_admin_token, set_login_status
from swagger_client.main.models import PostMessageEnableRequest
from swagger_client.staff.api.asset_management_api import AssetManagementApi
from test.main.scenario.venture_prepare import (recharge_notify,
                                                withdraw_notify,
                                                create_venture)

DEFAULT_VERIFY_CODE = "666666"


class TestAssetManager:
    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_get_asset(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_assets_get()
        assert isinstance(res.asset_info, list)
        assert isinstance(res.estimates.usdt, str)
        assert isinstance(res.estimates.cny, str)

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_get_asset(self, platform):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        try:
            asset_api.asset_mgmt_assets_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录时获取账户资产,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_get_single_asset(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        try:
            asset_api.asset_mgmt_assets_coin_id_get(coin_id="1")
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录获取单个币种资产,java接口异常"
        register_with_login(platform, with_login, [asset_api])
        try:
            asset_api.asset_mgmt_assets_coin_id_get(coin_id="9999999")
        except manager.api_exception as e:
            assert e.status == 404
        else:
            assert False, "获取不存在的单个币种资产, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_get_single_balance(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        try:
            asset_api.asset_mgmt_balance_coin_id_get(coin_id="1")
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录获取单个币种余额,java接口异常"
        register_with_login(platform, with_login, [asset_api])
        try:
            asset_api.asset_mgmt_balance_coin_id_get(coin_id="1")
        except manager.api_exception as e:
            assert e.status == 404
        else:
            assert False, "获取不存在的单个币种余额, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_set_asset_password(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        try:
            asset_api.asset_mgmt_asset_password_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录获取是否设置资金密码时,java接口异常"
        user = register_with_login(platform, with_login,
                                   [asset_api, verify_api])
        res = asset_api.asset_mgmt_asset_password_get()
        assert not res.is_set
        faker = Faker()
        assert_password = faker.password()
        try:
            asset_api.asset_mgmt_asset_password_put(body={
                "password": user.get("password"),
                "traPassword": assert_password,
                "baseToken": ""})
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "没有通过极验就修改资金密码"

        res = manager.verify({
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:" + user.get("email"),
            "code": DEFAULT_VERIFY_CODE,
            "type": "edit_asset_pwd"})
        base_token = res.token
        asset_api.asset_mgmt_asset_password_put(body={
            "password": user.get("password"),
            "traPassword": assert_password,
            "baseToken": base_token})
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_change_asset_password(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        faker = Faker()
        asset_password = faker.password()
        user = register_with_login(platform, with_login, [asset_api,
                                                          verify_api])
        res = asset_api.asset_mgmt_asset_password_get()
        assert not res.is_set

        # 添加资金密码后修改密码
        res = manager.verify({
                "challenge": "fjdks",
                "seccode": "jfkdlfd",
                "validate": "kfld;s",
                "account": "mailto:" + user.get("email"),
                "code": DEFAULT_VERIFY_CODE,
                "secondCode": "fdsaff",
                "type": "edit_asset_pwd"})
        base_token = res.token
        asset_api.asset_mgmt_asset_password_put(body={
            "password": user.get("password"),
            "traPassword": asset_password,
            "baseToken": base_token})
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set
        res = manager.verify({
                "challenge": "fjdks",
                "seccode": "jfkdlfd",
                "validate": "kfld;s",
                "account": "mailto:" + user.get("email"),
                "code": DEFAULT_VERIFY_CODE,
                "secondCode": "fdsaff",
                "type": "edit_asset_pwd"})
        base_token = res.token
        change_password = faker.password()
        asset_api.asset_mgmt_asset_password_put({
            "password": user.get("password"),
            "traPassword": change_password,
            "baseToken": base_token})

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_check_asset_password(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [asset_api,
                                                          verify_api])
        faker = Faker()
        asset_password = faker.password()
        # 未添加资金密码后直接检查密码
        try:
            asset_api.asset_mgmt_asset_password_check_post(
                body={"traPassword": asset_password,
                      "coinId": "1",
                      "amount": "1"})
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "未添加资金密码后检查密码,java接口异常"
        # 添加资金密码
        res = manager.verify({
                "challenge": "fjdks",
                "seccode": "jfkdlfd",
                "validate": "kfld;s",
                "account": "mailto:" + user.get("email"),
                "code": DEFAULT_VERIFY_CODE,
                "secondCode": "fdsaff",
                "type": "edit_asset_pwd"})
        base_token = res.token
        asset_api.asset_mgmt_asset_password_put(body={
            "password": user.get("password"),
            "traPassword": asset_password,
            "baseToken": base_token})
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set

        # 检查资金密码
        res = asset_api.asset_mgmt_asset_password_check_post(
            body={"traPassword": asset_password,
                  "coinId": "1",
                  "amount": "1"})
        assert isinstance(res.token, str)

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_get_incoming_history(self, platform):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        # 未登录获取收支记录
        try:
            asset_api.asset_mgmt_journals_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录获取收支记录,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_get_incoming_history(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_journals_get()
        assert res.meta.total_page == 0
        assert res.meta.requested_page == 1
        assert res.meta.page == 1
        assert not res.query.subject_type
        assert not res.query.coin_id
        assert res.items == list()

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_get_no_exist_incoming_history(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_journals_get(page=100, page_size=100,
                                                subject_type="COMMISSION")
        assert res.meta.total_page == 0
        assert res.meta.requested_page == 100
        assert res.meta.page == 100
        assert res.query.subject_type == "COMMISSION"
        assert not res.query.coin_id
        assert res.items == list()

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_get_recharge_history(self, platform):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        try:
            asset_api.asset_mgmt_recharge_records_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录时获取账户充值记录, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_get_recharge_history(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_recharge_records_get()
        assert res.meta.total_page == 0
        assert res.meta.requested_page == 1
        assert res.meta.total_count == 0
        assert not res.query.status
        assert not res.query.coin_id
        assert res.items == list()

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_get_no_exist_recharge_history(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_recharge_records_get(page=100,
                                                        page_size=100,
                                                        status="CONFIRMING",
                                                        coin_id="1")
        assert res.meta.total_page == 0
        assert res.meta.requested_page == 100
        assert res.query.status == "CONFIRMING"
        assert res.query.coin_id == "1"
        assert res.items == list()

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_get_withdraw_history(self, platform):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        try:
            asset_api.asset_mgmt_withdraw_records_get()
        except manager.api_exception as e:
            print(e.body)
            assert e.status == 403
        else:
            assert False, "未登录时获取提币记录,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_get_withdraw_history(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_withdraw_records_get()
        assert res.meta.requested_page == 1
        assert res.meta.total_page == 0
        # assert not res.query.status
        # assert not res.query.coin_id
        assert res.items == list()

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_get_no_exist_withdraw_history(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_withdraw_records_get(page=100,
                                                        page_size=100,
                                                        coin_id="1",
                                                        status="CONFIRMING")
        assert res.meta.requested_page == 100
        assert res.meta.total_page == 0
        assert res.query.status == "CONFIRMING"
        assert res.query.coin_id == "1"
        assert res.items == list()

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_get_coin_info(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        try:
            asset_api.asset_mgmt_coins_coin_id_get("500")
        except manager.api_exception as e:
            assert e.status == 404
        else:
            assert False, "获取不存在的币种信息时,java接口报错"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_recharge_list(self, platform):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        try:
            asset_api.asset_mgmt_coins_rechargeable_lists_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录时获取充值列表, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_recharge_list(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_coins_rechargeable_lists_get()
        assert isinstance(res, list)

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_recharge_address(self, platform):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        try:
            asset_api.asset_mgmt_recharge_addresses_get(coin_id="1")
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录时获取冲币地址, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_error_field_recharge_address(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        try:
            asset_api.asset_mgmt_recharge_addresses_get(coin_id=1)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "获取指定币种的冲币地址时填写错误类型的币种id, java接口异常"

    # @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    # def test_normal_recharge_address(self, platform, with_login):
    #     manager = PlatformManager(platform)
    #     asset_api = manager.asset_api
    #     register_with_login(platform, with_login, [asset_api])
    #     res = asset_api.asset_mgmt_recharge_addresses_get(coin_id="1")
    #     assert res.coin_id == "1"
    #     assert res.coin_address == str()

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_withdraw_list(self, platform):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        res = asset_api.asset_mgmt_coins_withdrawable_lists_get()
        assert isinstance(res, list)

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_withdraw_list(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_coins_withdrawable_lists_get()
        assert isinstance(res, list)

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_withdraw_address(self, platform, with_login):
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        # 未登录获取提币地址
        try:
            asset_api.asset_mgmt_withdraw_addresses_get(coin_id="1")
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录获取提币地址, java接口异常"

        # 未添加获取提币地址
        register_with_login(platform, with_login, [asset_api])
        res = asset_api.asset_mgmt_withdraw_addresses_get(coin_id="1")
        assert not res

        # 添加提币地址后获取提币地址
        asset_api.asset_mgmt_withdraw_addresses_post(
            body={"coinId": "1",
                  "remark": "remark",
                  "address": "new_withdraw_address"})
        res = asset_api.asset_mgmt_withdraw_addresses_get(coin_id="1")
        withdraw_address = res.pop()
        assert withdraw_address["coinId"] == "1"
        assert withdraw_address["remark"] == "remark"
        assert withdraw_address["address"] == "new_withdraw_address"
        address_id = withdraw_address["id"]
        asset_api.asset_mgmt_withdraw_addresses_id_put(id=address_id)
        res = asset_api.asset_mgmt_withdraw_addresses_get(coin_id="1")
        assert not res

    def test_limit_asset(self):
        """
        /asset-mgmt/assets/restriction查询资产限制的用户
        """
        admin_token = get_admin_token()
        api = AssetManagementApi()
        set_login_status(api, admin_token)

        api.asset_mgmt_assets_restriction_id_put(id="463", body={
            "withdraw": True,
            "otc": True
        })
        res = api.asset_mgmt_assets_restriction_id_get(id="463")
        assert res.otc
        assert res.withdraw
        res = api.asset_mgmt_assets_restriction_get(
            withdraw=True,
            otc=True)
        assert res.meta.requested_page == 1
        assert res.query.withdraw
        api.asset_mgmt_assets_restriction_id_delete(id="463")
        res = api.asset_mgmt_assets_restriction_get(withdraw=True, otc=True)
        assert not res.items

    def test_revenue(self):
        admin_token = get_admin_token()
        api = AssetManagementApi()
        set_login_status(api, admin_token)
        res = api.asset_mgmt_revenue_get(coin_id="1")
        assert res.meta.requested_page == 1
        assert res.query.coin_id == "1"

    # 接口弃用
    # def test_commission(self):
    #     admin_token = get_admin_token()
    #     api = AssetManagementApi()
    #     set_login_status(api, admin_token)
    #     try:
    #         api.asset_mgmt_commission_account_id_get(account_id="99999")
    #     except ApiException as e:
    #         assert e.status == 404
    #     else:
    #         assert False
    #     # 交易返佣管理
    #     res = api.asset_mgmt_commission_get()
    #     print(res)

    def test_get_coin_config(self):
        (coin_id, coin_id_, coin_name,
         rc_confirmed_time, wc_confirmed_time) = create_venture()
        admin_token = get_admin_token()
        api = AssetManagementApi()
        set_login_status(api, admin_token)
        # 设置充提币
        api.asset_mgmt_coins_id_recharge_put(id=coin_id, rechargeable=True)
        api.asset_mgmt_coins_id_withdraw_put(id=coin_id, withdrawable=True)
        # 获取币种列表
        res = api.asset_mgmt_coins_get(coin_name=coin_name)
        assert len(res.items) == 1
        coin_config = res.items.pop()
        assert coin_config.coin_name == coin_name.upper()
        assert coin_config.coin_id == coin_id_
        assert coin_config.id == coin_id
        assert coin_config.rechargeable
        assert coin_config.withdrawable
        assert coin_config.initialized
        # 通过id获取币种配置
        res = api.asset_mgmt_coins_id_get(id=coin_id)
        assert res.id == coin_id
        # 获取币种提示信息
        api.asset_mgmt_coins_id_prompt_get(id=coin_id)
        # 修改币种提示信息
        api.asset_mgmt_coins_id_prompt_put(
            id=coin_id, body={"prompt": "prompt"})
        # 获取币种提示信息
        res = api.asset_mgmt_coins_id_prompt_get(id=coin_id)
        assert res.prompt == "prompt"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_recharge_withdraw(self, platform, with_login):
        (coin_id, coin_id_, coin_name,
         rc_confirmed_time, wc_confirmed_time) = create_venture()
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        account_api = manager.account_api
        user = register_with_login(platform, with_login,
                                   [asset_api, verify_api, account_api])
        admin_token = get_admin_token()
        asset_manage_api = AssetManagementApi()
        set_login_status(asset_manage_api, admin_token)
        # 获取账户信息
        res = account_api.accounts_account_info_get()
        account_id = res.account_info.account_id
        # 账户实名认证
        id_number = get_random_id_number()
        individual_verify(platform, id_number, user["token"])
        # 设置可以充币
        asset_manage_api.asset_mgmt_coins_id_recharge_put(
            id=coin_id, rechargeable=True)
        # 获取冲币地址
        res = asset_api.asset_mgmt_recharge_addresses_get(coin_id=coin_id_)
        assert res.coin_id == coin_id_
        # 通知冲币
        recharge_address = res.coin_address
        recharge_amount = 100
        recharge_confirmed_times = 30
        recharge_notify(coin_name, recharge_confirmed_times,
                        recharge_address, amount=recharge_amount)
        # 获取账户冲币记录
        res = asset_api.asset_mgmt_recharge_records_get(status="SUCCEED")
        assert res.meta.total_count == 1
        item = res.items.pop()
        assert item.coin_id == coin_id_
        assert item.status == "SUCCEED"
        assert float(item.amount) == recharge_amount
        assert item.address == '{}_recharge_from_address'.format(coin_name)
        assert item.confirmed_times == recharge_confirmed_times
        assert item.confirmation_number == rc_confirmed_time

        # 从后台获取冲币记录
        res = asset_manage_api.get_recharge_list(
            account_id=account_id, coin_id=coin_id_, status="SUCCEED")
        assert len(res.items) == 1
        item = res.items.pop()
        assert item.coin_id == coin_id_
        assert item.confirmed_times == recharge_confirmed_times
        assert item.confirmation_number == rc_confirmed_time
        assert item.address == '{}_recharge_from_address'.format(coin_name)
        assert item.status == "SUCCEED"
        
        # 获取账户资产
        res = asset_api.asset_mgmt_assets_get()
        for i in res.asset_info:
            if i.coin_id == coin_id_:
                assert float(i.total) == recharge_amount
                assert float(i.balance) == recharge_amount
                break
        else:
            assert False, "未发现冲币币种余额"
        # 获取指定币种余额
        res = asset_api.asset_mgmt_balance_coin_id_get(coin_id=coin_id_)
        assert float(res.balance) == recharge_amount

        # 获取单个币种资产
        res = asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id_)
        assert res.coin_id == coin_id_
        assert float(res.balance) == recharge_amount
        assert float(res.total) == recharge_amount
        assert float(res.frozen) == 0

        # 通知冲币失败
        failed = -1
        recharge_notify(coin_name, 1, recharge_address, failed)

        # 获取账户失败的冲币记录
        res = asset_api.asset_mgmt_recharge_records_get(status="FAILED")
        assert res.meta.total_count == 1
        item = res.items.pop()
        assert item.coin_id == coin_id_
        assert item.status == "FAILED"
        assert float(item.amount) == recharge_amount
        assert item.address == '{}_recharge_from_address'.format(coin_name)
        assert item.confirmed_times == 1
        assert item.confirmation_number == rc_confirmed_time

        # 从后台获取冲币记录
        res = asset_manage_api.get_recharge_list(
            account_id=account_id, coin_id=coin_id_, status="FAILED")
        assert len(res.items) == 1
        item = res.items.pop()
        assert item.coin_id == coin_id_
        assert item.confirmed_times == 1
        assert item.confirmation_number == rc_confirmed_time
        assert item.address == '{}_recharge_from_address'.format(coin_name)
        assert item.status == "FAILED"

        # 通知确认中的冲币
        confirming = 0
        recharge_notify(coin_name, 2, recharge_address, confirming)

        # 获取账户冲币记录
        res = asset_api.asset_mgmt_recharge_records_get(status="CONFIRMING")
        assert res.meta.total_count == 1
        item = res.items.pop()
        assert item.coin_id == coin_id_
        assert item.confirmed_times == 2
        assert item.status == "CONFIRMING"
        assert float(item.amount) == recharge_amount
        assert item.address == '{}_recharge_from_address'.format(coin_name)
        assert item.confirmation_number == rc_confirmed_time

        # 从后台获取冲币记录
        res = asset_manage_api.get_recharge_list(
            account_id=account_id, coin_id=coin_id_, status="CONFIRMING")
        assert len(res.items) == 1
        item = res.items.pop()
        assert item.coin_id == coin_id_
        assert item.confirmed_times == 2
        assert item.confirmation_number == rc_confirmed_time
        assert item.address == '{}_recharge_from_address'.format(coin_name)
        assert item.status == "CONFIRMING"

        # 获取单个币种资产
        res = asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id_)
        assert res.coin_id == coin_id_
        assert float(res.balance) == recharge_amount
        assert float(res.total) == recharge_amount
        assert float(res.frozen) == 0

        # 新增提币地址
        withdraw_address_1 = "{}_{}".format(coin_name, uuid.uuid4().hex)
        withdraw_address_2 = "{}_{}".format(coin_name, uuid.uuid4().hex)
        asset_api.asset_mgmt_withdraw_addresses_post(
            body={"coinId": coin_id_,
                  "remark": "remark_1",
                  "address": withdraw_address_1})
        asset_api.asset_mgmt_withdraw_addresses_post(
            body={"coinId": coin_id_,
                  "remark": "remark_2",
                  "address": withdraw_address_2})

        # 获取所有提币地址
        res = asset_api.asset_mgmt_withdraw_addresses_get(coin_id=coin_id_)
        assert len(res) == 2
        for item in res:
            assert item["coinId"] == coin_id_
        delete_address = res.pop()
        delete_address_id = delete_address["id"]

        # 从后台获取提币地址
        res = asset_manage_api.asset_mgmt_assets_withdraw_address_get(
            account_id=account_id)
        assert len(res.items) == 2
        for i in res.items:
            assert i.address in [withdraw_address_1, withdraw_address_2]

        # 获取所有提币地址
        res = asset_api.asset_mgmt_withdraw_addresses_all_get()
        assert len(res) == 2
        for i in res:
            assert isinstance(i["id"], str)
            assert isinstance(i["coinName"], str)
            assert i["address"] in [withdraw_address_1, withdraw_address_2]

        # 删除提币地址
        asset_api.asset_mgmt_withdraw_addresses_id_put(id=delete_address_id)

        # 删除后获取所有提币地址
        res = asset_api.asset_mgmt_withdraw_addresses_get(coin_id=coin_id_)
        assert len(res) == 1

        # 删除不存在的提笔地址
        try:
            asset_api.asset_mgmt_withdraw_addresses_id_put(id="9999")
        except manager.api_exception as e:
            assert e.status == 404
        else:
            assert False, "删除不存在的提币地址时,java接口异常"

        # 设置资金密码
        faker = Faker()
        asset_password = faker.password()
        res = manager.verify({
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:" + user.get("email"),
            "code": DEFAULT_VERIFY_CODE,
            "type": "edit_asset_pwd"})
        base_token = res.token
        asset_api.asset_mgmt_asset_password_put(body={
            "password": user.get("password"),
            "traPassword": asset_password,
            "baseToken": base_token})

        # 从后台查询是否设置资金密码
        res = asset_manage_api.asset_mgmt_asset_password_has_set_account_id_get(
            account_id=account_id)
        assert res.is_set

        # 修改可提币配置
        asset_manage_api.asset_mgmt_coins_id_withdraw_put(
            id=coin_id, withdrawable=True)

        withdraw_amount = int(50)
        withdraw_fee = 0.15
        # 资金密码校验
        res = asset_api.asset_mgmt_asset_password_check_post(
            body={"traPassword": asset_password, "coinId": coin_id_,
                  "amount": withdraw_amount})
        assert res.token

        # 提币
        res = manager.verify({
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:" + user.get("email"),
            "code": DEFAULT_VERIFY_CODE,
            "type": "withdraw"})
        withdraw_address_3 = "{}_{}".format(coin_name, uuid.uuid4().hex)
        asset_api.asset_mgmt_withdraw_post(body={
            "traPassword": asset_password,
            "baseToken": res.token,
            "coinId": coin_id_,
            "amount": withdraw_amount,
            "remark": "withdraw_remark",
            "addressTag": "address_tag",
            "address": withdraw_address_3,
            "isSaveAddress": True
        })
        # 获取钱包资金
        res = asset_api.asset_mgmt_assets_get()
        for i in res.asset_info:
            if i.coin_id == coin_id_:
                assert float(i.total) == recharge_amount
                assert float(i.balance) == recharge_amount - withdraw_amount
                break
        else:
            assert False, "未发现冲币币种余额"

        # # 从平台获取提币记录
        res = asset_api.asset_mgmt_withdraw_records_get(status="WAIT_REVIEW")
        assert res.meta.total_count == 1
        item = res.items.pop()
        assert item.coin_id == coin_id_
        assert float(item.amount) == withdraw_amount
        assert float(item.fee) == withdraw_fee
        assert item.address == withdraw_address_3
        assert item.status == "WAIT_REVIEW"

        # 重新获取提币地址
        res = asset_api.asset_mgmt_withdraw_addresses_get(coin_id=coin_id_)
        for i in res:
            assert i["coinId"] == coin_id_
            assert i["address"] in [withdraw_address_3,
                                    withdraw_address_1,
                                    withdraw_address_2]

        # 从管理后台获取提币记录
        res = asset_manage_api.get_withdraw_list(to_address=withdraw_address_3)
        assert res.meta.total_count == 1
        item = res.items.pop()
        withdraw_record_id = item.id
        assert item.coin_id == coin_id_
        assert item.status == "WAIT_REVIEW"
        assert item.confirmation_number == wc_confirmed_time
        assert not item.confirmed_times
        assert float(item.amount) == withdraw_amount
        assert float(item.fee) == withdraw_fee
        assert item.address == withdraw_address_3

        # 从后台获取提币详情
        res = asset_manage_api.asset_mgmt_withdraw_records_id_get(
            id=withdraw_record_id)
        assert res.id == withdraw_record_id
        assert res.email == user["email"]
        assert res.coin_id == coin_id_
        assert float(item.fee) == withdraw_fee
        assert res.status == "WAIT_REVIEW"
        assert res.address == withdraw_address_3

        # # 撤销提币
        # asset_api.asset_mgmt_withdraw_id_cancel_post(id=withdraw_record_id)
        #
        # # 从后台获取提币详情
        # res = asset_manage_api.asset_mgmt_withdraw_records_id_get(
        #     id=withdraw_record_id)
        # assert res.id == withdraw_record_id
        # # assert res.email == user["email"]
        # assert res.coin_id == "66"
        # assert float(item.fee) == 0.15
        # assert res.status == "CANCEL"
        # assert res.address == withdraw_address_3
        #
        # # 查看账户余额
        # res = asset_api.asset_mgmt_assets_get()
        # for i in res.asset_info:
        #     if i.coin_id == "66":
        #         assert float(i.total) == 100
        #         assert float(i.balance) == 100
        #         break
        # else:
        #     assert False, "未发现冲币币种余额"
        #
        # # 获取单个币种资产
        # res = asset_api.asset_mgmt_assets_coin_id_get(coin_id="66")
        # assert res.coin_id == "66"
        # assert float(res.balance) == 100
        # assert float(res.total) == 100
        # assert float(res.frozen) == 0

        # 后台一审
        asset_manage_api.asset_mgmt_withdraw_id_first_audit_post(
            id=withdraw_record_id,
            body={"result": True, "remark": "withdraw_first_remark"})

        # 从管理后台获取提币记录
        res = asset_manage_api.get_withdraw_list(to_address=withdraw_address_3)
        assert res.meta.total_count == 1
        item = res.items.pop()
        withdraw_record_id = item.id
        assert item.coin_id == coin_id_
        assert item.status == "FIRST_REVIEW"
        assert item.confirmation_number == wc_confirmed_time
        assert not item.confirmed_times
        assert float(item.amount) == withdraw_amount
        assert float(item.fee) == withdraw_fee
        assert item.address == withdraw_address_3

        # 从后台获取提币详情
        res = asset_manage_api.asset_mgmt_withdraw_records_id_get(
            id=withdraw_record_id)
        assert res.id == withdraw_record_id
        # assert res.email == user["email"]
        assert res.coin_id == coin_id_
        assert float(item.fee) == withdraw_fee
        assert res.status == "FIRST_REVIEW"
        assert res.address == withdraw_address_3

        # 后台二审
        asset_manage_api.asset_mgmt_withdraw_id_second_audit_post(
            id=withdraw_record_id,
            body={"result": True, "remark": "withdraw_second_remark"})

        # 从管理后台获取提币记录
        res = asset_manage_api.get_withdraw_list(to_address=withdraw_address_3)
        assert res.meta.total_count == 1
        item = res.items.pop()
        withdraw_record_id = item.id
        assert item.coin_id == coin_id_
        assert item.status == "CONFIRMING"
        assert item.confirmation_number == wc_confirmed_time
        assert not item.confirmed_times
        assert float(item.amount) == withdraw_amount
        assert float(item.fee) == withdraw_fee
        assert item.address == withdraw_address_3

        # 从后台获取提币详情
        res = asset_manage_api.asset_mgmt_withdraw_records_id_get(
            id=withdraw_record_id)
        assert res.id == withdraw_record_id
        # assert res.email == user["email"]
        assert res.coin_id == coin_id_
        assert float(item.fee) == withdraw_fee
        assert res.status == "CONFIRMING"
        assert res.address == withdraw_address_3

        # 通知提币
        withdraw_confirmed_time = 30
        success = 1
        tx_id = "{}_{}_{}".format(coin_name,
                                  withdraw_address_3, withdraw_amount)
        withdraw_notify(txid=tx_id, status=success,
                        confirmations=withdraw_confirmed_time)

        # 查看账户余额
        res = asset_api.asset_mgmt_assets_get()
        for i in res.asset_info:
            if i.coin_id == coin_id_:
                assert float(i.total) == float(recharge_amount - withdraw_amount)
                assert float(i.balance) == float(recharge_amount - withdraw_amount)
                break
        else:
            assert False, "未发现冲币币种余额"

        # 获取单个币种资产
        res = asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id_)
        assert res.coin_id == coin_id_
        assert float(res.balance) == recharge_amount - withdraw_amount
        assert float(res.total) == recharge_amount - withdraw_amount
        assert float(res.frozen) == 0

        # 获取提币总额
        res = asset_api.asset_mgmt_withdraw_withdraw_total_get(coin_id=coin_id_)
        assert float(res.total) == recharge_amount - withdraw_amount
        
        # 后台重置资金密码
        asset_manage_api.asset_mgmt_asset_password_reset_id_put(id=account_id)

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_withdraw_patch(self, platform, with_login):
        (coin_id, coin_id_, coin_name,
         rc_confirmed_time, wc_confirmed_time) = create_venture()
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        account_api = manager.account_api
        user = register_with_login(platform, with_login,
                                   [asset_api, verify_api, account_api])
        admin_token = get_admin_token()
        asset_manage_api = AssetManagementApi()
        set_login_status(asset_manage_api, admin_token)
        # 账户实名认证
        id_number = get_random_id_number()
        individual_verify(platform, id_number, user["token"])
        # 设置可以充币
        asset_manage_api.asset_mgmt_coins_id_recharge_put(
            id=coin_id, rechargeable=True)
        # 获取冲币地址
        res = asset_api.asset_mgmt_recharge_addresses_get(coin_id=coin_id_)
        assert res.coin_id == coin_id_
        # 通知冲币
        recharge_address = res.coin_address
        recharge_amount = 100
        recharge_notify(coin_name, 30, recharge_address, amount=recharge_amount)
        # 设置资金密码
        faker = Faker()
        asset_password = faker.password()
        res = manager.verify({
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:" + user.get("email"),
            "code": DEFAULT_VERIFY_CODE,
            "type": "edit_asset_pwd"})
        base_token = res.token
        asset_api.asset_mgmt_asset_password_put(body={
            "password": user.get("password"),
            "traPassword": asset_password,
            "baseToken": base_token})
        # 修改可提币配置
        asset_manage_api.asset_mgmt_coins_id_withdraw_put(
            id=coin_id, withdrawable=True)

        # 资金密码校验
        withdraw_amount = int(50)
        asset_api.asset_mgmt_asset_password_check_post(
            body={"traPassword": asset_password, "coinId": coin_id_,
                  "amount": withdraw_amount})

        # 提币
        res = manager.verify({
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:" + user.get("email"),
            "code": DEFAULT_VERIFY_CODE,
            "type": "withdraw"})
        withdraw_address = "{}_{}".format(coin_name, uuid.uuid4().hex)

        asset_api.asset_mgmt_withdraw_post(body={
            "traPassword": asset_password,
            "baseToken": res.token,
            "coinId": coin_id_,
            "amount": withdraw_amount,
            "remark": "withdraw_remark",
            "addressTag": "address_tag",
            "address": withdraw_address,
            "isSaveAddress": True
        })
        # 从管理后台获取提币记录
        res = asset_manage_api.get_withdraw_list(to_address=withdraw_address)
        item = res.items.pop()
        withdraw_record_id = item.id
        # 后台一审
        asset_manage_api.asset_mgmt_withdraw_id_first_audit_post(
            id=withdraw_record_id,
            body={"result": True, "remark": "withdraw_first_remark"})
        # 后台二审
        asset_manage_api.asset_mgmt_withdraw_id_second_audit_post(
            id=withdraw_record_id,
            body={"result": True, "remark": "withdraw_second_remark"})
        # 通知提币(该笔记录为失败状态)
        tx_id = "{}_{}_{}".format(coin_name, withdraw_address, withdraw_amount)
        withdraw_notify(txid=tx_id, status=-1, confirmations=30)
        # 从管理后台获取提币记录
        res = asset_manage_api.get_withdraw_list(to_address=withdraw_address)
        item = res.items.pop()
        withdraw_record_id = item.id
        assert item.status == "FAILED"
        assert item.confirmation_number == 2
        assert item.confirmed_times == 30
        
        # # 自动补单提币
        # asset_manage_api.asset_mgmt_withdraw_patch_id_post(
        #     id=withdraw_record_id, body={"patchType": "AUTO"})
        #
        # # 通知提币(该笔记录为失败状态)
        # tx_id = "{}_{}_{}".format("YSSKUR", withdraw_address, withdraw_amount)
        # withdraw_notify(txid=tx_id, status=-1, confirmations=20)
        #
        # # 从管理后台获取提币记录
        # res = asset_manage_api.get_withdraw_list(to_address=withdraw_address)
        # item = res.withdraw_records.pop()
        # withdraw_record_id = item.id
        # assert item.status == "FAILED"
        # assert item.confirmation_number == 2
        # assert item.confirmed_times == 20
        
        # 手动补单
        tx_id = uuid.uuid4().hex
        asset_manage_api.asset_mgmt_withdraw_patch_id_post(
            id=withdraw_record_id, body={"patchType": "MANUAL",
                                         "txid": tx_id})

        # 从管理后台获取提币记录
        res = asset_manage_api.get_withdraw_list(to_address=withdraw_address,
                                                 status="PATCH")
        item = res.items.pop()
        assert item.status == "PATCH"
        assert item.confirmation_number == 2
        assert item.confirmed_times == 30

        # 获取单个币种资产
        res = asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id_)
        assert res.coin_id == coin_id_
        assert float(res.balance) == recharge_amount - withdraw_amount
        assert float(res.total) == recharge_amount - withdraw_amount
        assert float(res.frozen) == 0

    @pytest.mark.parametrize("platform", ["main"])
    def test_withdraw_info(self, platform, with_login):
        (coin_id, coin_id_, coin_name,
         rc_confirmed_time, wc_confirmed_time) = create_venture()
        manager = PlatformManager(platform)
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        account_api = manager.account_api
        user = register_with_login(platform, with_login,
                                   [asset_api, verify_api, account_api])
        admin_token = get_admin_token()
        asset_manage_api = AssetManagementApi()
        set_login_status(asset_manage_api, admin_token)
        # 账户实名认证
        id_number = get_random_id_number()
        individual_verify(platform, id_number, user["token"])
        # 设置可以充币
        asset_manage_api.asset_mgmt_coins_id_recharge_put(
            id=coin_id, rechargeable=True)
        # 获取冲币地址
        res = asset_api.asset_mgmt_recharge_addresses_get(coin_id=coin_id_)
        assert res.coin_id == coin_id_
        # 通知冲币
        recharge_address = res.coin_address
        recharge_amount = 100
        recharge_notify(coin_name, 30, recharge_address, amount=recharge_amount)
        # 设置资金密码
        faker = Faker()
        asset_password = faker.password()
        res = manager.verify({
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:" + user.get("email"),
            "code": DEFAULT_VERIFY_CODE,
            "type": "edit_asset_pwd"})
        base_token = res.token
        asset_api.asset_mgmt_asset_password_put(body={
            "password": user.get("password"),
            "traPassword": asset_password,
            "baseToken": base_token})
        # 修改可提币配置
        asset_manage_api.asset_mgmt_coins_id_withdraw_put(
            id=coin_id, withdrawable=True)
    
        # 资金密码校验
        withdraw_amount = int(50)
        asset_api.asset_mgmt_asset_password_check_post(
            body={"traPassword": asset_password, "coinId": coin_id_,
                  "amount": withdraw_amount})
    
        # 提币
        res = manager.verify({
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:" + user.get("email"),
            "code": DEFAULT_VERIFY_CODE,
            "type": "withdraw"})
        withdraw_address = "{}_{}".format(coin_name, uuid.uuid4().hex)
    
        asset_api.asset_mgmt_withdraw_post(body={
            "traPassword": asset_password,
            "baseToken": res.token,
            "coinId": coin_id_,
            "amount": withdraw_amount,
            "remark": "withdraw_remark",
            "addressTag": "address_tag",
            "address": withdraw_address,
            "isSaveAddress": True
        })
        # 从管理后台获取提币记录
        res = asset_manage_api.get_withdraw_list(to_address=withdraw_address)
        item = res.items.pop()
        withdraw_record_id = item.id
        # 后台一审
        asset_manage_api.asset_mgmt_withdraw_id_first_audit_post(
            id=withdraw_record_id,
            body={"result": True, "remark": "withdraw_first_remark"})
        # 后台二审
        asset_manage_api.asset_mgmt_withdraw_id_second_audit_post(
            id=withdraw_record_id,
            body={"result": True, "remark": "withdraw_second_remark"})
        # 通知提币(该笔记录为失败状态)
        tx_id = "{}_{}_{}".format(coin_name, withdraw_address, withdraw_amount)
        withdraw_notify(txid=tx_id, status=-1, confirmations=30)
    
        # 从管理后台获取提币记录
        res = asset_manage_api.get_withdraw_list(to_address=withdraw_address)
        item = res.items.pop()
        assert item.status == "FAILED"
        assert item.confirmation_number == 2
        assert item.confirmed_times == 30

        # 查看主平台消息列表
        message_list = account_api.get_message_list(page=1, type='main')
        message_res = [i for i in message_list.items if i.status is False]
        message_id = message_res[0].id
        # 设置消息为已读
        payload = PostMessageEnableRequest()
        payload.id = message_id
        account_api.messages_put(payload)
        # 查看主平台消息列表
        mess_res_list = account_api.get_message_list(page=1, type='main')
        message_result = [i.id for i in mess_res_list.items if i.status is True]
        assert message_id in message_result
