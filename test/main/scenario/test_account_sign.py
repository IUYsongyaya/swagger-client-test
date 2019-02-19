#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_account_sign.py
@time: 2018/11/11
"""
import uuid

import pytest
from faker import Faker

from common.utils import PlatformManager
from common.account_sign import random_user
from common.account_sign import set_login_status
from swagger_client.main.api import DeviceManagerApi


class TestAccountSign:
    # 以下三个是极验参数
    challenge = ""
    sec_code = ""
    validate = ""

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_sign(self, platform):
        manager = PlatformManager(platform)
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        country = user.get("country_abbreviation")
        manager.register(email=email, password=password,
                         promotion_code=None, verification_code="666666",
                         nationality_code=country, challenge=self.challenge,
                         sec_code=self.sec_code,
                         validate=self.validate)
        token = manager.login(account=email, password=password,
                              challenge=self.challenge,
                              sec_code=self.sec_code, validate=self.validate)
        assert token
        assert isinstance(token, str)
        manager.logout(token, list())
        api_exception = manager.api_exception
        try:
            manager.logout(token, list())
        except api_exception as e:
            assert e.status == 403
        else:
            assert False, "重复注销java部分发生异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_account_login(self, platform):
        manager = PlatformManager(platform)
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        api_exception = manager.api_exception
        try:
            manager.login(account=email, password=password,
                          challenge=self.challenge,
                          sec_code=self.sec_code, validate=self.validate)
        except api_exception as e:
            assert e.status == 400
        else:
            assert False, "不存在的账户登录时java部分发生异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_incorrect_password_login(self, platform):
        faker = Faker()
        manager = PlatformManager(platform)
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        country = user.get("country_abbreviation")
        manager.register(email=email, password=password,
                         promotion_code=None, verification_code="666666",
                         nationality_code=country, challenge=self.challenge,
                         sec_code=self.sec_code,
                         validate=self.validate)
        api_exception = manager.api_exception
        try:
            manager.login(account=email, password=faker.password(),
                          challenge=self.challenge,
                          sec_code=self.sec_code,
                          validate=self.validate)
        except api_exception as e:
            assert e.status == 400
        else:
            assert False, "错误密码登录java借口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_incorrect_field_register(self, platform):
        manager = PlatformManager(platform)
        api_exception = manager.api_exception
        account_api = manager.account_api
        try:
            # manager.register(email=123, password=123,
            #                  promotion_code=123, verification_code=123,
            #                  country=123, challenge=self.challenge,
            #                  sec_code=self.sec_code,
            #                  validate=self.validate)
            account_api.create_user(body={
                              "email": 123,
                              "password": 123,
                              "promotionCode": 123,
                              "verificationCode": 123,
                              "country": 123,
                              "challenge": 123,
                              "seccode": 123,
                              "validate": 123
                                })
        except api_exception as e:
            assert e.status == 400
        else:
            assert False, "传参类型不对java借口调用异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_repeated_register(self, platform):
        manager = PlatformManager(platform)
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        country = user.get("country_abbreviation")
        manager.register(email=email, password=password,
                         verification_code="666666",
                         nationality_code=country,
                         challenge=self.challenge,
                         sec_code=self.sec_code,
                         validate=self.validate)
        api_exception = manager.api_exception
        try:
            manager.register(email=email, password=password,
                             verification_code="666666",
                             nationality_code=country,
                             challenge=self.challenge,
                             sec_code=self.sec_code,
                             validate=self.validate)
        except api_exception as e:
            assert e.status == 400
        else:
            assert False, "重复注册java部分发生异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_incorrect_field_login(self, platform):
        manager = PlatformManager(platform)
        api_exception = manager.api_exception
        account_api = manager.account_api
        try:
            account_api.accounts_login_post({
              "account": 132,
              "password": 132,
              "challenge": 132,
              "seccode": 132,
              "validate": 132
            })
        except api_exception as e:
            assert e.status == 400
        else:
            assert False, "登录传参类型不对java部分发生异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_repeat_login(self, platform):
        manager = PlatformManager(platform)
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        country = user.get("country_abbreviation")
        manager.register(email=email, password=password,
                         verification_code="666666",
                         nationality_code=country, challenge=self.challenge,
                         sec_code=self.sec_code,
                         validate=self.validate)
        token = manager.login(account=email, password=password,
                              challenge=self.challenge,
                              sec_code=self.sec_code, validate=self.validate)
        assert token
        assert isinstance(token, str)
        token_ = manager.login(account=email, password=password,
                               challenge=self.challenge,
                               sec_code=self.sec_code, validate=self.validate)
        assert token_
        assert isinstance(token_, str)
        api_exception = manager.api_exception
        try:
            manager.logout(token, list())
        except api_exception as e:
            assert e.status == 403
        else:
            assert False, "旧token注销java部分发生异常"

    @pytest.mark.parametrize("platform_1", ["main", "tenant", "venture"])
    @pytest.mark.parametrize("platform_2", ["main", "tenant", "venture"])
    @pytest.mark.parametrize("platform_3", ["main", "tenant", "venture"])
    def test_interweave_sign(self, platform_1, platform_2, platform_3):
        manager_1 = PlatformManager(platform_1)
        manager_2 = PlatformManager(platform_2)
        manager_3 = PlatformManager(platform_3)
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        country = user.get("country_abbreviation")
        manager_1.register(email=email, password=password,
                           nationality_code=country, challenge=self.challenge,
                           sec_code=self.sec_code,
                           validate=self.validate)
        token = manager_2.login(account=email, password=password,
                                challenge=self.challenge,
                                sec_code=self.sec_code, validate=self.validate)
        assert token
        assert isinstance(token, str)
        manager_3.logout(token, list())
        api_exception = manager_1.api_exception
        try:
            manager_1.logout(token, list())
        except api_exception as e:
            assert e.status == 403
        else:
            assert False, "重复注销java部分发生异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_fill_promotion_sign(self, platform):
        manager = PlatformManager(platform)
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        country = user.get("country_abbreviation")
        try:
            manager.register(email=email, password=password,
                             promotion_code="2NbYYJiEb4npQ",
                             verification_code="666666",
                             nationality_code=country, challenge=self.challenge,
                             sec_code=self.sec_code,
                             validate=self.validate)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "填入不存在的验证码时, java接口异常"

    def test_token_isvalid(self):
        manager = PlatformManager("main")
        account_api = manager.account_api
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        country = user.get("country_abbreviation")
        manager.register(email=email, password=password,
                         promotion_code=None, verification_code="666666",
                         nationality_code=country, challenge=self.challenge,
                         sec_code=self.sec_code,
                         validate=self.validate)
        token = manager.login(account=email, password=password,
                              challenge=self.challenge,
                              sec_code=self.sec_code, validate=self.validate)
        set_login_status(account_api, token)
        account_api.accounts_verify_is_valid_post()

    @pytest.mark.parametrize("device_type", ["iOS", "Android", "Web", "Other"])
    def test_bind_device(self, device_type):
        manager = PlatformManager("main")
        device_api = DeviceManagerApi()
        user = random_user()
        email = user.get("email")
        password = user.get("password")
        country = user.get("country_abbreviation")
        manager.register(email=email, password=password,
                         promotion_code=None, verification_code="666666",
                         nationality_code=country, challenge=self.challenge,
                         sec_code=self.sec_code,
                         validate=self.validate)
        token = manager.login(account=email, password=password,
                              challenge=self.challenge,
                              sec_code=self.sec_code, validate=self.validate)
        set_login_status(device_api, token)
        device_id = uuid.uuid4().hex
        device_type = device_type
        device_api.device_bind_post(device_id=device_id,
                                    device_type=device_type)
        device_api.device_unbind_post(device_id=device_id,
                                      device_type=device_type)
