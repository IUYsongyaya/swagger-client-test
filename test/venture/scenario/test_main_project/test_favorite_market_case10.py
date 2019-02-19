#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/07 16:32
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 收藏列表（市场）——收藏市场——收藏列表（市场）
from faker import Faker
import pytest

from common.certification_verify import individual_verify
from common.utils import (PlatformManager, random_get_country_ob,
                          get_random_id_number)
from swagger_client.venture.api.project_api import ProjectApi
from swagger_client.main.api.project_api import ProjectApi as Main
from common.account_sign import set_login_status
from swagger_client.main.api.exchange_api import ExchangeApi
from swagger_client.main.api.market_api import MarketApi
from swagger_client.main.api.favorite_market_api import FavoriteMarketApi
from test.venture.scenario.rand_email import random_email

api = ProjectApi()
main_api = Main()


class TestFavoriteProjectCase10(object):

    @pytest.mark.order1
    def test_favorite_project_case10(self):
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
        # 获取交易对市场列表
        market_api = MarketApi()
        set_login_status(market_api, token)
        res = market_api.markets_get(exchange_id=exchange_id, page=1)
        market_id = ''
        for item in res.items:
            market_id = item.id
        # 收藏列表
        favorite_api = FavoriteMarketApi()
        set_login_status(favorite_api, token)
        res = favorite_api.favorites_market_get(page=1, exchange_id=exchange_id)
        assert res.meta.total_count == 0
        # 收藏
        payload = {
            'marketId': market_id
        }
        favorite_api.favorites_market_post(body=payload)
        # 收藏列表
        res = favorite_api.favorites_market_get(page=1, exchange_id=exchange_id)
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.market_id == market_id
            assert item.id
        # 判断是否收藏
        res = favorite_api.favorites_market_is_favorite_get(market_id=market_id)
        assert res.status is True
        assert res.id
