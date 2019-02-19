#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 15:23
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 收藏项目成功——收藏列表（项目）——取消收藏
from faker import Faker
import pytest

from common.certification_verify import individual_verify
from common.utils import (PlatformManager, random_get_country_ob,
                          get_random_id_number)
from swagger_client.venture.api.project_api import ProjectApi
from swagger_client.main.api.project_api import ProjectApi as Main
from common.account_sign import set_login_status
from swagger_client.main.api.favorite_project_api import FavoriteProjectApi
from test.venture.scenario.rand_email import random_email

api = ProjectApi()
main_api = Main()


class TestFavoriteProjectCase6(object):

    @pytest.mark.order1
    def test_favorite_project_case6(self):
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

        # 主平台获取项目列表
        favorite_api = FavoriteProjectApi()
        set_login_status(favorite_api, token)
        res = main_api.projects_get(page=1, sort_key="volume", limit=100)
        main_project_id = ''
        for item in res.items:
            main_project_id = item.project_id
        # 收藏列表
        res = favorite_api.favorites_projects_get(page=1)
        assert res.meta.total_count == 0
        # 收藏
        payload = {
            'projectId': main_project_id,
        }
        favorite_api.favorites_projects_post(body=payload)
        # 收藏列表
        res = favorite_api.favorites_projects_get(page=1)
        favorite_id = ''
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.project_id == main_project_id
            assert item.id
            assert item.account_id
            assert item.project_id
            assert item.short_name
            assert item.full_name
            favorite_id = item.id
        # 取消收藏
        favorite_api.favorites_projects_delete(ids=favorite_id)
        # 收藏列表
        res = favorite_api.favorites_projects_get(page=1)
        assert res.meta.total_count == 0
