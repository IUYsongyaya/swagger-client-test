#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/15 17:21
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 获取文章模型列表——新增文章（文章列表需要PlatformNotice）——主平台文章列表——平台文章详情——平台文章详情
import pytest
import random
from faker import Faker

from common.utils import PlatformManager, random_get_country_ob
from swagger_client.staff.api.content_management_api import ContentManagementApi
from common.account_sign import get_admin_token
from common.account_sign import set_login_status
from swagger_client.main.api.platform_article_management_api import PlatformArticleManagementApi
from test.venture.scenario.rand_email import random_email


class TestPlatformArticleCase13(object):

    @pytest.mark.order1
    def test_platform_article_case13(self):
        faker = Faker()
        manager = PlatformManager("main")
        email = random_email()
        password = faker.password()
        country = random_get_country_ob()
        manager.register(email=email, password=password,
                         promotion_code=None, verification_code="666666",
                         nationality_code=country.get("k"))
        token = manager.login(account=email, password=password)
        # 后台登录
        content_api = ContentManagementApi()
        staff_token = get_admin_token()
        set_login_status(content_api, staff_token)
        # 获取文章模型列表
        models_id = ''
        page = 1
        res = content_api.models_get(type='article', page=page)
        total_page = res.meta.total_page
        while page <= total_page:
            res = content_api.models_get(type='article', page=page)
            for item in res.items:
                if item.name == '公告中心':
                    assert item.status is True
                    assert item.type == 'article'
                    models_id = item.id
            page += 1
        # 新建documents文章
        payload1 = {
            "author": "作者" + str(random.randint(10000, 99999)),
            "content": "文章内容" + str(random.randint(10000, 99999)),
            "isTop": True,
            "language": "zh_cn",
            "modelId": models_id,
            "order": str(random.randint(10000, 99999)),
            "status": True,
            "title": "文章标题" + str(random.randint(10000, 99999)),
            "type": "article"
        }
        content_api.documents_post(body=payload1)
        # 主平台平台文章列表
        platform_api = PlatformArticleManagementApi()
        documents_id = ''
        page = 1
        res = platform_api.platform_articles_get(identification='PlatformNotice', language='zh_cn')
        total_page = res.meta.total_page
        while page <= total_page:
            res = platform_api.platform_articles_get(identification='PlatformNotice', language='zh_cn')
            for item in res.items:
                if item.title == payload1['title']:
                    assert item.id
                    assert item.read is False
                    documents_id = item.id
            page += 1
        # 主平台获取文章详情
        res = platform_api.platform_articles_id_get(id=documents_id)
        assert res.title == payload1['title']
        assert res.read is False
        assert res.content == payload1['content']
        # 主平台文章已读
        set_login_status(platform_api, token)
        platform_api.platform_articles_id_mark_read_put(id=documents_id)
        # 主平台平台文章列表
        page = 1
        res = platform_api.platform_articles_get(identification='PlatformNotice', language='zh_cn')
        total_page = res.meta.total_page
        while page <= total_page:
            res = platform_api.platform_articles_get(identification='PlatformNotice', language='zh_cn')
            for item in res.items:
                if item.title == payload1['title']:
                    assert item.id
                    assert item.read is True
            page += 1
