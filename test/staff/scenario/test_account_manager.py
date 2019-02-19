#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_account_manager.py
@time: 2018/11/25
"""
import random
import json

from faker import Faker
import pytest

from swagger_client.staff.api import account_management_api
from swagger_client.staff.rest import ApiException
from common.utils import PlatformManager, get_random_id_number
from common.account_sign import register_with_login, get_admin_token
from common.certification_verify import individual_verify, company_verify


DEFAULT_VERIFY_CODE = "666666"


def verify_info(manager, account, verify_type):
    verify_ = {"challenge": "",
               "seccode": "",
               "validate": "",
               "account": "mailto:" + account,
               "code": DEFAULT_VERIFY_CODE,
               "type": verify_type}
    if verify_type in ["alter_phone", "alter_google"]:
        verify_.update({"secondCode": DEFAULT_VERIFY_CODE})
    return manager.verify(verify_)


class TestAccountManager:
    def test_no_login_lock_account(self):
        api = account_management_api.AccountManagementApi()
        try:
            api.accounts_id_lock_account_put(id=str(random.randint(1, 100)),
                                             body={
                                                 "isBlocked": True,
                                                 "blockedReason": "填写的锁定原因"}
                                             )
        except ApiException as e:
            assert e.status == 403
        else:
            assert False, "未登录时后台锁定账户, java接口失败"
            
    def test_lock_no_exist_account(self):
        api = account_management_api.AccountManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        try:
            api.accounts_id_lock_account_put(id="20000",
                                             body={
                                                 "isBlocked": True,
                                                 "blockedReason": "填写的锁定原因"}
                                             )
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "锁定不存在的账户"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_lock_account(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        user = register_with_login(platform, with_login, [account_api])
        
        # 获取用户列表找到该用户id
        api = account_management_api.AccountManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        investors_resp = api.accounts_investors_get(email=user["email"])
        assert investors_resp.meta.requested_page == 1
        assert len(investors_resp.items) > 0
        account = investors_resp.items.pop()
        user_id = account.uid
        assert account.email == user["email"]
        assert account.nationality == user["country_abbreviation"]
        # assert account.auth_type == str()
        # assert account.certificated_id == "user"
        assert not account.is_blocked
        
        # 获取不存在的账户详情
        try:
            api.accounts_accounts_id_get(id=str(500000))
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "获取不存在的账户详情时,java接口异常"
            
        # 获取该测试账户详情
        account_info = api.accounts_accounts_id_get(id=user_id)
        assert account_info.basic_info.email == user["email"]
        assert not account_info.basic_info.is_certified
        assert not account_info.basic_info.is_blocked
        
        # 锁定该测试账户
        api.accounts_id_lock_account_put(id=user_id,
                                         body={
                                             "isBlocked": True,
                                             "blockedReason": "填写的锁定原因"}
                                         )
        
        # 锁定后通过获取列表判断状态
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        investors_resp = api.accounts_investors_get(email=user["email"])
        account = investors_resp.items.pop()
        assert account.is_blocked
        # 锁定后通过详情判断账户状态
        account_info = api.accounts_accounts_id_get(id=user_id)
        assert account_info.basic_info.is_blocked
        # # 判断登录的token是否过期
        # try:
        #     account_api.accounts_verify_isvalid_post()
        # except manager.api_exception as e:
        #     assert e.status == 403
        # else:
        #     assert False, "锁定账户后验证token有效, java接口异常"
        # 尝试登录来判断状态
        try:
            with_login(platform, list(), account=user["email"],
                       password=user["password"])
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "锁定的账户进行登录时,java接口异常"
            
        # 解除锁定
        api.accounts_id_unlock_account_put(id=user_id,
                                           body={"isBlocked": False})
        
        # 解锁后通过获取列表判断状态
        investors_resp = api.accounts_investors_get(email=user["email"])
        account = investors_resp.items.pop()
        assert not account.is_blocked
        # 解锁后通过详情判断账户状态
        account_info = api.accounts_accounts_id_get(id=user_id)
        assert not account_info.basic_info.is_blocked
        
        # 尝试登录判断解锁成功
        with_login(platform, list(), account=user["email"],
                   password=user["password"])

    # 该接口暂时废弃
    # @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    # def test_reset_phone(self, platform, with_login):
    #     manager = PlatformManager(platform)
    #     account_api = manager.account_api
    #     verify_api = manager.verify_api
    #     api = account_management_api.AccountManagementApi()
    #     admin_token = get_admin_token()
    #     api.api_client.set_default_header("Authorization",
    #                                       "Bearer " + admin_token)
    #     user = register_with_login(platform, with_login, [account_api,
    #                                                       verify_api])
    #     faker = Faker('zh_CN')
    #     phone = faker.phone_number()
    #     # 给账户绑定电话
    #     verify = verify_info(manager, user["email"], "bind_phone")
    #     manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
    #                        area_code="+86", token=verify.token)
    #
    #     # 获取账户状态信息判断是否绑定成功
    #     account_info = account_api.accounts_account_info_get()
    #     assert account_info.account_info.email == user["email"]
    #     # print(account_info.account_info.phone_number)
    #     # print(dir(account_info.account_info.phone_number))
    #     assert account_info.account_info.phone_number.short_phone_number == phone
    #
    #     # 后台获取账户状态判断是否绑定成功
    #     investors_resp = api.accounts_investors_get(email=user["email"])
    #     account = investors_resp.items.pop()
    #     assert account.email == user["email"]
    #     user_id = account.uid
    #     account_info = api.accounts_accounts_id_get(id=user_id)
    #     assert account_info.basic_info.phone_number == "+86" + phone
    #
    #     # 通过列表获取账户
    #     investors_resp = api.accounts_investors_get(email=user["email"])
    #     account = investors_resp.items.pop()
    #     assert account.email == user["email"]
    #     user_id = account.uid
    #
    #     # 重置不存在的用户的手机号
    #     try:
    #         api.accounts_id_reset_phone_put(id=str(50000))
    #     except ApiException as e:
    #         assert e.status == 400
    #     else:
    #         assert False, "重置不存在的账户电话时, java接口异常"
    #
    #     # 正常重置用户手机号
    #     api.accounts_id_reset_phone_put(id=user_id)
    #
    #     # 重置后从后台判断手机号是否为空
    #     account_info = api.accounts_accounts_id_get(id=user_id)
    #     assert not account_info.basic_info.phone_number
    #
    #     # 从其他平台判断用户手机号是否为空
    #     account_info = account_api.accounts_account_info_get()
    #     assert account_info.account_info.email == user["email"]
    #     assert not account_info.account_info.phone_number

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_remove_google_auth(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [account_api,
                                                          verify_api])
        api = account_management_api.AccountManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        # 解放未绑定google认证的账户
        investors_resp = api.accounts_investors_get(email=user["email"])
        account = investors_resp.items.pop()
        assert account.email == user["email"]
        user_id = account.uid
        try:
            api.accounts_id_release_google_delete(id=user_id)
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, "账户未绑定google这时解除google绑定时, java接口异常"
        
        email = user["email"]
        # 绑定google验证
        verify = verify_info(manager, email, "bind_google")
        manager.bind_google(DEFAULT_VERIFY_CODE, verify.token)
            
        # 通过其他平台获取用户绑定google状态
        account_info = account_api.accounts_account_info_get()
        assert account_info.account_info.google_authenticator
        
        # 解放不存在的用户的google认证
        try:
            api.accounts_id_release_google_delete(id="500000")
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "解除不存在的用户google时, java接口异常"
            
        # 正常解放用户的google认证
        api.accounts_id_release_google_delete(id=user_id)
        account_info = account_api.accounts_account_info_get()
        assert not account_info.account_info.google_authenticator

    def test_no_exist_individual(self):
        api = account_management_api.AccountManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        try:
            api.accounts_id_individual_get(id="500000")
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "获取不存在的账户个人认证时, java接口异常"
            
    def test_no_login_individual(self):
        api = account_management_api.AccountManagementApi()
        try:
            api.accounts_id_individual_get(id="500000")
        except ApiException as e:
            assert e.status == 403
        else:
            assert False, "未登录时获取账户个人认证时, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_individual_account(self, platform, with_login):
        api = account_management_api.AccountManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        user = register_with_login(platform, with_login, [])
        email = user["email"]
        # 通过列表获取账户id
        investors_resp = api.accounts_investors_get(email=user["email"])
        account = investors_resp.items.pop()
        assert account.email == email
        user_id = account.uid
        try:
            api.accounts_id_individual_get(id=user_id)
        except ApiException as e:
            assert e.status == 404
        else:
            assert False

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_individual(self, platform, with_login):
        user = register_with_login(platform, with_login, [])
        email = user["email"]
        id_number = get_random_id_number()
        # 进行个人实名认证
        individual_verify(platform=platform, id_number=id_number,
                          token=user["token"], verify_status="ACCEPTED")
        
        api = account_management_api.AccountManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        # 通过列表获取账户id
        investors_resp = api.accounts_investors_get(email=user["email"])
        account = investors_resp.items.pop()
        assert account.email == email
        user_id = account.account_id
        individual_info = api.accounts_id_individual_get(id=user_id)
        assert individual_info.type == "ID"
        assert individual_info.number == id_number
        # assert individual_info.front_photo == "front_photo"
        # assert individual_info.back_photo == "back_photo"
        # assert individual_info.handheld_photo == "handheld_photo"
        
    def test_no_login_company(self):
        api = account_management_api.AccountManagementApi()
        try:
            api.accounts_id_company_get(id="500000")
        except ApiException as e:
            assert e.status == 403
        else:
            assert False, "未登录时获取账户企业认证, java接口异常"
        
    def test_no_exist_company(self):
        api = account_management_api.AccountManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        try:
            api.accounts_id_company_get(id="500000")
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "获取不存在的账户企业认证, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_company(self, platform, with_login):
        user = register_with_login(platform, with_login, [])
        email = user["email"]
        social_number = get_random_id_number()
        # social_number = "123456788"
        # 进行企业实名认证
        company_verify(platform=platform, social_number=social_number,
                       token=user["token"])
    
        api = account_management_api.AccountManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        # 通过列表获取账户id
        investors_resp = api.accounts_investors_get(email=user["email"])
        account = investors_resp.items.pop()
        assert account.email == email
        user_id = account.account_id
        company_info = api.accounts_id_company_get(id=user_id)
        assert company_info.social_code == social_number
        assert company_info.area == "公司所在区域"
