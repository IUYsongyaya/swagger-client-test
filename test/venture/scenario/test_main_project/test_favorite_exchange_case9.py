#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/07 15:56
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 收藏交易所成功——收藏列表（交易所）——取消收藏
from faker import Faker
import pytest

from common.certification_verify import individual_verify
from common.utils import (PlatformManager, random_get_country_ob,
                          get_random_id_number)
from swagger_client.venture.api.project_api import ProjectApi
from swagger_client.main.api.project_api import ProjectApi as Main
from common.account_sign import set_login_status
from swagger_client.main.api.exchange_api import ExchangeApi
from swagger_client.main.api.favorite_exchange_api import FavoriteExchangeApi
from test.venture.scenario.rand_email import random_email

api = ProjectApi()
main_api = Main()


class TestFavoriteProjectCase9(object):

    @pytest.mark.order1
    def test_favorite_project_case9(self):
        faker = Faker()
        manager = PlatformManager("main")
        email = random_email()
        password = faker.password()
        country = random_get_country_ob()
        manager.register(email=email, password=password,
                         promotion_code=None, verification_code="666666",
                         nationality_code=country.get("k"))
        token = manager.login(account=email, password=password)
        # 个人实名认证
        individual_verify(platform="main", id_number=get_random_id_number(), token=token)
        # 交易所排行列表
        exchange_api = ExchangeApi()
        set_login_status(exchange_api, token)
        res = exchange_api.exchanges_exchanges_get()
        exchange_id = ''
        for item in res.items:
            exchange_id = item.id
        # 收藏列表
        favorite_api = FavoriteExchangeApi()
        set_login_status(favorite_api, token)
        res = favorite_api.favorites_exchange_get(page=1)
        assert res.meta.total_count == 0
        # 收藏
        payload = {
            'exchangeId': exchange_id,
        }
        favorite_api.favorites_exchange_post(body=payload)
        # 收藏列表
        res = favorite_api.favorites_exchange_get(page=1)
        id_ = ''
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.exchange_id == exchange_id
            assert item.id
            assert item.exchange_name
            id_ = item.id
        # 取消收藏
        favorite_api.favorites_exchange_delete(id=id_)
        # 收藏列表
        res = favorite_api.favorites_exchange_get(page=1)
        assert res.meta.total_count == 0
