#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/11 14:33
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 后台创建保荐方账号——登录保荐方——退出保荐方
from faker import Faker
import pytest

from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from common.utils import get_random_name
from common.account_sign import get_admin_token, get_sponsor_token
from common.account_sign import set_login_status
from swagger_client.sponsor.api.sponsor_api import SponsorApi


class TestSponsorAccountCase1(object):

    @pytest.mark.order1
    def test_sponsor_account_case1(self):
        faker = Faker()
        # 创建保健方账号
        staff_api = SponsorsManagermentApi()
        staff_token = get_admin_token()
        set_login_status(staff_api, staff_token)
        sponsor = {"account": get_random_name(6, 50), "password": faker.password(),
                   "name": faker.user_name(), "email": faker.email(),
                   "phone": faker.phone_number()}
        staff_api.staff_sponsors_post(post_sponsor=sponsor)
        # 保健方登
        api = SponsorApi()
        get_sponsor_token(account=sponsor.get("account"),
                          password=sponsor.get("password"),
                          email=sponsor.get("email"), api_list=[api])
        # 保荐方退出
        api.sponsor_logout_post()
