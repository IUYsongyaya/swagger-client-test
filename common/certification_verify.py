#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: certification_verify.py
@time: 2018/11/11
"""
from swagger_client.staff.api.audit_api import AuditApi
from swagger_client.staff.models.post_individual_audit_request \
    import PostIndividualAuditRequest
from swagger_client.staff.models.post_company_audit_request\
    import PostCompanyAuditRequest
from common.utils import PlatformManager, get_random_name
from common.account_sign import get_admin_token


def individual_verify(platform: str, id_number: str, token,
                      verify_status: str="ACCEPTED", reject_type: str=str()):
    """
    申请个人实名审核以及通过通过指定证件id下的所有待审核的认证(供其他人调用)
    :param reject_type: 失败类型 [ INDIVIDUAL_ID,
                                 INDIVIDUAL_PASSPORT, ENTERPRISE_LOGO,
                                 ENTERPRISE_LICENSE, INDIVIDUAL_ABNORMAL,
                                 ENTERPRISE_ABNORMAL, USER_REPORT_ABNORMAL ]
    :param verify_status: 验证状态approved（通过）、disapproved（未通过）
    :param token: 用户登录token
    :param platform: 平台类型 Enum("main", "sponsor", "staff",
                                    "tenant", "venture")
    :param id_number: 证件号码
    """
    manager = PlatformManager(platform)
    manager.apply_individual_verify(id_number, token)
    admin_token = get_admin_token()
    audit_api = AuditApi()
    audit_api.api_client.set_default_header("Authorization",
                                            "Bearer " + admin_token)
    apply_list = get_individual_apply_list(audit_api, id_number)
    for apply_id in apply_list:
        handle_individual_apply(audit_api, apply_id, verify_status,
                                reject_type)
        

def company_verify(platform: str, social_number: str, token,
                   verify_status: str="ACCEPTED", reject_type: str=str()):
    """
    申请公司实名审核以及通过通过指定社会统一编号下的所有待审核的认证(供其他人调用)
    :param reject_type: 失败类型 [ INDIVIDUAL_ID,
                                 INDIVIDUAL_PASSPORT, ENTERPRISE_LOGO,
                                 ENTERPRISE_LICENSE, INDIVIDUAL_ABNORMAL,
                                 ENTERPRISE_ABNORMAL, USER_REPORT_ABNORMAL ]
    :param verify_status: 验证状态ACCEPTED（通过）、REJECTED（未通过）
    :param platform:平台类型 Enum("main", "sponsor", "staff",
                                    "tenant", "venture")
    :param social_number: 社会统一编号
    :param token: 用户登录token
    """
    manager = PlatformManager(platform)
    manager.apply_company_verify(social_number, token)
    admin_token = get_admin_token()
    audit_api = AuditApi()
    audit_api.api_client.set_default_header("Authorization",
                                            "Bearer " + admin_token)
    rv = audit_api.accounts_company_audits_tasks_audit_num_get()
    assert rv.pending_num >= 1
    apply_list = get_company_apply_list(audit_api, social_number)
    for apply_id in apply_list:
        handle_company_apply(audit_api, apply_id, verify_status, reject_type)


def get_individual_apply_list(audit_api: AuditApi, id_number: str)-> list:
    """
    获取制定证件号下所有待审核的id
    :param audit_api: audit_api实例化对象
    :param id_number: 证件号
    :return:
    """
    resp = audit_api.accounts_individual_audits_get(id_number=id_number,
                                                    status="APPLIED")
    return [item.id for item in resp.items]


def handle_individual_apply(audit_api: AuditApi, apply_id: str,
                            verify_status: str, reject_type: str=str()):
    """
    通过指定申请id的个人认证
    :param reject_type: 失败类型 [ INDIVIDUAL_ID,
                                 INDIVIDUAL_PASSPORT, ENTERPRISE_LOGO,
                                 ENTERPRISE_LICENSE, INDIVIDUAL_ABNORMAL,
                                 ENTERPRISE_ABNORMAL, USER_REPORT_ABNORMAL ]
    :param verify_status: 验证状态ACCEPTED（通过）、REJECTED（未通过）
    :param audit_api:
    :param apply_id:
    """
    if reject_type:
        post_info = PostIndividualAuditRequest(id=apply_id,
                                               status=verify_status,
                                               reject_type=reject_type,
                                               rejected_reason="reason")
    else:
        post_info = PostIndividualAuditRequest(id=apply_id,
                                               status=verify_status)
    audit_api.accounts_individual_audits_post(post_info)


def get_company_apply_list(audit_api: AuditApi, social_code: str)-> list:
    """
    获取指定公司的待审核的实名认证列表
    :param audit_api: 借口实例化对象
    :param social_code: 社会统一编号
    :return:
    """
    resp = audit_api.accounts_company_audits_get(social_number=social_code,
                                                 status="APPLIED")
    return [item.id for item in resp.items]


def handle_company_apply(audit_api: AuditApi, apply_id: str,
                         verify_status: str, reject_type: str=str()):
    if reject_type:
        post_info = PostCompanyAuditRequest(id=apply_id,
                                            status=verify_status,
                                            reject_type=reject_type,
                                            reject_reason="reason")
    else:
        post_info = PostCompanyAuditRequest(id=apply_id,
                                            status=verify_status)
    audit_api.accounts_company_audits_post(body=post_info)
