# coding: utf-8

"""
    otc

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pytest
import json
import swagger_client.otc
from swagger_client.otc.api.balance_api import BalanceApi  # noqa: E501
from swagger_client.otc.rest import ApiException
from conftest import verify, login, logout, register, BACK_DOOR_VERIFY_CODE, rand_password, rand_email, rand_phone, rand_indiv_cert


api = swagger_client.otc.api.balance_api.BalanceApi()


def pytest_namespace():
    return {'email': "", "password": "", "base_token": "", "phone": ""}


class TestBalanceApi:
    """BalanceApi pytest stubs"""

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

    def test_balance_getflow_get(self):
        """Test case for balance_getflow_get

        查询流水  # noqa: E501
        """
        pass

    def test_balance_list_get(self):
        """Test case for balance_list_get

        查询账目  # noqa: E501
        """
        pass
