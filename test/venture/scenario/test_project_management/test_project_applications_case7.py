#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/06 16:22
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 交易所向项目方发起申请——项目方设置接入方式无需验证——接入成功
from faker import Faker
import pytest
import random
import copy

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
from swagger_client.tenant.api.account_api import AccountApi
from swagger_client.staff.api.website_management_api import WebsiteManagementApi
from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
from swagger_client.staff.api.audit_api import AuditApi
from swagger_client.venture.api.contacts_api import ContactsApi
from swagger_client.tenant.api.contacts_api import ContactsApi as ExchangeContacts
from swagger_client.staff.api.asset_management_api import AssetManagementApi
from swagger_client.tenant.api.project_api import ProjectApi as ExchangeProject
from test.venture.scenario.config import payload
from test.venture.scenario.rand_email import random_email


class TestProjectCase8(object):

    @pytest.mark.order1
    def test_applications8(self):
        faker = Faker()
        manager = PlatformManager("venture")
        email = random_email()
        password = faker.password()
        country = random_get_country_ob()
        manager.register(email=email, password=password,
                         promotion_code=None, verification_code="666666",
                         nationality_code=country.get("k"), nick_name='fghfg')
        token = manager.login(account=email, password=password)
        # 个人实名认证
        individual_verify(platform="venture", id_number=get_random_id_number(), token=token)
        # 申请项目
        project_name = get_random_name(2, 16)
        short_name = "N" + str(random.randint(10000, 99999))
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
        # 新建交易所标签
        website_api = WebsiteManagementApi()
        set_login_status(website_api, staff_token)
        website = {"name": "交易所标签" + str(random.randint(10000, 99999)),
                   "otherLanguage": [{
                       "key": "英语",
                       "value": "public_chain"
                   },
                       {
                           "key": "法语",
                           "value": "public_chain"
                       }]
                   }
        website_api.exchange_tags_post(body=website)
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
        # 获取项目列表
        res = project_api.projects_get(page=1)
        audit_project_id = ''
        for item in res.items:
            assert item.project_name == project_name
            assert item.full_name == full_name
            assert item.short_name == short_name
            audit_project_id = item.project_id
        # 修改申请项目
        payload1 = {
            "setting":
                {
                    "open": True,
                    "accessMethod": "accept"
                }
        }
        project_api.projects_id_put(id=audit_project_id, type="setting", body=payload1)
        # 币种配置列表
        asset_api = AssetManagementApi()
        set_login_status(asset_api, staff_token)
        res = asset_api.asset_mgmt_coins_get(page=1, coin_name=short_name)
        coin_id = ''
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.coin_name == short_name
            coin_id = item.id
        # 初始化币种配置
        payload2 = {
                      "usdtPrice": "1",
                      "rcTimes": 0,
                      "wcTimes": 0,
                      "withdrawRate": "1",
                      "minWithdrawFee": "1",
                      "minWithdraw": "1",
                      "maxWithdraw": "1",
                      "dayWithdrawTotal": "1",
                      "minRecharge": "1",
                      "addressTagSwitch": True,
                      "addressType": "1",
                      "addressUrl": "1",
                      "txidUrl": "1"
                    }
        asset_api.asset_mgmt_coins_id_init_put(id=coin_id, body=payload2)
        # 授权登录
        api = AccountApi()
        set_login_status(api, token)
        api.create_platform()
        # 提交交易所申请
        exchange_api = ExchangeManagementApi()
        set_login_status(exchange_api, token)
        exchange = {
            "email": email,
            "logo": "gdfgdvdfvdf",
            "name": "交易所" + str(random.randint(10000, 99999)),
            "nationality": "+86",
            "phone": '+86135678' + str(random.randint(10000, 99999)),
            "tags": website['name']
        }
        exchange_api.exchange_post(exchange)
        # 交易所账号审核列表
        audit_api = AuditApi()
        set_login_status(audit_api, staff_token)
        res = audit_api.tenant_audits_get(exchange_name=exchange['name'])
        audit_id = ''
        for item in res.items:
            audit_id = item.id
        # 交易所初审
        audit = {
            "failureType": "string",
            "id": audit_id,
            "isDataReceived": True,
            "status": "approved"
        }
        audit_api.tenant_audits_audit_post(body=audit)
        # 交易所账号审核列表
        res = audit_api.tenant_audits_get(exchange_name=exchange['name'])
        re_audit_id = ''
        for item in res.items:
            re_audit_id = item.id
        # 交易所账号复审
        re_audit = {
            "failureType": "string",
            "id": re_audit_id,
            "status": "approved"
        }
        audit_api.tenant_audits_re_audit_post(body=re_audit)
        # 获取交易所id
        exchange_id_ = ''
        res = exchange_api.exchange_exchange_id_get()
        exchange_id_ = res.id
        # 获取项目列表
        exchange_project_api = ExchangeProject()
        set_login_status(exchange_project_api, token)
        project_id = ''
        res = exchange_project_api.projects_get(coin_name=short_name)
        for item in res.items:
            if item.full_name == full_name:
                project_id = item.project_id
        # 申请对接
        contacts_api = ExchangeContacts()
        set_login_status(contacts_api, token)
        contacts = {
            "exchangeId": exchange_id_,
            "projectId": project_id,
            "sponsor": "tenant"
        }
        contacts_api.contacts_post(contacts)
        # 判断项目方与交易所是否已经申请对接
        contacts_project_api = ContactsApi()
        set_login_status(contacts_project_api, token)
        res = contacts_project_api.contacts_check_get(project_id=project_id, exchange_id=exchange_id_)
        assert res.result is True
