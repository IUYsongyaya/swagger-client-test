# -*- coding: utf-8 -*-
# @File :  test_invite_rank.py
# @Author : lh
# @time : 18-11-13 下午5:55
from faker import Faker
import pytest
from common.utils import PlatformManager, random_get_country_ob
from common.account_sign import rand_email, rand_password, register_with_login, \
    set_login_status, get_admin_token
from swagger_client.main import InviteApi, AccountApi
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
        user1 = register_with_login(platform, with_login, [main_ac_api, main_invite_api])
        # 绑定登录user1与api
        # 获取主平台登录账户account_id,邀请码
        user1_acinfo_res = main_ac_api.accounts_account_info_get()
        invite_code = user1_acinfo_res.account_info.promotion_code
        user1_account_id = user1_acinfo_res.account_info.account_id
        print('user1账户id:', user1_account_id)
        user1_account_mail = user1_acinfo_res.account_info.email
        # user2用user1的邀请码注册账号,登录成功
        manager = PlatformManager(platform)
        user2_ran_email = rand_email()
        print('user2邮箱:', user2_ran_email)
        ran_password = rand_password()
        ran_country = random_get_country_ob()["k"]
        print(invite_code)
        manager.register(email=user2_ran_email, password=ran_password, promotion_code=invite_code,
                         nationality_code=ran_country, nick_name=faker.name())
        user2_token = manager.login(user2_ran_email, ran_password)
        # assert user2_token
        # 查看主平台user1邀请信息
        set_login_status(main_ac_api, user1['token'])
        set_login_status(main_invite_api, user1['token'])
        main_user1_inviteres = main_ac_api.accounts_invites_get()
        print('user1邀请信息:', main_user1_inviteres)
        # 绑定主平台user2与api
        set_login_status(main_ac_api, user2_token)
        set_login_status(main_invite_api, user2_token)
        user2_acinfo_res = main_ac_api.accounts_account_info_get()
        user2_account_id = user2_acinfo_res.account_info.account_id
        print('user2账户id:', user2_account_id)
        main_user1_invitelist = [i.account_id for i in main_user1_inviteres.items]
        assert user2_account_id in main_user1_invitelist
        # 后台查看邀请记录信息
        user2_invite_res = staff_acmanager_api.accounts_id_inviter_get(id=user2_account_id)
        user2_invitor = user2_invite_res.inviter
        assert user2_invitor == user1_account_mail
        # 后台查看邀请好友列表
        user1_invite_res = staff_acmanager_api.accounts_id_invitees_get(id=user1_account_id)
        user1_invite_list = [i.account_id for i in user1_invite_res.items]
        assert user2_account_id in user1_invite_list
        # 查看邀请奖励记录
        reward_record_res = main_invite_api.invites_reward_list_get(account_id=user1_account_id)
        print('邀请奖励:', reward_record_res)
        assert reward_record_res.items == []
        # 主平台查看邀请排行榜
        record_list = main_invite_api.invites_ranking_list_get()
        print('排行榜list:', record_list)
        assert record_list
