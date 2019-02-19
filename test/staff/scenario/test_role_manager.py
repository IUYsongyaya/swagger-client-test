#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_role_manager.py
@time: 2018/11/27
"""
import random

from faker import Faker

from swagger_client.staff.api import (security_management_api,
                                      staff_management_api)
from swagger_client.staff.rest import ApiException
from common.account_sign import get_admin_token
from common.utils import get_random_name


class TestRoleManager:
    def test_create_role(self):
        api = security_management_api.SecurityManagementApi()
        faker = Faker()
        # 未登录创建角色
        role_name = faker.name()
        try:
            api.roles_post(body={"name": role_name,
                                 "description": "this is description of role"}
                           )
        except ApiException as e:
            assert e.status == 403
        else:
            assert False, "未登录时创建角色时, java接口异常"
            
        # 正常创建角色
        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        resp = api.roles_post(
            body={"name": role_name,
                  "description": "this is description of role"}
        )
        assert resp.role_id
        assert isinstance(resp.role_id, str)
        
        # 重复创建角色
        try:
            api.roles_post(body={"name": role_name,
                                 "description": "this is description of role"}
                           )
        except ApiException as e:
            assert e.status == 409
        else:
            assert False, "重复创建角色时, java接口异常"

    def test_delete_role(self):
        api = security_management_api.SecurityManagementApi()
        # 未登录时,删除角色
        try:
            api.roles_id_delete(id="500000")
        except ApiException as e:
            assert e.status == 403
        else:
            assert False, "未登录时删除角色, java接口异常"

        admin_token = get_admin_token()
        api.api_client.set_default_header("Authorization",
                                          "Bearer " + admin_token)
        # 删除不存在的角色
        try:
            api.roles_id_delete(id="500000")
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "删除不存在的角色, java接口异常"
            
        # 正常创建删除角色
        faker = Faker()
        role_name = faker.name()
        resp = api.roles_post(
            body={"name": role_name,
                  "description": "this is description of role"}
        )
        role_id = resp.role_id
        api.roles_id_delete(id=role_id)
        # 通过获取角色信息来判断是否删除
        try:
            api.roles_id_get(id=role_id)
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "删除角色后还可以获取该角色详情"
        
        # 重复删除
        try:
            api.roles_id_delete(id=role_id)
        except ApiException as e:
            assert e.status == 404
        else:
            assert "删除已删除的角色时, java接口异常"

    def test_set_role_for_staff(self):
        staff_api = staff_management_api.StaffManagementApi()
        admin_token = get_admin_token()
        staff_api.api_client.set_default_header("Authorization",
                                                "Bearer " + admin_token)
        faker = Faker('zh_CN')
        account = get_random_name(2, 25)
        real_name = get_random_name(2, 16)
        phone = faker.phone_number()
        email = faker.email()
        # 正常创建一个职员
        staff_api.staffs_post(body={
            "account": account,
            "realName": real_name,
            "phoneNumber": phone,
            "emailAddress": email})
        res = staff_api.get_staff_list(page=1, email_address=email)
        staff = res.items.pop()
        staff_id = staff.id
        
        # 分配个该职员不存在的角色
        try:
            staff_api.staffs_set_role_post(body={"staffId": staff_id,
                                                 "ids": ["999999"]})
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, "分配给给职员不存在的角色, java接口异常"
            
        # 正常创建一个角色
        role_api = security_management_api.SecurityManagementApi()
        role_api.api_client.set_default_header("Authorization",
                                               "Bearer " + admin_token)
        role_name = faker.name()
        role_description = "this is description of role"
        resp = role_api.roles_post(
            body={"name": role_name,
                  "description": role_description}
        )
        role_id = resp.role_id
        
        # 查看不存在角色下的职员信息
        try:
            role_api.roles_get_staffs_get(role_id="999999", page=1)
        except ApiException as e:
            assert e.status == 404

        # 移除该角色下未绑定的职员
        try:
            role_api.roles_remove_staff_post(
                role_remove_staff={"roleId": role_id,
                                   "staffId": staff_id})
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "移除角色下未绑定的职员, java接口异常"
        
        # 正常将角色分配给职员
        staff_api.staffs_set_role_post(body={"staffId": staff_id,
                                             "ids": [role_id]})
        
        # 查看该角色下的职员信息
        res = role_api.roles_get_staffs_get(role_id=role_id, page=1)
        assert res.meta.total_page == 1
        assert len(res.items) == 1
        item = res.items.pop()
        assert item.id == staff_id
        assert item.phone_number == phone
        assert item.email_address == email
        assert item.account == account
        assert item.real_name == real_name
        assert item.status
        assert len(item.roles) == 1
        role_item = item.roles.pop()
        assert role_item.role_id == role_id
        assert role_item.role_name == role_name

        # 获取职员的角色信息
        res = staff_api.staffs_id_roles_get(id=staff_id)
        assert len(res) == 1
        item = res.pop()
        assert item["id"] == role_id
        assert item["name"] == role_name
        assert item["description"] == role_description
        
        # 移除该角色下不存在的职员
        try:
            role_api.roles_remove_staff_post(
                role_remove_staff={"roleId": role_id,
                                   "staffId": "999999"})
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "移除角色下不存在的职员, java接口异常"
            
        # 移除不存在的角色下的职员
        try:
            role_api.roles_remove_staff_post(
                role_remove_staff={"roleId": "9999999",
                                   "staffId": staff_id})
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "移除不存在的角色下的职员, java接口异常"

        # 正常移除角色下职员
        role_api.roles_remove_staff_post(
            role_remove_staff={"roleId": role_id,
                               "staffId": staff_id})

        # 查看该角色下的职员信息
        res = role_api.roles_get_staffs_get(role_id=role_id, page=1)
        assert res.meta.total_page == 0
        assert not len(res.items)

        # 获取职员的角色信息
        res = staff_api.staffs_id_roles_get(id=staff_id)
        assert not len(res)
        
    def test_set_staff_for_role(self):
        staff_api = staff_management_api.StaffManagementApi()
        admin_token = get_admin_token()
        staff_api.api_client.set_default_header("Authorization",
                                                "Bearer " + admin_token)
        faker = Faker('zh_CN')
        account = get_random_name(2, 25)
        real_name = get_random_name(2, 16)
        phone = faker.phone_number()
        email = faker.email()
        # 正常创建一个职员
        staff_api.staffs_post(body={
            "account": account,
            "realName": real_name,
            "phoneNumber": phone,
            "emailAddress": email})
        res = staff_api.get_staff_list(page=1, email_address=email)
        staff = res.items.pop()
        staff_id = staff.id
    
        # 正常创建一个角色
        role_api = security_management_api.SecurityManagementApi()
        role_api.api_client.set_default_header("Authorization",
                                               "Bearer " + admin_token)
        role_name = faker.name()
        role_description = "this is description of role"
        resp = role_api.roles_post(
            body={"name": role_name,
                  "description": role_description}
        )
        role_id = resp.role_id
        
        # 获取角色列表(无分页)
        res = role_api.roles_list_get()
        for i in res:
            if i["id"] == role_id:
                break
        else:
            assert False

        # 正常将职员分配给角色
        role_api.roles_set_staff_post(role_assignment_staff={"roleId": role_id,
                                                             "ids": [staff_id]})
    
        # 查看该角色下的职员信息
        res = role_api.roles_get_staffs_get(role_id=role_id, page=1)
        assert res.meta.total_page == 1
        assert len(res.items) == 1
        item = res.items.pop()
        assert item.id == staff_id
        assert item.phone_number == phone
        assert item.email_address == email
        assert item.account == account
        assert item.real_name == real_name
        assert item.status
        assert len(item.roles) == 1
        role_item = item.roles.pop()
        assert role_item.role_id == role_id
        assert role_item.role_name == role_name
    
        # 获取职员的角色信息
        res = staff_api.staffs_id_roles_get(id=staff_id)
        assert len(res) == 1
        item = res.pop()
        assert item["id"] == role_id
        assert item["name"] == role_name
        assert item["description"] == role_description
        
    def test_manager_permission(self):
        role_api = security_management_api.SecurityManagementApi()
        admin_token = get_admin_token()
        role_api.api_client.set_default_header("Authorization",
                                               "Bearer " + admin_token)
        # 获取权限列表
        res = role_api.permission_get()
        assert len(res)
        for i in res:
            assert i["id"]
            assert i["title"]
        
        # 创建角色
        faker = Faker()
        role_api = security_management_api.SecurityManagementApi()
        role_api.api_client.set_default_header("Authorization",
                                               "Bearer " + admin_token)
        role_name = faker.name()
        role_description = "this is description of role"
        resp = role_api.roles_post(
            body={"name": role_name,
                  "description": role_description}
        )
        role_id = resp.role_id
        
        # 分配给角色不存在的权限
        try:
            role_api.roles_set_permissions_post(
                body={"roleId": role_id,
                      "description": "this is description",
                      "ids": ["999999"]})
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, "分配给角色不存在的权限, java接口异常"
            
        random_permission = random.choice(res)
        # 分配给不存在的角色权限
        try:
            role_api.roles_set_permissions_post(
                body={"roleId": "9999999",
                      "description": "this is description",
                      "ids": [random_permission["id"]]}
            )
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "分配给不存在的角色权限, java接口异常"
        
        # 正常给角色分配权限
        random_permission_list = [i["id"] for i in random.choices(res, k=3)]
        role_api.roles_set_permissions_post(
            body={"roleId": role_id,
                  "description": "this is description",
                  "ids": random_permission_list}
        )
        
        # 获取不存在角色的所有权限
        try:
            role_api.roles_id_permissions_get(id="9999999")
        except ApiException as e:
            assert e.status == 404
        else:
            assert False, "获取不存在的角色权限时, java接口异常"
            
        # 正常获取角色权限
        role_permission = role_api.roles_id_permissions_get(id=role_id)
        assert len(role_permission.ids) == len(random_permission_list)
        for i in role_permission.ids:
            if i not in random_permission_list:
                assert False, "角色有未分配的权限, java接口异常"
