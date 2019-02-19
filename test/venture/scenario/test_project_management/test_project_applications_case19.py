#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/21 17:30
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 重复申请项目——>项目名相同
from faker import Faker
import pytest
import copy
import random

from swagger_client.venture.api.project_api import ProjectApi
from swagger_client.sponsor.api.sponsors_project_api import SponsorsProjectApi
from common.certification_verify import individual_verify
from swagger_client.venture.api.sponsors_managerment_api import SponsorsManagermentApi as SMApi
from common.utils import (PlatformManager, random_get_country_ob,
                          get_random_id_number, get_random_name)
from common.account_sign import set_login_status
from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from common.account_sign import get_admin_token, get_sponsor_token
from swagger_client.venture.models.application_request import ApplicationRequest
from swagger_client.staff.api.project_api import ProjectApi as Sta_project
from swagger_client.venture.rest import ApiException
import json
from test.venture.scenario.config import payload
from test.venture.scenario.rand_email import random_email


class TestProjectCase19(object):

    @pytest.mark.order1
    def test_applications19(self):
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
        short_name = "Y" + str(random.randint(10000, 99999))
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
        # 保健方登
        # 保健项目
        sponsor_api = SponsorsProjectApi()
        get_sponsor_token(account=sponsor.get("account"),
                          password=sponsor.get("password"),
                          email=sponsor.get("email"), api_list=[sponsor_api])
        sponsor_api.projects_sponsor_put(put_project_sponsor_request={
            "id": project_apply_id,
            "status": 1,
            "remark": "remark"
        }
        )
        # 后台获取所有项目列表
        staff_project = Sta_project()
        set_login_status(staff_project, token)
        res = staff_project.projects_get(project_name=project_name)
        up_project_name = ''
        for item in res.items:
            up_project_name = item.project_name
        # 申请项目
        try:
            full_name1 = get_random_name(2, 16)
            short_name1 = get_random_name(2, 6)
            payload1 = {
                "project_name": project_name,
                "description": "{}-description".format(project_name),
                "official_website": "www.{}.com".format(project_name),
                "white_paper_key": "{}-whitePaper".format(project_name),
                "area_code": "+86",
                "project_poster_key": "123455",
                "cellphone": "123456789",
                "telephone": "12345678910",
                "email": faker.email(),
                "full_name": full_name1,
                "short_name": short_name1,
                "issue_price": "2.24545",
                "issued_volume": "1000000",
                "circulation_volume": "1000000",
                "issued_date": "2018-08-08",
                "coin_logo_key": "456455",
                "blockchain_type": "public_chain",
                "data_link": "{}-data-link".format(project_name),
                "block_browser": "{}-block-Browser".format(project_name)
            }
            req = ApplicationRequest(**payload1)
            project_api.applications_post(body=req)
        except ApiException as e:
            assert e.status == 400
            message = json.loads(e.body)['message']
            assert message == '项目名称已经存在'
        else:
            assert False
