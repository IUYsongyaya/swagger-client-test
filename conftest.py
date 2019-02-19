#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: conftest.py
@time: 2018/11/12
"""
import pytest

from common.utils import PlatformManager


@pytest.fixture(scope="function")
def with_login(request):
    """
    每个测试用例所用到的登录fixture,在teardown中会自动退出
    :param request:
    :return:
    """
    api_record = list()
    platform_type = str()
    token = str()

    def sign_in(platform, api_list, account="", password="", challenge="",
                sec_code="", validate=""):
        """
        :param platform: 平台名称Enum("main", "sponsor", "staff",
                                    "tenant", "venture", "otc")
        :param api_list: 所要登录的接口
        :param account: 账户
        :param password: 密码
        :param challenge:
        :param sec_code:
        :param validate:
        """
        nonlocal token
        nonlocal api_record
        nonlocal platform_type
        platform_type = platform
        manager = PlatformManager(platform)
        token = manager.login(account, password, challenge,
                              sec_code, validate)
        for api in api_list:
            api.api_client.set_default_header("Authorization",
                                              "Bearer " + token)
        api_record = api_list
        return token

    def sign_out():
        return
        nonlocal token
        nonlocal api_record
        nonlocal platform_type
        manager = PlatformManager(platform_type)
        if token and api_record:
            manager.logout(token, api_record)

    request.addfinalizer(sign_out)
    return sign_in


@pytest.fixture(scope="function")
def entrust_login(request):
    """
    每个测试用例所用到的登录fixture,在teardown中会自动退出
    :param request:
    :return:
    """
    api_record = list()
    platform_type = str()
    token = str()

    def sign_in(platform, api_list, account="", password="", challenge="",
                sec_code="", validate=""):
        """
        :param platform: 平台名称Enum("main", "sponsor", "staff",
                                    "tenant", "venture", "otc")
        :param api_list: 所要登录的接口
        :param account: 账户
        :param password: 密码
        :param challenge:
        :param sec_code:
        :param validate:
        """
        nonlocal token
        nonlocal api_record
        nonlocal platform_type
        platform_type = platform
        manager = PlatformManager(platform)
        token = manager.login(account, password, challenge,
                              sec_code, validate)
        for api in api_list:
            api.api_client.set_default_header("Authorization",
                                              "Bearer " + token)
        api_record = api_list
        return token

    def sign_out():
        nonlocal token
        nonlocal api_record
        nonlocal platform_type
        manager = PlatformManager(platform_type)
        if token and api_record:
            manager.logout(token, api_record)

    return sign_in
