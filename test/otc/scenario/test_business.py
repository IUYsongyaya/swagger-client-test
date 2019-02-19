# -*- coding: utf-8 -*-
# @File :  test_asset_buy_sell_record.py
# @Author : lh
import pytest
import random
import logging
from common.account_sign import get_admin_token, set_login_status
from swagger_client.otc.rest import ApiException
from swagger_client.staff import SystemManagementApi, PostFailureReasonRequest
from swagger_client.staff.rest import ApiException as OtcApiexception
from swagger_client.otc.api.bussiness_api import BussinessApi
from swagger_client.otc.api.account_api import AccountApi
from swagger_client.staff.api.bussiness_api import BussinessApi as StaffBussinessApi
from swagger_client.staff.models.audit_request import AuditRequest
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())


otc_buss_api = BussinessApi()
otc_ac_api = AccountApi()
staff_sys_api = SystemManagementApi()
staff_buss_api = StaffBussinessApi()


class TestBusiness:
    # 未设置实名认证，点击申请商家 -〉申请商家失败，提示未进行实名认证
    # 未绑定手机号，点击申请商家 -〉申请商家失败，提示未绑定手机号
    # 未设置昵称，点击申请商家 -》申请商家失败，提示未设置昵称
    # 未设置资金密码，点击申请商家 -〉申请商家失败，提示未设置资金密码
    # 商家保证金不足，点击申请商家 -〉申请商家失败，提示保证金不足
    # 企业实名认证通过，其它限制条件已满足，点击申请商家 -〉申请商家失败，提示企业用户无法申请
    #
    # 用户已满足申请商家限制条件，点击申请商家 -〉商家申请成功，在申请商家页面显示资料已提交，请等待审核结果
    # 申请商家审核不通过，查看审核结果-〉 点击商家审核，页面显示审核不同过与原因
    # 申请商家审核通过，查看审核结果 -〉 点击商家审核，页面显示审核通过与原因
    # @pytest.mark.parametrize('fail_type,code', [('not_real_name', 1),
    #                                             ('is_company', 2),
    #                                             ('not_bind_phone', 3),
    #                                             ('not_nick_name', 4),
    #                                             ('not_assert_pwd', 5),
    #                                             ('not_have_deposit', 7)])
    # def test_auth(self, fail_type, code, register_limit_user):
    #     register_limit_user([otc_buss_api], fail_type)
    #     try:
    #         res = otc_buss_api.biz_apply_post()
    #     except ApiException as e:
    #         assert res.code == 400

    def test_application_success(self, otc_business_user):
        """
        otc平台获取账户id,otc平台申请成为商家,后台管理获取申请列表,后台管理查看申请记录,后台管理审核申请
        """
        otc_business_user([otc_buss_api, otc_ac_api])
        return
        # 后台登录
        staff_token = get_admin_token()
        set_login_status(staff_buss_api, staff_token)
        set_login_status(staff_sys_api, staff_token)
        # ot平台获取账户id
        ac_info = otc_ac_api.accounts_account_info_get()
        assert ac_info
        ac_id = ac_info.account_info.account_id

        # otc平台申请成为商家
        otc_buss_api.biz_apply_post()
        biz_info = otc_buss_api.biz_info_get()
        assert biz_info.code == 1

        # otc平台查询押金信息
        otc_margin_res = otc_buss_api.biz_margin_info_get()
        logger.info(f'押金信息:{otc_margin_res}')

        # 后台管理获取申请列表
        application_rec = staff_buss_api.admin_biz_find_page_get(user_id=ac_id)
        order_num = application_rec.items[0].id
        logger.info(f'后台申请列表:{application_rec}')
        # 后台管理查看申请记录
        staff_biz_info = staff_buss_api.admin_biz_info_get(id=order_num)
        assert staff_biz_info.status == 1

        # 后台管理审核申请成功
        success_reaason = '您的信良好,继续保持'
        payload = AuditRequest(id=order_num, status=2, reason=success_reaason, file_recved=1)
        staff_buss_api.admin_biz_audit_post(payload)

        # 检查后台查看申请记录
        staff_app_list = staff_buss_api.admin_biz_find_page_get(user_id=ac_id)
        order_id = staff_app_list.items[0].id
        assert staff_app_list.items[0].status == 2

        # 后台管理查看申请记录
        staff_biz_info2 = staff_buss_api.admin_biz_info_get(id=order_id)
        assert staff_biz_info2.status == 2
        # 检查otc平台结果
        biz_res = otc_buss_api.biz_info_get()
        assert biz_res and biz_res.code == 2
        assert biz_res.reason == success_reaason

    def test_application_fail(self, otc_business_user):
        """
        otc平台获取账户id,otc平台申请成为商家,后台管理获取申请列表,后台管理查看申请记录,后台管理审核申请
        """
        otc_business_user([otc_buss_api, otc_ac_api])
        # 后台登录
        staff_token = get_admin_token()
        set_login_status(staff_buss_api, staff_token)
        set_login_status(staff_sys_api, staff_token)
        # ot平台获取账户id
        ac_info = otc_ac_api.accounts_account_info_get()
        assert ac_info
        ac_id = ac_info.account_info.account_id

        # otc平台申请成为商家
        otc_buss_api.biz_apply_post()
        biz_info = otc_buss_api.biz_info_get()
        assert biz_info.code == 1

        # 后台查询押金信息
        otc_margin_info = otc_buss_api.biz_margin_info_get()
        logger.info(f'后台押金信息:{otc_margin_info}')

        # 后台管理获取申请列表
        application_rec = staff_buss_api.admin_biz_find_page_get(user_id=ac_id)
        order_num = application_rec.items[0].id

        # 后台管理查看申请记录
        staff_biz_info = staff_buss_api.admin_biz_info_get(id=order_num)
        assert staff_biz_info.status == 1

        # 后台管理审核申请失败
        fail_reason_list = staff_sys_api.system_failure_reasons_get(type='OTC_SHOPKEEPER')
        logger.info(f'失败原因:{fail_reason_list}')
        if not fail_reason_list.items:
            payload = PostFailureReasonRequest()
            payload.type = 'OTC_SHOPKEEPER'
            payload.failure_reason = '您的信誉有待提升'
            staff_sys_api.system_failure_reasons_post(payload)
            fail_reason_list = staff_sys_api.system_failure_reasons_get(type='OTC_SHOPKEEPER')
            sys_reason_list = [i.failure_reason for i in fail_reason_list.items]
            fail_reason = random.choice(sys_reason_list)
        else:
            sys_reason_list = [i.failure_reason for i in fail_reason_list.items]
            fail_reason = random.choice(sys_reason_list)
        payload = AuditRequest(id=order_num, status=3, reason=fail_reason, file_recved=1)
        staff_buss_api.admin_biz_audit_post(payload)
        # 检查后台查看申请记录
        staff_app_list = staff_buss_api.admin_biz_find_page_get(user_id=ac_id)
        order_id = staff_app_list.items[0].id
        assert staff_app_list.items[0].status == 3

        # 后台管理查看申请记录
        staff_biz_info2 = staff_buss_api.admin_biz_info_get(id=order_id)
        assert staff_biz_info2.status == 3
        # 检查otc平台结果
        biz_res = otc_buss_api.biz_info_get()
        assert biz_res and biz_res.code == 3
        assert biz_res.reason == fail_reason
