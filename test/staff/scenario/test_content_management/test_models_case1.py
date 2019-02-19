#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/28 16:22
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 新建文章模型——获取文章模型列表——获取文章模型名称列表——获取文章模型详情
import pytest
import random

from common.utils import get_random_name
from swagger_client.staff.api.content_management_api import ContentManagementApi
from common.account_sign import get_admin_token
from common.account_sign import set_login_status


class TestModelsCase1(object):

    @pytest.mark.order1
    def test_models_case1(self):
        # 后台登录
        content_api = ContentManagementApi()
        staff_token = get_admin_token()
        set_login_status(content_api, staff_token)
        # 新建文章模型
        payload = {
            'identification': get_random_name(2, 50),
            'name': get_random_name(2, 50),
            'status': True,
            'order': random.randint(100000, 999999),
            'type': 'article'  # article文章，kinmall金猫
        }
        content_api.models_post(body=payload)
        # 获取文章模型列表
        res = content_api.models_get(type='article')
        for item in res.items:
            if item.name == payload['name']:
                assert item.identification == payload['identification']
                assert item.id
        # 获取文章模型名称列表
        res = content_api.models_names_get(type='article')
        id_ = ''
        for item in res.items:
            if item.name == payload['name']:
                assert item.id
                id_ = item.id
        # 获取文章模型详情
        res = content_api.models_id_get(id=id_)
        assert res.name == payload['name']
        assert res.status == payload['status']
        assert res.order == payload['order']
        assert res.type == payload['type']
        assert res.identification == payload['identification']
