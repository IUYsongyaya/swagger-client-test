#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/30 17:02
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 新建kinmall文章——获取kinmall文章列表——删除kinmall文章——获取kinmall文章列表
import pytest
import random

from common.utils import get_random_name
from swagger_client.staff.api.content_management_api import ContentManagementApi
from common.account_sign import get_admin_token
from common.account_sign import set_login_status


class TestModelsCase16(object):

    @pytest.mark.order1
    def test_models_case16(self):
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
            'type': 'kinmall'  # article文章，kinmall金猫
        }
        content_api.models_post(body=payload)
        # 获取文章模型列表
        models_id = ''
        page = 1
        res = content_api.models_get(type='kinmall', page=page)
        total_page = res.meta.total_page
        while page <= total_page:
            res = content_api.models_get(type='kinmall', page=page)
            for item in res.items:
                if item.name == payload['name']:
                    assert item.status is True
                    assert item.order == payload['order']
                    assert item.type == 'kinmall'
                    models_id = item.id
            page += 1
        # 新建子模型
        sub_payload = {
            "identification": get_random_name(2, 50),
            "name": get_random_name(2, 50),
            "status": True,
            "order": random.randint(1000, 9999),
            "modelId": models_id
        }
        content_api.sub_models_post(body=sub_payload)
        # 获取子模型列表
        id_ = ''
        res = content_api.sub_models_get(parent_id=models_id)
        for item in res.items:
            if item.name == sub_payload['name']:
                assert item.status is True
                assert item.order == sub_payload['order']
                id_ = item.id
        # 新建documents文章
        payload1 = {
            "author": "作者" + str(random.randint(10000, 99999)),
            "content": "文章内容" + str(random.randint(10000, 99999)),
            "isTop": True,
            "language": "zh_cn",
            "modelId": models_id,
            "order": 1,
            "status": True,
            "subModelId": id_,
            "title": "文章标题" + str(random.randint(10000, 99999)),
            "type": "kinmall"
        }
        content_api.documents_post(body=payload1)
        # 获取documents文章列表
        documents_id = ''
        page = 1
        res = content_api.documents_get(type='kinmall', page=page)
        total_page = res.meta.total_page
        while page <= total_page:
            res = content_api.documents_get(type='kinmall', page=page)
            for item in res.items:
                if item.title == payload1['title']:
                    assert item.language == payload1['language']
                    assert item.order == payload1['order']
                    assert item.status == payload1['status']
                    documents_id = item.id
            page += 1
        # 删除documents文章
        content_api.documents_id_delete(id=documents_id)
        # 获取documents文章列表
        page = 1
        res = content_api.documents_get(type='kinmall', page=page)
        total_page = res.meta.total_page
        while page <= total_page:
            res = content_api.documents_get(type='kinmall', page=page)
            for item in res.items:
                assert item.title
            page += 1
