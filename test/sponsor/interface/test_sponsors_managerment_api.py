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
from swagger_client.sponsor.api.sponsors_managerment_api import SponsorsManagermentApi  # noqa: E501
from swagger_client.sponsor.rest import ApiException
from conftest import verify, login, logout, register, BACK_DOOR_VERIFY_CODE, rand_password, rand_email, rand_phone, rand_indiv_cert


api = swagger_client.tenant.api.sponsors_managerment_api.SponsorsManagermentApi()


def pytest_namespace():
    return {'email': "", "password": "", "base_token": "", "phone": ""}


class TestSponsorsManagermentApi:
    """SponsorsManagermentApi pytest stubs"""

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

    def test_sponsors_ranking_get(self):
        """Test case for sponsors_ranking_get

        获取保荐方排行榜  # noqa: E501
        """
        pass
