# coding: utf-8

"""
    kinmall 平台接口（保荐方平台端）

    `kinmall` 平台接口（保荐方平台端）  当前接口为 `sponsor` 端  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: api@kinmall.team
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pytest
import json
import swagger_client.sponsor
from swagger_client.sponsor.api.sponsor_api import SponsorApi  # noqa: E501
from swagger_client.sponsor.rest import ApiException
from conftest import verify, login, logout, register, BACK_DOOR_VERIFY_CODE, rand_password, rand_email, rand_phone, rand_indiv_cert


api = swagger_client.tenant.api.sponsor_api.SponsorApi()


def pytest_namespace():
    return {'email': "", "password": "", "base_token": "", "phone": ""}


class TestSponsorApi:
    """SponsorApi pytest stubs"""

    def test_register_and_login_prepare(self):
        country = "86"
        pytest.email = rand_email()
        pytest.password = rand_password()
        register(email=pytest.email, password=pytest.password, promotion_code="",
                 verification_code=BACK_DOOR_VERIFY_CODE,
                 country=country)

        pytest.base_token = login(api, pytest.email, pytest.password, challenge="", seccode=BACK_DOOR_VERIFY_CODE,
                                  validate="")
        print("register return base_token:%s" % pytest.base_token)

    def test_sponsor_info_post(self):
        """Test case for sponsor_info_post

        重置密码之前根据用户名获取绑定的手机和邮箱  # noqa: E501
        """
        pass

    def test_sponsor_login_post(self):
        """Test case for sponsor_login_post

        账户登录  # noqa: E501
        """
        pass

    def test_sponsor_logout_post(self):
        """Test case for sponsor_logout_post

        账户注销  # noqa: E501
        """
        pass

    def test_sponsor_send_verification_code_post(self):
        """Test case for sponsor_send_verification_code_post

        发送验证码  # noqa: E501
        """
        pass

    def test_sponsor_set_password_post(self):
        """Test case for sponsor_set_password_post

        重置密码  # noqa: E501
        """
        pass
