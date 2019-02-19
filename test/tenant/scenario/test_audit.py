# # @Author  : ymy
# # @Email   : yaomingyong@wanshare.com
# # @Time    : 18-11-19 下午4:57
#
# import pytest
# import random
#
# from common.account_sign import register_with_login
# from swagger_client.tenant.rest import ApiException
# from swagger_client.staff.api.audit_api import AuditApi
# from swagger_client.tenant.api.account_api import AccountApi
# from common.utils import PlatformManager, random_get_country_code, get_random_id_number
# from common.certification_verify import individual_verify, company_verify
# from swagger_client.tenant.models.get_exchange_request import GetExchangeRequest
# from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
# from swagger_client.staff.models.post_tenant_audit_request import PostTenantAuditRequest
# from swagger_client.staff.models.post_tenant_re_audit_request import PostTenantReAuditRequest
#
#
# admin, password = '', ''
# img = 'http://www.example.com/test1.png'
#
#
# def get_random_exchange_name():
#     exchange_api = ExchangeManagementApi()
#     name = '宇宙交易所' + str(random.randint(1, 10000))
#     while True:
#         try:
#             return exchange_api.exchange_exchange_name_verify_get(name)
#         except ApiException as e:
#             if e.status == 400:
#                 # 名称已经存在
#                 name = '宇宙交易所' + str(random.randint(1, 10000))
#             else:
#                 raise
#
#
# @pytest.fixture
# def exchange(tags):
#     random_country = random_get_country_code()
#     # 随机取几个tag
#     amount = random.randint(1, len(tags))
#     tag = random.sample(tags, amount)
#     g = GetExchangeRequest()
#     g.name = get_random_exchange_name()
#     g.nationality = '+' + random_country['n']
#     g.logo = img
#     g.tags = tag
#     return g
#
#
# def search_tenant_audits(account_id):
#     manager = PlatformManager('tenant')
#     admin_token = manager.login(admin, password)
#     audit_api = AuditApi()
#     audit_api.api_client.set_default_header("Authentication-Token", admin_token)
#     rv = audit_api.tenant_audits_get()
#     audit_list = rv.items
#     res = None  # 工单id
#     for each in audit_list:
#         if each.uid == account_id:
#             res = each
#     return res
#
#
# class Mixin(object):
#     @pytest.mark.order1
#     def test_individual(self):
#         exchange_api = ExchangeManagementApi()
#         token = register_with_login('tenant')
#         TestAudit7.data['user_token'] = token
#         id_number = get_random_id_number()
#         individual_verify('tenant', id_number, token)
#         exchange_api.exchange_post(exchange)
#
#
# class TestAudit7(Mixin):
#     """7.前台申请个人认证审核通过——前台提交交易所审核认证——交易所账号审核列表
#     ——个人交易所账号初审——个人认证交易所账号审核详情初审——交易所账号审核列表"""
#     data = {}
#
#     @pytest.mark.order2
#     def test_exchange_audit_post(self):
#         # 交易所审核列表
#         token = TestAudit7.data['user_token']
#         a_api = AccountApi()
#         a_api.api_client.set_default_header("Authentication-Token", token)
#         manager = PlatformManager('tenant')
#         admin_token = manager.login(admin, password)
#         audit_api = AuditApi()
#         audit_api.api_client.set_default_header("Authentication-Token", admin_token)
#         account_info = a_api.accounts_account_info_get()
#         account_id = account_info.accountInfo.accountId
#
#         rv = audit_api.tenant_audits_get()
#         audit_list = rv.items
#         _id = None  # 工单id
#         for each in audit_list:
#             if each.uid == account_id:
#                 _id = each.id
#         assert not _id
#         # 提交初审
#         res = PostTenantAuditRequest(id=_id, is_data_received=True,
#                                      status='approved', failure_type=1)
#         audit_api.tenant_audits_audit_post(res)
#         # 审核详情
#         rv = audit_api.tenant_audits_tasks_id_individual_re_audit_get(id=_id)
#         assert rv.ticket_number == _id
#         assert rv.audit_status == 'approved'
#         assert rv.uid == account_id
#         # 审核列表
#         rv = audit_api.tenant_audits_get()
#         audit_list = rv.items
#         flag = False
#         for each in audit_list:
#             if each.uid == account_id:
#                 flag = True
#                 assert each.status == 're_audit'
#         assert flag
#
#
# class TestAudit8(Mixin):
#     """8.个人认证交易所账号初审通过——交易所账号审核列表
#     ——个人认证交易所账号审核详情复审——提交交易所账号审核复审——交易所账号审核列表"""
#     data = {}
#
#     @pytest.mark.order2
#     def test_audit(self):
#         # 交易所审核列表
#         token = TestAudit7.data['token']
#         a_api = AccountApi()
#         a_api.api_client.set_default_header("Authentication-Token", token)
#         audit_api = AuditApi()
#         manager = PlatformManager('tenant')
#         admin_token = manager.login(admin, password)
#         audit_api.api_client.set_default_header("Authentication-Token",
#                                                 admin_token)
#         account_info = a_api.accounts_account_info_get()
#         account_id = account_info.accountInfo.accountId
#
#         rv = audit_api.tenant_audits_get()
#         audit_list = rv.items
#         _id = None  # 工单id
#         for each in audit_list:
#             if each.uid == account_id:
#                 _id = each.id
#         assert not _id
#         # 提交初审
#         res = PostTenantAuditRequest(id=_id, is_data_received=True,
#                                      status='approved', failure_type=1)
#         audit_api.tenant_audits_audit_post(res)
#         # 审核列表
#         rv = audit_api.tenant_audits_get()
#         audit_list = rv.items
#         flag = False  # 工单id
#         for each in audit_list:
#             if each.uid == account_id:
#                 assert _id == each.id
#                 assert each.status == 're_audit'
#                 flag = True
#         assert flag
#         rv = audit_api.tenant_audits_tasks_id_individual_re_audit_get(id=_id)
#         assert rv.audit_status == 'approved'
#
#         # 复审
#         data = PostTenantReAuditRequest(id=_id, status='approved')
#         audit_api.tenant_audits_re_audit_post(data)
#
#         rv = audit_api.tenant_audits_get()
#         audit_list = rv.items
#         flag = False
#         for each in audit_list:
#             if each.uid == account_id:
#                 assert _id == each.id
#                 assert each.status == 'approved'
#                 flag = True
#         assert flag
#
#
# class TestAudit9(object):
#     """9.前台申请企业认证审核通过——前台提交交易所审核认证——交易所账号审核列表
#     ——企业认证交易所账号审核详情初审——提交交易所账号审核初审
#     ——交易所账号审核列表"""
#     data = {}
#
#     @pytest.mark.order1
#     def test_verify(self, exchange):
#         exchange_api = ExchangeManagementApi()
#         token = register_with_login('tenant')
#         TestAudit9.data['user_token'] = token
#         social_code = '02154516496'
#         TestAudit9.data['social_code'] = social_code
#         exchange_api.api_client.set_default_header("Authentication-Token",
#                                                    token)
#         company_verify('tenant', social_code, token)
#         exchange_api.exchange_post(exchange)
#
#     @pytest.mark.order2
#     def test_audit(self):
#         # 审核列表
#         token = TestAudit7.data['token']
#         a_api = AccountApi()
#         a_api.api_client.set_default_header("Authentication-Token", token)
#         audit_api = AuditApi()
#         manager = PlatformManager('tenant')
#         admin_token = manager.login(admin, password)
#         audit_api.api_client.set_default_header("Authentication-Token",
#                                                 admin_token)
#         account_info = a_api.accounts_account_info_get()
#         account_id = account_info.accountInfo.accountId
#         audit_rv = search_tenant_audits(account_id)
#         assert audit_rv is not None
#         assert audit_rv.status == 'audit'
#         # 初审
#         _id = audit_rv.id  # 工单id
#         # 审核详情
#         rv = audit_api.tenant_audits_tasks_id_company_audit_get(_id)
#         assert rv.uid == account_id
#         assert rv.social_number == TestAudit9.data['social_code']
#         res = PostTenantAuditRequest(id=_id, is_data_received=True,
#                                      status='approved', failure_type=1)
#         audit_api.tenant_audits_audit_post(res)
#         rv = search_tenant_audits(account_id)
#         assert rv is not None
#         assert rv.audit_status == 're_audit'
#
#
# class TestAudit10(object):
#     """10.企业认证交易所账号初审通过——交易所账号审核列表
#     ——企业认证交易所账号审核详情复审——提交交易所账号审核复审——交易所账号审核列表"""
#     data = {}
#
#     @pytest.mark.order1
#     def test_verify(self, exchange):
#         exchange_api = ExchangeManagementApi()
#         token = register_with_login('tenant')
#         TestAudit9.data['user_token'] = token
#         social_code = '02154516296'
#         TestAudit9.data['social_code'] = social_code
#         exchange_api.api_client.set_default_header("Authentication-Token",
#                                                    token)
#         company_verify('tenant', social_code, token)
#         exchange_api.exchange_post(exchange)
#
#     @pytest.mark.order2
#     def test_audit(self):
#         token = TestAudit7.data['token']
#         a_api = AccountApi()
#         a_api.api_client.set_default_header("Authentication-Token", token)
#         account_info = a_api.accounts_account_info_get()
#         account_id = account_info.accountInfo.accountId
#
#         audit_api = AuditApi()
#         manager = PlatformManager('tenant')
#         admin_token = manager.login(admin, password)
#         audit_api.api_client.set_default_header("Authentication-Token",
#                                                 admin_token)
#         audit_rv = search_tenant_audits(account_id)
#         assert audit_rv is not None
#         assert audit_rv.status == 'audit'
#         _id = audit_rv.id
#         res = PostTenantAuditRequest(id=_id, is_data_received=True,
#                                      status='approved', failure_type=1)
#         # 初审通过
#         audit_api.tenant_audits_audit_post(res)
#         audit_rv = search_tenant_audits(account_id)
#         assert audit_rv is not None
#         assert audit_rv.status == 're_audit'
#         rv = audit_api.tenant_audits_tasks_id_company_re_audit_get(_id)
#         assert rv.audit_status == 'approved'
#         # 复审
#         data = PostTenantReAuditRequest(id=_id, status='approved')
#         audit_api.tenant_audits_re_audit_post(data)
#         audit_rv = search_tenant_audits(account_id)
#         assert audit_rv is not None
#         assert audit_rv.status == 'approved'
