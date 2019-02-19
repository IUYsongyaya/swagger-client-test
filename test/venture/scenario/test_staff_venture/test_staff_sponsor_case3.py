#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/24 15:30
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 后台新建保荐方——获取保荐方列表——修改保荐方信息——获取保荐方列表
from faker import Faker

from common.utils import get_random_name
from common.account_sign import set_login_status
from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from common.account_sign import get_admin_token


class TestSponsorsCase3(object):

    def test_sponsors_case3(self):
        faker = Faker()
        # 创建保健方账号
        staff_api = SponsorsManagermentApi()
        staff_token = get_admin_token()
        set_login_status(staff_api, staff_token)
        sponsor = {"account": get_random_name(6, 25), "password": faker.password(),
                   "name": faker.user_name(), "email": faker.email(),
                   "phone": faker.phone_number()}
        staff_api.staff_sponsors_post(post_sponsor=sponsor)
        # 管理后台获取保健列表
        res = staff_api.staff_sponsors_get(page=1, name=sponsor.get("name"))
        sponsor_id = ''
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.account == sponsor.get("account")
            assert item.email == sponsor.get("email")
            assert item.name == sponsor.get("name")
            assert item.status is True
            sponsor_id = item.id
        # 修改保荐方信息
        payload1 = {
            'id': sponsor_id,
            'logo': 'url/images',
            'website': 'www.baidu.com',
            'summary': '这是简介',
            'password': 'aaaaa888',
            'phone': '13877778888',
            'email': '654321@qq.com'
        }
        staff_api.staff_sponsors_put(put_sponsor=payload1)
        # 获取保荐方列表
        res = staff_api.staff_sponsors_get(page=1)
        for item in res.items:
            if item.name == sponsor.get("name"):
                assert item.account == sponsor.get("account")
                assert item.email == payload1['email']
                assert item.status is True
                assert item.id
