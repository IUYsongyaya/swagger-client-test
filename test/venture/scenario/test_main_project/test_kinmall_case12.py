#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/15 15:45
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 新建kinmall文章——获取kinmall文章列表——主平台金猫规则列表——金猫规则菜单列表——金猫规则详情
import pytest
import random

from swagger_client.staff.api.content_management_api import ContentManagementApi
from common.account_sign import get_admin_token
from common.account_sign import set_login_status
from swagger_client.main.api.kinmall_management_api import KinmallManagementApi


class TestKinMallCase12(object):

    @pytest.mark.order1
    def test_kin_mall_case12(self):
        # 后台登录
        content_api = ContentManagementApi()
        staff_token = get_admin_token()
        set_login_status(content_api, staff_token)
        # 新建文章模型
        identification = '模型标识' + str(random.randint(10000, 99999))
        name = '文章模型' + str(random.randint(10000, 99999))
        payload = {
            'identification': identification,
            'name': name,
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
        identification = '模型标识' + str(random.randint(1000, 9999))
        name = '文章模型' + str(random.randint(1000, 9999))
        sub_payload = {
            "identification": identification,
            "name": name,
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
        # 主平台金猫规则列表
        kin_mall_api = KinmallManagementApi()
        res = kin_mall_api.kinmalls_get(type='kinmall', title=payload1['title'])
        id_ = ''
        for item in res.items:
            if item.title == payload1['title']:
                id_ = item.id
        # 主平台金猫规则菜单列表
        sub = {}
        res = kin_mall_api.kinmalls_menus_get()
        for item in res.items:
            if item.name == payload['name']:
                sub = item.submenu
                for i in sub:
                    assert i.name == sub_payload['name']
        # 主平台规则详情
        res = kin_mall_api.kinmalls_id_get(id=id_)
        assert res.author == payload1['author']
        assert res.content == payload1['content']
        assert res.title == payload1['title']
