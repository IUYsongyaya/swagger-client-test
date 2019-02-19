#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 14:57
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 收藏列表（项目）——收藏项目——收藏列表（项目）

import pytest

from common.certification_verify import individual_verify
from common.utils import get_random_id_number
from swagger_client.main.api.project_api import ProjectApi as Main
from swagger_client.main.api.favorite_project_api import FavoriteProjectApi
from common.account_sign import register_with_login, set_login_status


main_api = Main()
favorite_api = FavoriteProjectApi()


class TestFavoriteProjectCase6(object):

    @pytest.mark.order1
    def test_favorite_project_case6(self, with_login):
        user = register_with_login('main', with_login, [favorite_api])
        # 个人实名认证
        individual_verify(platform="main", id_number=get_random_id_number(), token=user["token"])

        # 主平台获取项目列表
        set_login_status(favorite_api, user["token"])
        res = main_api.projects_get(page=1, sort_key="volume", limit=100)
        main_project_id = ''
        for item in res.items:
            main_project_id = item.project_id
        # 收藏列表
        res = favorite_api.favorites_projects_get(page=1)
        assert res.meta.total_count == 0
        # 收藏
        payload = {
            'projectId': main_project_id
        }
        favorite_api.favorites_projects_post(body=payload)
        # 收藏列表
        res = favorite_api.favorites_projects_get(page=1)
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.project_id == main_project_id
            assert item.id
            assert item.full_name
            assert item.project_name
            assert item.short_name
        # 判断是否收藏
        res = favorite_api.favorites_projects_is_favorite_get(project_id=main_project_id)
        assert res.status is True
        assert res.id
