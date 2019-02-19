# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-13


#
# staff = Staff(mocking=True)
# tenant = Tenant(mocking=True)
# venture = Venture(mocking=True)
#
#
# @pytest.fixture("session")
# def sponsor_testing():
#     sponsor_name_list = []
#     pages = Pager(staff.api_sponsors_management.staff_sponsors_get())
#
#     for page in pages:
#         if len(page.items):
#             sponsor_name_list.extend([item.name for item in page.items])
#     if TEST_SPONSOR["name"] not in sponsor_name_list:
#
#         req = PostSponsorRequest(**TEST_SPONSOR)
#         staff.api_sponsors_management.staff_sponsors_post(req)
#     return DictObject(**TEST_SPONSOR)
#
#
# @pytest.fixture("session")
# def sponsor_testing():
#     sponsor_name_list = []
#     pages = Pager(staff.api_sponsors_management.staff_sponsors_get())
#
#     for page in pages:
#         if len(page.items):
#             sponsor_name_list.extend([item.name for item in page.items])
#     if TEST_SPONSOR["name"] not in sponsor_name_list:
#         req = PostSponsorRequest(**TEST_SPONSOR)
#         staff.api_sponsors_management.staff_sponsors_post(req)
#     return DictObject(**TEST_SPONSOR)
#
#
# @pytest.fixture("session")
# def exchange_testing():
#     exchange_exists = False
#     exchange_id = DictObject(**dict(
#         id=""
#     ))
#     try:
#         rsp = tenant.api_exchange_management.exchange_exchange_id_get()
#         exchange_id.id = rsp.id
#     except ApiException as ae:
#         assert ae.status == 404
#     else:
#         assert rsp.status == "approved"
#         exchange_exists = True
#
#     if not exchange_exists:
#         tenant.api_exchange_management.exchange_post(**TEST_EXCHANGE)
#         # 初审
#         rv = staff.api_audit.tenant_audits_get()
#         audit_list = rv.items
#         _id = None
#         for each in audit_list:
#             if each['uid'] == tenant.account:
#                 _id = each['id']  # 工单id
#         assert not _id
#         res = PostTenantAuditRequest(
#             id=_id,
#             is_data_received=True,
#             status='approved',
#             failure_type=1)
#         staff.api_audit.tenant_audits_audit_post(res)
#         # 复审
#         req = PostTenantReAuditRequest(
#             id=_id,
#             status='approved',
#             failure_type=None)
#         staff.api_audit.tenant_audits_re_audit_post(body=req)
#         rv = tenant.api_exchange_management.exchange_exchange_status_get()
#         assert rv.status == 'approved'
#         rsp = tenant.api_exchange_management.exchange_exchange_id_get()
#         exchange_id.id = rsp.id
#
#     exchange_ret = dict.copy(TEST_EXCHANGE)
#     exchange_ret.update(
#         dict(
#             id=exchange_id.id
#         )
#     )
#
#     return DictObject(**exchange_ret)
#
#
# def get_project_id_by_name(name):
#     pages = Pager(tenant.api_project.projects_get)
#     for page in pages:
#         id = [item.id for item in page.items if item.project_name == name]
#         if id:
#             return id
#     return []
#
#
# @pytest.fixture("session")
# def project_testing():
#     project_id = get_project_id_by_name(TEST_PROJECT["name"])
#     if not project_id:
#         req = ApplicationRequest(**TEST_PROJECT)
#         apid = venture.api_project.applications_post(body=req)
#         # 初审
#         rv = staff.api_audit.tenant_audits_get()
#         audit_list = rv.items
#         _id = None
#         for each in audit_list:
#             if each['uid'] == venture.account:
#                 _id = each['id']  # 工单id
#         assert not _id
#         res = PostTenantAuditRequest(
#             id=_id,
#             is_data_received=True,
#             status='approved',
#             failure_type=1)
#         staff.api_audit.tenant_audits_audit_post(res)
#         # 复审
#         req = PostTenantReAuditRequest(
#             id=_id,
#             status='approved',
#             failure_type=None)
#         staff.api_audit.tenant_audits_re_audit_post(body=req)
#
#         rv = venture.api_project.applications_id_get(id=apid)
#         assert rv.status == 'done'
#         project_id.extend(get_project_id_by_name(TEST_PROJECT["name"]))
#
#     project_ret = dict.copy(TEST_PROJECT)
#     project_ret.update(
#         dict(
#             id=project_id[0]
#         )
#     )
#     return DictObject(**project_ret)
#
#
