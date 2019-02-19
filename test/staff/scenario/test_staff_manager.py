#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_staff_manager.py
@time: 2018/11/27
"""
from faker import Faker

from swagger_client.staff.api import staff_management_api
from swagger_client.staff.rest import ApiException
from common.account_sign import get_admin_token, ADMIN_ACCOUNT


class TestStaffManager:
    def test_no_login_create_staff(self):
        api = staff_management_api.StaffManagementApi()
        faker = Faker()
        account = faker.user_name()
        real_name = faker.name()
        phone = faker.phone_number()
        email = faker.email()
        try:
            api.staffs_post(body={
                              "account": account,
                              "realName": real_name,
                              "phoneNumber": phone,
                              "emailAddress": email}
                            )
        except ApiException as e:
            assert e.status == 403
        else:
            assert False, "未登录创建新职员, java接口异常"

    def test_normal_login_create_staff(self):
        api = staff_management_api.StaffManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        faker = Faker("zh-CN")
        account = faker.user_name()
        real_name = faker.name()
        phone = faker.phone_number()
        email = faker.email()
        api.staffs_post(body={
            "account": account,
            "realName": real_name,
            "phoneNumber": phone,
            "emailAddress": email}
        )
        # 重复创建职员
        try:
            api.staffs_post(body={
                "account": account,
                "realName": real_name,
                "phoneNumber": phone,
                "emailAddress": email}
            )
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, "重复创建职员, java接口异常"
        
        # 获取职员列表判断创建职员成功
        res = api.get_staff_list(page=1, email_address=email)
        assert res.meta.requested_page == 1
        assert res.meta.total_page == 1
        assert res.query.email_address == email
        assert not res.query.role_id
        staff = res.items.pop()
        assert staff.email_address == email
        assert staff.status
        assert staff.account == account
        assert staff.real_name == real_name
        assert staff.phone_number == phone
        staff_id = staff.id
        
        # 禁用不存在的职员
        try:
            api.staffs_put(body={"id": "50000", "status": False})
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "禁用不存在的账户时, java接口异常"
        
        # 禁用测试账户
        api.staffs_put(body={"id": staff_id, "status": False})
        res = api.get_staff_list(page=1, email_address=email)
        staff = res.items.pop()
        assert not staff.status
        
        # 启用测试账户
        api.staffs_put(body={"id": staff_id, "status": True})
        res = api.get_staff_list(page=1, email_address=email)
        staff = res.items.pop()
        assert staff.status
        
        # 重置不存在的职员密码
        try:
            api.staffs_id_reset_password_post(id="50000000")
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "重置不存在的职员密码, java接口异常"
            
        # 正常重置职员密码
        api.staffs_id_reset_password_post(id=staff_id)
        
        # 获取不存在的职员角色信息
        try:
            api.staffs_id_roles_get(id="500000")
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "获取不存在的职员角色信息时, java接口异常"
        # 正常获取职员角色信息
        role_resp = api.staffs_id_roles_get(id=staff_id)
        assert not role_resp
        
    def test_error_create_staff(self):
        """测试不填写电话和邮箱创建职员"""
        api = staff_management_api.StaffManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        faker = Faker()
        account = faker.user_name()
        real_name = faker.name()
        try:
            api.staffs_post(body={
                "account": account,
                "realName": real_name}
            )
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, "未填写电话和邮箱进行创建职员, java接口异常"
            
    def test_get_staff_info(self):
        api = staff_management_api.StaffManagementApi()
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        res = api.staffs_info_get()
        assert res.account == ADMIN_ACCOUNT
        assert isinstance(res.phone_number, str)
        assert isinstance(res.real_name, str)
        assert isinstance(res.id, str)
        assert isinstance(res.resource, list)
