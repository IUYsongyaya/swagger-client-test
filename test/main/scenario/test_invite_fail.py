# -*- coding: utf-8 -*-
# @File :  test_invite_fail.py
# @Author : lh
# @time : 18-11-12 下午3:49
from faker import Faker
import pytest
from common.utils import PlatformManager, random_get_country_ob
from common.account_sign import rand_email, rand_password, register_with_login, \
    set_login_status, get_admin_token
from swagger_client.main import InviteApi, AccountApi
from swagger_client.main.rest import ApiException
from swagger_client.staff.api import AccountManagementApi

staff_acmanager_api = AccountManagementApi()
main_invite_api = InviteApi()
main_ac_api = AccountApi()
faker = Faker("zh_CN")


class TestInviteFail:
    @pytest.mark.parametrize("platform", ["main"])
    def test_invite_success(self, platform, with_login):
        # 验证主平台,后台登录状态
        staff_token = get_admin_token()
        set_login_status(staff_acmanager_api, staff_token)
        register_with_login(platform, with_login, [main_ac_api, main_invite_api])
        # 绑定登录user1与api
        # 获取主平台登录账户account_id,邀请码
        user1_acinfo_res = main_ac_api.accounts_account_info_get()
        user1_account_id = user1_acinfo_res.account_info.account_id
        print('user1账户id:', user1_account_id)
        # user2用user1的邀请码注册账号,登录成功
        manager = PlatformManager(platform)
        user2_ran_email = rand_email()
        print('user2邮箱:', user2_ran_email)
        ran_password = rand_password()
        ran_country = random_get_country_ob()["k"]
        try:
            manager.register(email=user2_ran_email, password=ran_password, promotion_code='321564',
                             nationality_code=ran_country, nick_name=faker.name())
        except ApiException as e:
            assert e.status == 400
