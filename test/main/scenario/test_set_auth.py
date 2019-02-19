#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_set_auth.py
@time: 2018/11/13
"""
import pytest
from faker import Faker

from common.utils import PlatformManager
from common.account_sign import register_with_login


TURN_ON = 1
TURN_OFF = 0
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


class TestAuthSetting:
    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_set_auth(self, with_login, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [account_api,
                                                          verify_api])
        email = user.get("email", "")
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)
            
        # 修改电话
        changed_phone = faker.phone_number()
        verify = verify_info(manager, email, "alter_phone")
        manager.alter_phone(changed_phone, DEFAULT_VERIFY_CODE, "+86",
                            token=verify.token)
            
        # 绑定谷歌验证器
        verify = verify_info(manager, email, "bind_google")
        manager.bind_google(DEFAULT_VERIFY_CODE, verify.token)

        verify = verify_info(manager, email, "alter_google")
        # 修改谷歌验证器
        manager.alter_google(DEFAULT_VERIFY_CODE, verify.token)
        
        # 查看验证开关
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
        
        # 开启谷歌验证
        manager.open_google(DEFAULT_VERIFY_CODE)

        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON

        # 开启电话验证
        manager.open_phone(DEFAULT_VERIFY_CODE)
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON

        # 关闭谷歌验证
        manager.close_google(email, DEFAULT_VERIFY_CODE, DEFAULT_VERIFY_CODE)
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON

        # 关闭电话验证
        manager.close_phone(email, DEFAULT_VERIFY_CODE, DEFAULT_VERIFY_CODE)
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_repeat_open_auth(self, with_login, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [account_api,
                                                          verify_api])
        email = user.get("email")
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        # 绑定电话
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE, "+86", verify.token)

        # 绑定谷歌验证器
        verify = verify_info(manager, email, "bind_google")
        manager.bind_google(DEFAULT_VERIFY_CODE, verify.token)
        
        # 查看验证开关
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
    
        # 开启谷歌验证
        manager.open_google(DEFAULT_VERIFY_CODE)
        
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
        
        # 重复开启谷歌验证
        # try:
        manager.open_google(DEFAULT_VERIFY_CODE)
        # except manager.api_exception as e:
        #     assert e.status == 400
        # else:
        #     assert False, "重复开启google验证java接口异常"
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
        
        # 开启电话验证
        manager.open_phone(DEFAULT_VERIFY_CODE)
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
        # 重复开启电话验证
        # try:
        manager.open_phone(DEFAULT_VERIFY_CODE)
        # except manager.api_exception as e:
        #     assert e.status == 400
        # else:
        #     assert False, "重复开启电话验证java接口异常"
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_repeat_close_auth(self, with_login, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [account_api,
                                                          verify_api])
        email = user.get("email")
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        # 绑定电话
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE, "+86", verify.token)

        # 绑定谷歌验证器
        verify = verify_info(manager, email, "bind_google")
        manager.bind_google(DEFAULT_VERIFY_CODE, verify.token)
        
        # 查看验证开关
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
    
        # 开启谷歌验证
        manager.open_google(DEFAULT_VERIFY_CODE)

        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
    
        # 开启电话验证
        manager.open_phone(DEFAULT_VERIFY_CODE)
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_ON
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
    
        # 关闭谷歌验证
        manager.close_google(email, DEFAULT_VERIFY_CODE, DEFAULT_VERIFY_CODE)
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
        # 重复关闭谷歌
        # try:
        manager.close_google(email, DEFAULT_VERIFY_CODE,
                             DEFAULT_VERIFY_CODE)
        # except manager.api_exception as e:
        #     assert e.status == 400
        # else:
        #     assert False, "重复关闭谷歌验证java接口异常"
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_ON
        assert res.email_authenticator == TURN_ON
    
        # 关闭电话验证
        manager.close_phone(email, DEFAULT_VERIFY_CODE, DEFAULT_VERIFY_CODE)
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON
        # 重复关闭电话验证
        # try:
        manager.close_phone(email, DEFAULT_VERIFY_CODE,
                            DEFAULT_VERIFY_CODE)
        # except manager.api_exception as e:
        #     assert e.status == 400
        # else:
        #     assert False, "重复关闭电话验证java接口异常"
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_bind_incorrect_field_phone(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [account_api,
                                                          verify_api])
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON
        # 绑定电话
        verify = verify_info(manager, user["email"], "bind_phone")
        try:
            account_api.accounts_bind_phone_post(body={
                                                      "phoneNumber": 12345678,
                                                      "verificationCode": "666666",
                                                      "areaCode": "+86",
                                                      "token": verify.token
                                                    })
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "绑定电话时填写错误类型的电话java接口异常"

        # 绑定电话
        try:
            account_api.accounts_bind_phone_post(body={
                "phoneNumber": "()??.,.@@@@",
                "verificationCode": "666666",
                "areaCode": "+86",
                "token": verify.token
            })
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "绑定电话时填写特殊字符的电话java接口异常"

        faker = Faker('zh_CN')
        changed_phone = faker.phone_number()
        # 修改电话
        verify = verify_info(manager, user["email"], "alter_phone")
        try:
            manager.alter_phone(changed_phone, DEFAULT_VERIFY_CODE, "+86",
                                verify.token)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "未绑定电话后调用修改电话接口,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_incorrect_field_google(self, with_login, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [account_api,
                                                          verify_api])
        email = user["email"]
        # 绑定谷歌验证器
        verify = verify_info(manager, email, "bind_google")
        try:
            account_api.accounts_bind_google_authenticator_post(
                word={
                      "googleCode": 123456,
                      "token": verify.token
                    })
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "绑定谷歌时填写错误类型的验证码,java接口异常"
        
        # 修改谷歌验证器
        verify = verify_info(manager, email, "alter_google")
        try:
            manager.alter_google("666666", verify.token)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "未绑定谷歌验证时调用修改谷歌验证,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_open_no_auth(self, with_login, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        user = register_with_login(platform, with_login, [account_api])
        email = user.get("email")
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON

        # 开启谷歌验证
        try:
            manager.open_google(DEFAULT_VERIFY_CODE)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "未绑定google,开启google验证,java接口异常"
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON
    
        # 开启电话验证
        try:
            manager.open_phone(DEFAULT_VERIFY_CODE)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "未绑定电话, 开启电话验证, java接口异常"
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON
    
        # 关闭谷歌验证
        try:
            manager.close_google(email, DEFAULT_VERIFY_CODE,
                                 DEFAULT_VERIFY_CODE)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "未绑定谷歌验证, 关闭谷歌验证, java接口异常"
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON
    
        # 关闭电话验证
        try:
            manager.close_phone(email, DEFAULT_VERIFY_CODE,
                                DEFAULT_VERIFY_CODE)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "未绑定电话验证, 关闭电话验证, java接口异常"
        res = account_api.accounts_get_bind_status_get()
        assert res.google_authenticator == TURN_OFF
        assert res.phone_authenticator == TURN_OFF
        assert res.email_authenticator == TURN_ON

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_init_google(self, platform, with_login):
        manager = PlatformManager(platform)
        verify_api = manager.verify_api
        register_with_login(platform, with_login, api_list=[verify_api])
        res = manager.init_google()
        assert isinstance(res.uri, str)
        assert isinstance(res.key, str)
        res = manager.init_google()
        assert isinstance(res.uri, str)
        assert isinstance(res.key, str)

    # @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    # def test_error_field_init_google(self, platform):
    #     manager = PlatformManager(platform)
    #     try:
    #         manager.init_google(12345)
    #     except manager.api_exception as e:
    #         assert e.status == 400

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_init_captcha(self, platform):
        manager = PlatformManager(platform)
        verify_api = manager.verify_api
        res = verify_api.accounts_init_captcha_get()
        assert isinstance(res.success, str)
        assert res.success == "1"
        assert isinstance(res.challenge, str)
        assert isinstance(res.gt, str)
        assert isinstance(res.new_captcha, str)
