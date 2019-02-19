#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/22 16:45
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 废弃
# 新增项目新闻资讯成功（项目方）——获取项目资讯列表（项目方）——新闻快讯列表——项目新闻快讯详情
# import pytest
# import random
#
# from common.account_sign import register_with_login
# from swagger_client.venture.models.application_request import ApplicationRequest
# from swagger_client.venture.api.project_api import ProjectApi
# from swagger_client.venture.api.new_management_api import NewManagementApi
# from swagger_client.venture.models.post_news_request import PostNewsRequest
# from swagger_client.main.api.project_api import ProjectApi as MainProject
# from swagger_client.main.api.news_management_api import NewsManagementApi as MainNews
#
# api = ProjectApi()
# new_api = NewManagementApi()
# main_api = MainProject()
# main_news_api = MainNews()
#
#
# class TestProjectCase10(object):
#
#     @pytest.mark.order1
#     def test_applications(self, kin_mall_audit_project, staff_sponsors, individual_verify, with_login):
#         # 登录
#         user = register_with_login('venture', with_login, [api])
#         token = user['token']
#         id_number = '232332199003' + str(random.randint(100000, 999999))
#         # 个人实名认证
#         individual_verify('venture', id_number, token)
#         sponsors_id = staff_sponsors[1]
#         sponsors_payload = staff_sponsors[0]
#         project_name = '项目方' + str(random.randint(1000, 9999))
#         full_name = 'BitCoin' + str(random.randint(1000, 9999))
#         short_name = 'BTC' + str(random.randint(1000, 9999))
#         payload = {
#             'project_name': project_name,
#             'description': 'XXXXXXXXXXXXXXXX',
#             'official_website': 'www.xxxx.com',
#             'white_paper': 'url/pdf123455',
#             'area_code': '+86',
#             'project_poster': 'url/image123455',
#             'cellphone': '13510022445',
#             'telephone': '12874846',
#             'email': '1234832456@qq.com',
#             'full_name': full_name,
#             'short_name': short_name,
#             'issue_price': '2.24545',
#             'issued_volume': '1000000',
#             'circulation_volume': '1000000',
#             'issued_at': '2018-08-08',
#             'coin_logo': 'url/image456455',
#             'blockchain_type': 'public_chain',
#             'data_link': 'www.baidu.com',
#             'block_browser': 'www.baidu.com'
#         }
#         req = ApplicationRequest(**payload)
#         # 申请项目
#         res = api.applications_post(body=req)
#         project_id = res.id
#         # 设置保荐方
#         sponsors_put = {'sponsor_id': sponsors_id
#                         }
#         sponsors_req = ApplicationRequest(**sponsors_put)
#         api.applications_id_set_sponsor_put(id=project_id, body=sponsors_req)
#         # 保荐方审核项目通过
#         kin_mall_audit_project(project_name, 'accept')
#         # 获取项目列表
#         id_ = ''
#         res = api.projects_get(page=1)
#         for item in res.items:
#             if item.projectName == project_name:
#                 id_ = item.projectId
#         # 获取项目新闻资讯列表
#         res = new_api.news_project_id_get(project_id=id_)
#         total = res.meta.totalCount
#         assert res.meta.totalCount == 0
#         # 发送新闻资讯
#         payload = {
#             'title': '新闻资讯' + str(random.randint(1000, 9999)),
#             'link': 'www.baidu.com',
#             'source': '百度',
#             'project_id': id_
#         }
#         req = PostNewsRequest(**payload)
#         new_api.news_post(body=req)
#         # 主平台获取项目列表
#         res = main_api.projects_get()
#         main_project_id = ''
#         for item in res.items:
#             if item.fullName == full_name:
#                 main_project_id = item.projectId
#         # 主平台获取新闻快讯列表
#         res = main_news_api.project_news_project_id_get(project_id=main_project_id)
#         for item in res.items:
#             assert not item.id
#             assert item.title == payload['title']
