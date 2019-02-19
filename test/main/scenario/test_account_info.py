#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_account_info.py
@time: 2018/11/19
"""
from datetime import datetime

from faker import Faker
import pytest

from common.account_sign import register_with_login
from common.utils import PlatformManager, get_random_id_number, \
    random_get_country_ob, get_random_name
from common.certification_verify import individual_verify, company_verify


class TestAccountInfo:
    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_sample_get_account_info(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        user = register_with_login(platform, with_login, [account_api])
        email = user.get("email")
        country = user.get("country_abbreviation")
        password = user.get("password")
        res = account_api.accounts_account_info_get()
        print(res)
        assert isinstance(res.account_info.account_id, str)
        assert res.account_info.email == email
        assert res.account_info.nationality_code == country
        # assert isinstance(res.account_info.venture_id, str)
        # assert isinstance(res.account_info.tenant_id, str)
        # assert isinstance(res.account_info.investor_id, str)
        assert not res.account_info.phone_number
        assert isinstance(res.account_info.created_at, datetime)
        # assert res.security_verification.login_password == password
        # assert res.security_verification.tra_password == "false"
        assert not res.account_info.google_authenticator
        assert res.certification_audit.certification_status == "none"
        assert not res.certification_audit.certification_type
        assert not res.certification_audit.rejected_type
        assert not res.certification_audit.rejected_reason
        assert not res.certification_audit.application_date
        assert not res.certification_audit.certificat_name

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_get_account_info(self, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        try:
            account_api.accounts_account_info_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录时获取账户信息, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_get_no_exit_account_company(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        register_with_login(platform, with_login, [account_api])
        try:
            account_api.accounts_company_get()
        except manager.api_exception as e:
            assert e.status == 404
        else:
            assert False, "账号不存在企业申请时获取企业信息,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_get_normal_account_company(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        user = register_with_login(platform, with_login, [account_api])
        social_number = get_random_id_number()
        company_verify(platform, social_number=social_number,
                       token=user["token"])
        res = account_api.accounts_company_get()
        assert res.social_code[:2] == social_number[:2]
        assert res.social_code[-2:] == social_number[-2:]

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_get_account_company(self, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        try:
            account_api.accounts_company_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "账号未登录时获取企业信息,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_get_normal_individual_info(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        user = register_with_login(platform, with_login, [account_api])
        id_number = get_random_id_number()
        individual_verify(platform, id_number, token=user["token"])
        res = account_api.accounts_individual_get()
        assert res.number[:2] == id_number[:2]
        assert res.number[-2:] == id_number[-2:]

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_exit_get_individual_info(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        register_with_login(platform, with_login, [account_api])
        try:
            account_api.accounts_individual_get()
        except manager.api_exception as e:
            assert e.status == 404
        else:
            assert False, "账号不存在个人认证申请时获取个人认证信息,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_get_individual_info(self, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        try:
            account_api.accounts_individual_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "账号未登录时获取个人认证信息,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_login_history(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        register_with_login(platform, with_login, [account_api])
        res = account_api.accounts_get_login_history_get()
        assert len(res.items) > 0
        item = res.items.pop()
        assert isinstance(item.id, str)
        assert isinstance(item.login_at, str)
        assert isinstance(item.location, str)
        assert isinstance(item.ip, str)
        assert isinstance(item.equipment_type, str)
        assert isinstance(item.access_side, str)
        assert res.meta.requested_page == 1
        assert res.meta.page == 1
        res = account_api.accounts_get_login_history_get(page=2)
        assert len(res.items) == 0

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_history(self, platform):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        try:
            account_api.accounts_get_login_history_get()
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录时获取登录历史, java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_apply_individual(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        user = register_with_login(platform, with_login, [account_api])
        id_number = get_random_id_number()
        individual_info = manager.apply_individual_verify(id_number)
        res = account_api.accounts_individual_get()
        assert res.name == individual_info["name"]
        assert res.nationality_code == user["country_abbreviation"]
        assert res.type == "ID"
        assert res.number[:2] == id_number[:2]
        assert res.number[-2:] == id_number[-2:]
        account_info = account_api.accounts_account_info_get()
        status = account_info.certification_audit.certification_status
        assert status == "applied"
        type_ = account_info.certification_audit.certification_type
        assert type_ == "individual"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_apply_individual(self, platform):
        manager = PlatformManager(platform)
        id_number = get_random_id_number()
        try:
            manager.apply_individual_verify(id_number)
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录申请个人实名认证时java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_normal_apply_company(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        register_with_login(platform, with_login, [account_api])
        id_number = get_random_id_number()
        company_info = manager.apply_company_verify(id_number)
        res = account_api.accounts_company_get()
        assert res.name[:1] == company_info["name"][:1]
        assert res.name[-1:] == company_info["name"][-1:]
        assert res.company_name == company_info["company_name"]
        assert res.phone_number[:3] == company_info["phone"][:3]
        assert res.phone_number[-4:] == company_info["phone"][-4:]
        assert res.social_code[:2] == id_number[:2]
        assert res.social_code[-2:] == id_number[-2:]
        account_info = account_api.accounts_account_info_get()
        status = account_info.certification_audit.certification_status
        assert status == "applied"
        type_ = account_info.certification_audit.certification_type
        assert type_ == "company"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_no_login_apply_company(self, platform):
        manager = PlatformManager(platform)
        id_number = get_random_id_number()
        try:
            manager.apply_company_verify(id_number)
        except manager.api_exception as e:
            assert e.status == 403
        else:
            assert False, "未登录申请公司实名认证时java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_error_field_apply_individual(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        register_with_login(platform, with_login, [account_api])
        try:
            # manager.apply_individual_verify(123456)
            country = random_get_country_ob()["k"]
            account_api.request_individual_certification(
                body={"nationalityCode": country,
                      "name": get_random_name(2, 20),
                      "type": "identityCard",
                      "number": 123456,
                      "frontPhoto": "front_phone",
                      "backPhoto": "back_photo",
                      "handheldPhoto": "handheld_photo"})
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "填写错误类型字段进行个人实名认证,java接口异常"

    @pytest.mark.parametrize("platform", ["main", "tenant", "venture"])
    def test_error_field_apply_company(self, platform, with_login):
        manager = PlatformManager(platform)
        account_api = manager.account_api
        register_with_login(platform, with_login, [account_api])
        try:
            nationality_code = "nationality_code"
            faker = Faker("zh_CN")
            account_api.request_enterprise_certification(
                body={"companyName": get_random_name(2, 50),
                      "nationalityCode": nationality_code,
                      "area": "公司所在区域",
                      "address": faker.address(),
                      "logo": "logo",
                      "socialCode": 123,
                      "name": get_random_name(2, 20),
                      "phoneNumber": faker.phone_number(),
                      "taxNumber": "tax_code",
                      "organizationCode": "organization_code",
                      "businessLicense": "business_license"})
        except manager.api_exception as e:
            assert e.status == 400
        else:
            assert False, "填写错误类型字段进行公司实名认证,java接口异常"
