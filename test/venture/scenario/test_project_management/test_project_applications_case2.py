#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/15 15:25
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 申请项目——查看申请列表——修改申请项目信息——查看申请详情

from faker import Faker
import pytest
import random
import copy

from swagger_client.venture.api.project_api import ProjectApi
from swagger_client.venture.rest import ApiException
from common.certification_verify import individual_verify
from swagger_client.venture.api.sponsors_managerment_api import SponsorsManagermentApi as SMApi
from common.utils import (PlatformManager, random_get_country_ob,
                          get_random_id_number, get_random_name)
from common.account_sign import set_login_status
from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from common.account_sign import get_admin_token
from swagger_client.venture.models.application_request import ApplicationRequest
from test.venture.scenario.config import payload
from test.venture.scenario.rand_email import random_email


class TestProjectCase2(object):
    @pytest.mark.order1
    def test_applications2(self):
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
        # 申请项目
        project_name = get_random_name(2, 16)
        short_name = "I" + str(random.randint(10000, 99999))
        full_name = get_random_name(2, 16)
        project_api = ProjectApi()
        set_login_status(project_api, token)
        pay = copy.deepcopy(dict(payload))
        pay.update({'project_name': project_name,
                    'short_name': short_name,
                    'full_name': full_name})
        req = ApplicationRequest(**pay)
        res = project_api.applications_post(body=req)
        project_apply_id = res.id
        # 创建保健方账号
        staff_api = SponsorsManagermentApi()
        staff_token = get_admin_token()
        set_login_status(staff_api, staff_token)
        sponsor = {"account": get_random_name(6, 25), "password": faker.password(),
                   "name": faker.user_name(), "email": faker.email(),
                   "phone": faker.phone_number()}
        staff_api.staff_sponsors_post(post_sponsor=sponsor)
        # 项目方获取保健列表
        venture_api = SMApi()
        set_login_status(venture_api, token)
        res = venture_api.sponsors_get(page=1, name=sponsor.get("name"))
        item = res.items.pop()
        sponsor_id = item.id
        # 项目方设置保健方
        project_api.applications_id_set_sponsor_put(
            id=project_apply_id, sponsor_request={"sponsorId": sponsor_id})
        # 查看项目申请列表
        res = project_api.applications_get(page=1)
        project_id = ''
        for item in res.items:
            assert item.project_name == project_name
            assert item.fullname == full_name
            assert item.short_name == short_name
            assert item.status == 'under_review'
            project_id = item.id
        # 查看申请项目详情
        res = project_api.applications_id_get(id=project_id)
        assert res.sponsor_id == sponsor_id
        assert res.sponsor_name == sponsor.get("name")
        assert res.id == project_id
        assert res.project_name == project_name
        assert res.short_name == short_name
        assert res.full_name == full_name
        assert res.status == 'under_review'
        # 修改申请项目
        project_name1 = '项目方' + str(random.randint(1000, 9999))
        full_name1 = 'BitCoin' + str(random.randint(1000, 9999))
        short_name1 = 'BTC' + str(random.randint(100, 999))
        payload2 = {
            'project_name': project_name1,
            'description': 'XXXXXXXXXXXXXXXX',
            'official_website': 'www.xxxx.com',
            'white_paper_key': 'url/pdf123455',
            'area_code': '+86',
            "project_poster_key": "123455",
            'cellphone': '13510022445',
            'telephone': '12874846',
            'email': '1234832456@qq.com',
            'full_name': full_name1,
            'short_name': short_name1,
            'issue_price': '2.24545',
            'issued_volume': '1000000',
            'circulation_volume': '1000000',
            "coin_logo_key": "456455",
            'blockchain_type': 'public_chain',
            'data_link': 'www.baidu.com',
            'block_browser': 'www.baidu.com'
        }
        req = ApplicationRequest(**payload2)
        try:
            project_api.applications_id_put(id=project_id, body=req)
        except ApiException as apiexc:
            assert apiexc.status == 400
        else:
            assert False
        # # 查看项目申请列表
        # res = project_api.applications_get(page=1)
        # id_put = ''
        # for item in res.itmes:
        #     assert item.project_name == project_name
        #     assert item.full_name == full_name
        #     assert item.short_name == short_name
        #     assert item.status == 'under_review'
        #     assert item.project_id == project_id
        #     id_put = item.project_id
        # # 查看申请项目详情
        # res = project_api.applications_id_get(id=id_put)
        # assert res.sponsor_id == sponsor_id
        # assert res.sponsor_name == sponsor.get("name")
        # assert res.id == id_put
        # assert res.project_name == project_name
        # assert res.short_name == short_name
        # assert res.full_name == full_name
        # assert res.status == 'under_review'
