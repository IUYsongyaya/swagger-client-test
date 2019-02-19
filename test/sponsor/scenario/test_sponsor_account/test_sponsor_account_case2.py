#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/11 16:37
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 后台创建保荐方账号——忘记密码——登录保荐方
from faker import Faker
import pytest

from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from common.utils import get_random_name
from common.account_sign import get_admin_token, get_sponsor_token
from common.account_sign import set_login_status
from swagger_client.sponsor.api.sponsor_api import SponsorApi
from swagger_client.sponsor.api.verification_api import VerificationApi
from swagger_client.sponsor.api.sponsors_managerment_api import SponsorsManagermentApi as SponApi


class TestSponsorAccountCase2(object):

    @pytest.mark.order1
    def test_sponsor_account_case2(self):
        faker = Faker()
        # 创建保健方账号
        staff_api = SponsorsManagermentApi()
        staff_token = get_admin_token()
        set_login_status(staff_api, staff_token)
        sponsor = {"account": get_random_name(6, 50), "password": faker.password(),
                   "name": faker.user_name(), "email": faker.email(),
                   "phone": faker.phone_number()}
        staff_api.staff_sponsors_post(post_sponsor=sponsor)
        # 极验初始化
        verification_api = VerificationApi()
        challenge = ''
        res = verification_api.accounts_init_captcha_get()
        assert res.new_captcha == 'true'
        assert res.success == '1'
        challenge = res.challenge
        # 获取绑定的手机和邮箱
        api = SponsorApi()
        api.sponsor_info_post(sponsor_info={"userName": sponsor['account'],
                                            "challenge": challenge,
                                            "seccode": "fdhfghfdghfghfjhfghfasfas",
                                            "validate": "dfhdfgdfgfdgfdgsadfasfas"})
        # 二次验证
        base_token = ''
        res = api.sponsor_verify_post(post_verify_request={"userName": sponsor['account'],
                                                           "uri": "mailto:" + str(sponsor['email']),
                                                           "code": "666666",
                                                           "type": "forget_pwd"})
        base_token = res.base_token
        # 重置密码
        set_password = {"password": faker.password()}
        api.sponsor_set_password_post(sponsor_rest_pwd={"userName": sponsor['account'],
                                                        "baseToken": base_token,
                                                        "password": set_password['password']})
        # 保荐方登录
        sponsor_api = SponApi()
        get_sponsor_token(account=sponsor.get("account"),
                          password=set_password.get("password"),
                          email=sponsor.get("email"), api_list=[sponsor_api, api])
        # 获取保荐方排行榜
        res = sponsor_api.sponsors_ranking_get(page=1)
        assert res.ranking == res.meta.total_count
        # 保荐方退出
        api.sponsor_logout_post()
