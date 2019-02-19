#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/24 16:19
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 后台新建保荐方——获取保荐方列表——项目方获取保荐方列表
from faker import Faker

from common.account_sign import set_login_status
from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from common.account_sign import get_admin_token
from swagger_client.venture.api.sponsors_managerment_api import SponsorsManagermentApi as SMApi
from common.utils import (PlatformManager, random_get_country_ob,
                          get_random_id_number, get_random_name)
from common.certification_verify import individual_verify
from test.venture.scenario.rand_email import random_email


class TestSponsorsCase5(object):

    def test_sponsors_case5(self):
        faker = Faker()
        manager = PlatformManager("venture")
        email = random_email()
        password = faker.password()
        country = random_get_country_ob()
        manager.register(email=email, password=password,
                         promotion_code=None, verification_code="666666",
                         nationality_code=country.get("k"))
        token = manager.login(account=email, password=password)
        # 个人实名认证
        individual_verify(platform="venture", id_number=get_random_id_number(), token=token)
        # 创建保健方账号
        staff_api = SponsorsManagermentApi()
        staff_token = get_admin_token()
        set_login_status(staff_api, staff_token)
        sponsor = {"account": get_random_name(6, 25), "password": faker.password(),
                   "name": faker.user_name(), "email": email,
                   "phone": faker.phone_number()}
        staff_api.staff_sponsors_post(post_sponsor=sponsor)
        # 管理后台获取保健列表
        res = staff_api.staff_sponsors_get(page=1, name=sponsor.get("name"))
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.account == sponsor.get("account")
            assert item.email == sponsor.get("email")
            assert item.name == sponsor.get("name")
            assert item.status is True
            assert item.id
        # 项目方获取保健列表
        venture_api = SMApi()
        set_login_status(venture_api, token)
        res = venture_api.sponsors_get(page=1, name=sponsor.get("name"))
        item = res.items.pop()
        assert item.name == sponsor.get("name")
        assert item.id
