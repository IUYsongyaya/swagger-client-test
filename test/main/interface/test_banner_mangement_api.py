# coding: utf-8

"""
    crush 平台接口（主平台）

    `crush` 平台接口（主平台）  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: api@crush.team
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pytest
import json
import swagger_client.main
from swagger_client.main.api.banner_mangement_api import BannerMangementApi  # noqa: E501
from swagger_client.main.rest import ApiException
from conftest import verify, login, logout, register, BACK_DOOR_VERIFY_CODE, rand_password, rand_email, rand_phone, rand_indiv_cert


api = swagger_client.main.api.banner_mangement_api.BannerMangementApi()


def pytest_namespace():
    return {'email': "", "password": "", "base_token": "", "phone": ""}


class TestBannerMangementApi:
    """BannerMangementApi pytest stubs"""

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

    def test_banners_exchange_id_get(self):
        """Test case for banners_exchange_id_get

        交易所首页轮播图  # noqa: E501
        """
        pass

    def test_banners_get(self):
        """Test case for banners_get

        平台首页轮播图  # noqa: E501
        """
        pass

