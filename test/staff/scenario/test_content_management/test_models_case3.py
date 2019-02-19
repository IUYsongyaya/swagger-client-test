#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 10:52
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 新建文章模型——获取文章模型列表——删除文章模型——获取文章模型列表
import pytest
import random

from common.utils import get_random_name
from swagger_client.staff.api.content_management_api import ContentManagementApi
from common.account_sign import get_admin_token
from common.account_sign import set_login_status


class TestModelsCase3(object):

    @pytest.mark.order1
    def test_models_case3(self):
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
        models_id = ''
        page = 1
        res = content_api.models_get(type='article', page=page)
        total_page = res.meta.total_page
        while page <= total_page:
            res = content_api.models_get(type='article', page=page)
            for item in res.items:
                if item.name == payload['name']:
                    assert item.status is True
                    assert item.order == payload['order']
                    assert item.type == 'article'
                    models_id = item.id
            page += 1
        # 删除文章模型
        content_api.models_id_delete(id=models_id)
        # 获取文章模型列表
        res = content_api.models_get(type='article')
        models_name = ''
        total_page = res.meta.total_page
        while page <= total_page:
            res = content_api.models_get(type='article', page=page)
            for item in res.items:
                if item.name == payload['name']:
                    models_name = item.name
                assert not models_name
            page += 1
