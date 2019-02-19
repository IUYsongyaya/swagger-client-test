#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/28 18:03
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 新建文章模型——获取文章模型列表——获取文章模型详情——更新文章模型信息——获取文章模型列表——获取文章模型详情
import pytest
import random

from common.utils import get_random_name
from swagger_client.staff.api.content_management_api import ContentManagementApi
from common.account_sign import get_admin_token
from common.account_sign import set_login_status


class TestModelsCase2(object):

    @pytest.mark.order1
    def test_models_case2(self):
        # 后台登录
        content_api = ContentManagementApi()
        staff_token = get_admin_token()
        set_login_status(content_api, staff_token)
        # 新建文章模型
        payload = {
            'identification': get_random_name(2, 50),
            'name': get_random_name(2, 50),
            'status': True,
            'order': random.randint(1000, 9999),
            'type': 'article'  # article文章，kinmall金猫
        }
        content_api.models_post(body=payload)
        # 获取文章模型列表
        res = content_api.models_get(type='article')
        for item in res.items:
            if item.name == payload['name']:
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
        # 更新文章模型信息
        payload1 = {
            'identification': get_random_name(2, 50),
            'name': get_random_name(2, 50),
            'status': True,
            'order': payload['order'],
            'type': 'article'  # article文章，kinmall金猫
        }
        content_api.models_id_put(id=id_, body=payload1)
        # 获取文章模型列表
        res = content_api.models_get(type='article')
        for item in res.items:
            if item.name == payload['name']:
                assert item.id
        # 获取文章模型名称列表
        res = content_api.models_names_get(type='article')
        id_ = ''
        for item in res.items:
            if item.name == payload1['name']:
                assert item.id
                id_ = item.id
        # 获取文章模型详情
        res = content_api.models_id_get(id=id_)
        assert res.name == payload1['name']
        assert res.status == payload1['status']
        assert res.order == payload1['order']
        assert res.type == payload1['type']
