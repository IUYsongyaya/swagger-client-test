#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_account_password.py
@time: 2018/11/18
"""
import pytest

from faker import Faker

from common.utils import PlatformManager
from common.account_sign import register_with_login


class TestAccountPassword:
    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_change_password(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login,
                                   [account_api, verify_api])
        faker = Faker('zh_CN')
        new_password = faker.password()
        manager.change_password(user.get("email"), user.get("password"),
                                new_password)
        res = manager.login(account=user.get("email"), password=new_password)
        assert isinstance(res, str)
        try:
            manager.login(account=user.get("email"),
                          password=user.get("password"))
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "用旧密码登录,java接口发生异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_error_password_change(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login,
                                   [account_api, verify_api])
        faker = Faker('zh_CN')
        new_password = faker.password()
        try:
            manager.change_password(user.get("email"), "12345678", new_password)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "输入错误密码后修改密码,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_change(self, platform, with_login):
        manager = PlatformManager(platform)
        user = register_with_login(platform, with_login, list())
        faker = Faker('zh_CN')
        new_password = faker.password()
        try:
            manager.change_password(user.get("email"),
                                    user.get("password"),
                                    new_password)
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录的用户进行修改密码,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_error_field_change(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login,
                                   [account_api, verify_api])
        try:
            account_api.accounts_set_password_post(
                body={"oldPassword": user.get("password"),
                      "newPassword": 12345678})
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "填写错误类型的新密码, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_reset_password(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login,
                                   [account_api, verify_api])
        faker = Faker('zh_CN')
        new_password = faker.password()
        manager.reset_password(user.get("email"), new_password)
        token = manager.login(user.get("email"), new_password)
        assert isinstance(token, str)

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_account_reset_password(self, platform):
        manager = PlatformManager(platform)
        faker = Faker('zh_CN')
        email = faker.email()
        reset_password = manager.reset_password_request_model(uri=email,
                                                              challenge="",
                                                              seccode="",
                                                              validate="")
        try:
            manager.account_api.accounts_reset_password_post(reset_password)
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "不存在的账户充值密码时, java接口异常"

    @pytest.mark.parametrize("platform", ["main"])
    def test_normal_verify_password(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login,
                                   [account_api, verify_api])
        manager.verify_password(user.get("password"))
        faker = Faker()
        try:
            manager.verify_password(faker.password())
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "验证错误密码, java接口异常"

    @pytest.mark.parametrize("platform", ["main"])
    def test_no_login_verify_password(self, platform):
        manager = PlatformManager(platform)
        faker = Faker()
        try:
            manager.verify_password(faker.password())
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录进行密码验证, java接口异常"
