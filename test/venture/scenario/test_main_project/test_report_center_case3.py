#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/22 15:35
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 废弃
# 新增项目报告成功（项目方）——获取报告列表（项目方）——项目报告列表
# from faker import Faker
# import pytest
# import random
#
# from swagger_client.venture.api.project_api import ProjectApi
# from swagger_client.sponsor.api.sponsors_project_api import SponsorsProjectApi
# from common.certification_verify import individual_verify
# from swagger_client.venture.api.sponsors_managerment_api import SponsorsManagermentApi as SMApi
# from common.utils import (PlatformManager, random_get_country_ob,
#                           get_random_id_number, get_random_name)
# from common.account_sign import set_login_status
# from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
# from common.account_sign import get_admin_token, get_sponsor_token
# from swagger_client.venture.models.application_request import ApplicationRequest
# from swagger_client.tenant.api.account_api import AccountApi
# from swagger_client.staff.api.website_management_api import WebsiteManagementApi
# from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
# from swagger_client.staff.api.audit_api import AuditApi
# from swagger_client.venture.api.project_management_api import ProjectManagementApi
# from swagger_client.venture.api.contacts_api import ContactsApi
# from swagger_client.tenant.api.contacts_api import ContactsApi as ExchangeContacts
# from swagger_client.staff.api.asset_management_api import AssetManagementApi
# from swagger_client.venture.models.post_report_request import PostReportRequest
# from swagger_client.venture.api.report_management_api import ReportManagementApi
# from swagger_client.main.api.project_api import ProjectApi as MainProject
#
#
# class TestReportCenterCase3(object):
#
#     @pytest.mark.order1
#     def test_report_center_case3(self):
#         faker = Faker()
#         manager = PlatformManager("venture")
#         email = faker.email()
#         password = faker.password()
#         country = random_get_country_ob()
#         manager.register(email=email, password=password,
#                          promotion_code=None, verification_code="666666",
#                          country=country.get("k"), nick_name='fghfg')
#         token = manager.login(account=email, password=password)
#         # 个人实名认证
#         individual_verify(platform="venture", id_number=get_random_id_number(), token=token)
#         # 申请项目
#         project_api = ProjectApi()
#         set_login_status(project_api, token)
#         project_name = get_random_name(2, 16)
#         short_name = get_random_name(2, 6)
#         full_name = get_random_name(2, 16)
#         payload = {
#             "project_name": project_name,
#             "description": "{}-description".format(project_name),
#             "official_website": "www.{}.com".format(project_name),
#             "white_paper_key": "{}-whitePaper".format(project_name),
#             "area_code": "+86",
#             "project_poster_key": "123455",
#             "cellphone": "123456789",
#             "telephone": "12345678910",
#             "email": faker.email(),
#             "full_name": full_name,
#             "short_name": short_name,
#             "issue_price": "2.24545",
#             "issued_volume": "1000000",
#             "circulation_volume": "1000000",
#             "issued_date": "2018-08-08",
#             "coin_logo_key": "456455",
#             "blockchain_type": "public_chain",
#             "data_link": "{}-data-link".format(project_name),
#             "block_browser": "{}-block-Browser".format(project_name)
#         }
#         req = ApplicationRequest(**payload)
#         res = project_api.applications_post(body=req)
#         project_apply_id = res.id
#         # 创建保健方账号
#         staff_api = SponsorsManagermentApi()
#         staff_token = get_admin_token()
#         set_login_status(staff_api, staff_token)
#         sponsor = {"account": get_random_name(6, 50), "password": faker.password(),
#                    "name": faker.user_name(), "email": faker.email(),
#                    "phone": faker.phone_number()}
#         staff_api.staff_sponsors_post(post_sponsor=sponsor)
#         # 新建交易所标签
#         website_api = WebsiteManagementApi()
#         set_login_status(website_api, staff_token)
#         website = {"name": "交易所标签" + str(random.randint(10000, 99999)),
#                    "otherLanguage": [{
#                        "key": "英语",
#                        "value": "public_chain"
#                    },
#                        {
#                            "key": "法语",
#                            "value": "public_chain"
#                        }]
#                    }
#         website_api.exchange_tags_post(body=website)
#         # 项目方获取保健列表
#         venture_api = SMApi()
#         set_login_status(venture_api, token)
#         res = venture_api.sponsors_get(page=1, name=sponsor.get("name"))
#         item = res.items.pop()
#         sponsor_id = item.id
#         # 项目方设置保健方
#         project_api.applications_id_set_sponsor_put(
#             id=project_apply_id, sponsor_request={"sponsorId": sponsor_id})
#         # 保健方登
#         # 保健项目
#         sponsor_api = SponsorsProjectApi()
#         get_sponsor_token(account=sponsor.get("account"),
#                           password=sponsor.get("password"),
#                           email=sponsor.get("email"), api_list=[sponsor_api])
#         sponsor_api.projects_sponsor_put(put_project_sponsor_request={
#             "id": project_apply_id,
#             "status": 1,
#             "remark": "remark"
#         }
#         )
#         # 币种配置列表
#         asset_api = AssetManagementApi()
#         set_login_status(asset_api, staff_token)
#         res = asset_api.asset_mgmt_coins_get(page=1, coin_name=short_name)
#         coin_id = ''
#         assert res.meta.total_count == 1
#         for item in res.coin_info:
#             assert item.coin_name == short_name
#             coin_id = item.id
#         # 初始化币种配置
#         payload = {
#                       "usdtPrice": "1",
#                       "rcTimes": 0,
#                       "wcTimes": 0,
#                       "withdrawRate": "1",
#                       "minWithdrawFee": "1",
#                       "minWithdraw": "1",
#                       "maxWithdraw": "1",
#                       "dayWithdrawTotal": "1",
#                       "minRecharge": "1",
#                       "addressTagSwitch": True,
#                       "addressType": "1",
#                       "addressUrl": "1",
#                       "txidUrl": "1"
#                     }
#         asset_api.asset_mgmt_coins_id_init_put(id=coin_id, body=payload)
#         # 授权登录
#         api = AccountApi()
#         set_login_status(api, token)
#         api.create_platform()
#         # 提交交易所申请
#         exchange_api = ExchangeManagementApi()
#         set_login_status(exchange_api, token)
#         exchange = {
#             "email": email,
#             "logo": "gdfgdvdfvdf",
#             "name": faker.user_name(),
#             "nationality": "+86",
#             "phone": '+86135678' + str(random.randint(10000, 99999)),
#             "tags": website['name']
#         }
#         exchange_api.exchange_post(exchange)
#         # 交易所账号审核列表
#         audit_api = AuditApi()
#         set_login_status(audit_api, staff_token)
#         res = audit_api.tenant_audits_get(exchange_name=exchange['name'])
#         audit_id = ''
#         for item in res.items:
#             audit_id = item.id
#         # 交易所初审
#         audit = {
#             "failureType": "string",
#             "id": audit_id,
#             "isDataReceived": True,
#             "status": "approved"
#         }
#         audit_api.tenant_audits_audit_post(body=audit)
#         # 交易所账号审核列表
#         res = audit_api.tenant_audits_get(exchange_name=exchange['name'])
#         re_audit_id = ''
#         for item in res.items:
#             re_audit_id = item.id
#         # 交易所账号复审
#         re_audit = {
#             "failureType": "string",
#             "id": re_audit_id,
#             "status": "approved"
#         }
#         audit_api.tenant_audits_re_audit_post(body=re_audit)
#         # 申请接入交易所
#         exchange_project_api = ProjectManagementApi()
#         set_login_status(exchange_project_api, token)
#         res = exchange_project_api.projects_id_exchanges_get(id=coin_id, exchange_name=exchange['name'])
#         exchange_id = ''
#         for item in res.items:
#             exchange_id = item.exchange_id
#         # 申请对接
#         contacts_api = ContactsApi()
#         set_login_status(contacts_api, token)
#         contacts = {
#             "exchangeId": exchange_id,
#             "projectId": coin_id,
#             "sponsor": "venture"
#         }
#         contacts_api.contacts_post(contacts)
#         # 获取交易所对接的项目列表
#         exchange_contacts_api = ExchangeContacts()
#         set_login_status(exchange_contacts_api, token)
#         res = exchange_contacts_api.contacts_projects_exchange_id_get(exchange_id=exchange_id, status="pending")
#         contacts_id = ''
#         for item in res.items:
#             contacts_id = item.id
#         # 交易所处理对接邀请—接受
#         contacts = {
#             "contactId": contacts_id,
#             "status": "accepted"
#         }
#         exchange_contacts_api.contacts_put(body=contacts)
#         # 获取项目列表
#         res = project_api.projects_get(page=1)
#         audit_project_id = ''
#         for item in res.items:
#             assert item.project_name == project_name
#             assert item.full_name == full_name
#             assert item.short_name == short_name
#             audit_project_id = item.project_id
#         # 发送项目报告
#         report_api = ReportManagementApi()
#         set_login_status(report_api, token)
#         payload = {
#                       "title": "项目报告" + str(random.randint(1000, 9999)),
#                       "type": "daily",
#                       "report_url": "C:\pc\Desktop\wanshare.pdf",
#                       "project_id": audit_project_id
#                     }
#         req = PostReportRequest(**payload)
#         report_api.reports_post(body=req)
#         # 获取报告列表
#         res = report_api.reports_project_id_get(project_id=audit_project_id)
#         assert res.meta.total_count == 1
#         for item in res.items:
#             assert item.title == payload['title']
#             assert item.type == payload['type']
#             assert item.id
#         # 主平台获取项目列表
#         main_project_api = MainProject()
#         res = main_project_api.projects_get(page=1, sort_key="volume", limit=100)
#         print(full_name)
#         print(res)
