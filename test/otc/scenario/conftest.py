# @author: lj lh
import json
import random
import pytest
import requests

from faker import Faker
from common.account_sign import random_user, set_login_status, get_admin_token
from swagger_client.staff.models import AuditRequest
from swagger_client.staff.api import BussinessApi as StaffBuss, BalanceApi as StaffBalance
from swagger_client.staff.api import SystemManagementApi
from swagger_client.otc.api import AccountApi, AssetManagementApi, BussinessApi, BalanceApi
from swagger_client.otc.models import TransferFromRequest
from swagger_client.staff.rest import ApiException as OtcApiexception
from common.certification_verify import individual_verify
from swagger_client.main.configuration import Configuration
from swagger_client.staff.configuration import Configuration as StaffConfiguration
from common.account_sign import register_with_login
from common.utils import PlatformManager, get_random_id_number

otc_asset_api = AssetManagementApi()
otc_buss_api = BussinessApi()
otc_balance_api = BalanceApi()
staff_buss_api = StaffBuss()
staff_bal_api = StaffBalance()
otc_ac_api = AccountApi()
staff_sys_api = SystemManagementApi()

configuration = Configuration()
staff_configuration = StaffConfiguration()
TURN_ON = 1
TURN_OFF = 0
DEFAULT_VERIFY_CODE = "666666"


def verify_info(manager, account, verify_type):
    verify_ = {
        "challenge": "",
        "seccode": "",
        "validate": "",
        "account": "mailto:" + account,
        "code": DEFAULT_VERIFY_CODE,
        "type": verify_type
    }
    if verify_type in ["alter_phone", "alter_google"]:
        verify_.update({"secondCode": DEFAULT_VERIFY_CODE})
    return manager.verify(verify_)


@pytest.fixture(scope="function")
def otc_user(with_login):
    def create_all_done_account(api_list, platform='otc'):
        # 注册
        # 登录
        manager = PlatformManager(platform)
        account_api = manager.account_api
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [
            account_api, otc_balance_api, asset_api, verify_api, otc_buss_api,
            otc_asset_api
        ] + api_list)
        email = user.get("email")
        # 实名认证
        id_number = get_random_id_number()
        individual_verify(platform, id_number, user.get('token'))
        # 绑定手机号码
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(
            phone, DEFAULT_VERIFY_CODE, area_code="+86", token=verify.token)
        # 随机资金密码
        assert_password = faker.password()
        # print(user)
        # 设置资金密码，
        # 需要二次验证才能设置资金密码
        res = verify_info(manager, email, 'edit_asset_pwd')
        base_token = res.token
        asset_api.asset_mgmt_asset_password_put(
            body={
                "password": user.get("password"),
                "traPassword": assert_password,
                "baseToken": base_token
            })
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set
        user_res_info = dict()
        user_res_info['asset_password'] = assert_password
        # 查询otc交易支持的币种列表
        otc_coin_list = otc_balance_api.balance_otc_coin_list_get()
        # print('otc交易支持的币种列表:', otc_coin_list)
        seller_coins = []
        for i in otc_coin_list.items:
            i = i.to_dict()
            if i['short_name'] == 'USDT':
                usdt_coin_id = i['coin_id']
            else:
                seller_coins.append(i['coin_id'])
        coin_id = random.choice(seller_coins or [usdt_coin_id + 1])  # random_coin.coin_id

        # 充币金手指
        headers = {"Authorization": "Bearer {}".format(user.get('token'))}
        host = configuration.host
        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        user_res_info['account_id'] = account_id

        res = requests.post(
            f'{host}/asset-test/asset-initialize/{coin_id}/100000000',
            headers=headers)
        # print(res)
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{usdt_coin_id}/100000000',
            headers=headers)
        # print(coin_id)
        # print(usdt_coin_id)
        bb_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        # print('币币余额:', bb_res2)
        # 认证商户
        # 后台登录
        user_token = get_admin_token()
        user_res_info['admin_token'] = user_token
        user_res_info['buyer_coin_id'] = usdt_coin_id
        user_res_info['seller_coin_id'] = coin_id
        user_res_info['user_token'] = user.get('token')
        set_login_status(staff_buss_api, user_token)
        set_login_status(staff_bal_api, user_token)
        # 前台申请，后端通过
        # otc平台申请成为商家
        res = otc_buss_api.biz_apply_post()

        admin_biz_rec = staff_buss_api.admin_biz_find_page_get(
            user_id=account_id)
        order_num = admin_biz_rec.items[0].id

        # 后台管理查看申请记录
        staff_buss_api.admin_biz_info_get(id=order_num)

        # 后台管理审核申请成功
        success_reaason = '您的信良好,继续保持'
        payload = AuditRequest(
            id=order_num, status=2, reason=success_reaason, file_recved=1)
        staff_buss_api.admin_biz_audit_post(payload)

        # 币币划拨资产到法币余额
        transload = TransferFromRequest(
            currency_id=usdt_coin_id, amount=1000000)
        otc_balance_api.balance_transfer_from_post(transload)
        transload = TransferFromRequest(currency_id=coin_id, amount=1000000)
        otc_balance_api.balance_transfer_from_post(transload)
        return user_res_info

    return create_all_done_account


@pytest.fixture(scope="function")
def otc_business_user(with_login):
    def create_all_done_account(api_list, platform='otc'):
        # 注册
        # 登录
        manager = PlatformManager(platform)
        account_api = manager.account_api
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        user = register_with_login(platform, with_login, [
            account_api, otc_balance_api, asset_api, verify_api, otc_buss_api,
            otc_asset_api
        ] + api_list)
        email = user.get("email")
        # 实名认证
        id_number = get_random_id_number()
        individual_verify(platform, id_number, user.get('token'))
        # 绑定手机号码
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(
            phone, DEFAULT_VERIFY_CODE, area_code="+86", token=verify.token)
        # 随机资金密码
        assert_password = faker.password()
        # 设置资金密码，
        # 需要二次验证才能设置资金密码
        res = verify_info(manager, email, 'edit_asset_pwd')
        base_token = res.token
        asset_api.asset_mgmt_asset_password_put(
            body={
                "password": user.get("password"),
                "traPassword": assert_password,
                "baseToken": base_token
            })
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set
        user_res_info = dict()
        user_res_info['asset_password'] = assert_password
        # 查询otc交易支持的币种列表
        otc_coin_list = otc_balance_api.balance_otc_coin_list_get()
        print('otc交易支持的币种列表:', otc_coin_list)
        seller_coins = []
        for i in otc_coin_list.items:
            i = i.to_dict()
            if i['short_name'] == 'USDT':
                usdt_coin_id = i['coin_id']
            else:
                seller_coins.append(i['coin_id'])
        coin_id = random.choice(seller_coins or [usdt_coin_id + 1])
        # assert len(res) == 0
        # return
        # random_coin = random.choice(res)
        # 充币金手指
        headers = {"Authorization": "Bearer {}".format(user.get('token'))}
        print('headers:', headers)
        host = configuration.host
        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        user_res_info['account_id'] = account_id
        # for _ in range(100):
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{coin_id}/1000000000',
            headers=headers)
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{usdt_coin_id}/10000000000',
            headers=headers)
        print('冲币res:', res)
        bb_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        print('币币余额:', bb_res2)
        return
        # 币币划拨资产到法币余额
        transload = TransferFromRequest(currency_id=coin_id, amount=1000000000)
        otc_balance_api.balance_transfer_from_post(transload)
        return user_res_info

    return create_all_done_account


@pytest.fixture(scope="function")
def limit_user(with_login):
    def create_limit_account(api_list, fail_type, platform='otc'):
        faker = Faker('zh_CN')
        user = random_user()
        user_res_info = dict()
        user_res_info['asset_password'] = ''
        manager = PlatformManager(platform)
        account_api = manager.account_api
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        manager.register(
            email=user["email"],
            password=user["password"],
            nationality_code=user["country_abbreviation"],
            nick_name=faker.name()
        )

        token = with_login(
            'otc',
            api_list + [account_api, otc_balance_api, verify_api, asset_api, otc_buss_api],
            account=user["email"],
            password=user["password"])
        email = user.get("email")
        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        user_res_info['account_id'] = account_id

        def bind_phone():
            phone = faker.phone_number()
            verify = verify_info(manager, email, "bind_phone")
            manager.bind_phone(
                phone, DEFAULT_VERIFY_CODE, area_code="+86", token=verify.token)

        def individual():
            id_number = get_random_id_number()
            individual_verify(platform, id_number, token)

        def assertr_pwd():
            # 设置资金密码
            asset_password = faker.password()
            res = verify_info(manager, email, 'edit_asset_pwd')
            base_token = res.token
            asset_api.asset_mgmt_asset_password_put(
                body={
                    "password": user.get("password"),
                    "traPassword": asset_password,
                    "baseToken": base_token
                })
            res = asset_api.asset_mgmt_asset_password_get()
            assert res.is_set
            user_res_info["asset_password"] = asset_password

        def biz_apply():
            # 后台登录
            admin_token = get_admin_token()
            user_res_info["admin_token"] = admin_token
            set_login_status(staff_buss_api, admin_token)

            # 前端申请
            # 后端通过
            otc_buss_api.biz_apply_post()
            admin_biz_rec = staff_buss_api.admin_biz_find_page_get(user_id=user_res_info['account_id'])
            order_num = admin_biz_rec.items[0].id

            staff_buss_api.admin_biz_info_get(id=order_num)

            success_reaason = "您的信良好"
            payload = AuditRequest(id=order_num, status=2, reason=success_reaason, file_recved=1)
            staff_buss_api.admin_biz_audit_post(payload)

        def deposit():
            otc_coin_list = otc_balance_api.balance_otc_coin_list_get()
            seller_coins = []
            for i in otc_coin_list.items:
                i = i.to_dict()
                if i['short_name'] == 'USDT':
                    usdt_coin_id = i['coin_id']
                else:
                    seller_coins.append(i['coin_id'])
            coin_id = random.choice(seller_coins or [usdt_coin_id + 1])  # random_coin.coin_id
            # 充币金手指
            headers = {"Authorization": "Bearer {}".format(token)}
            host = configuration.host
            user_res_info['buyer_coin_id'] = usdt_coin_id
            user_res_info['seller_coin_id'] = coin_id
            user_res_info['user_token'] = user.get('token')

            res = requests.post(
                f'{host}/asset-test/asset-initialize/{account_id}/{coin_id}',
                headers=headers)
            print(res)
            res = requests.post(
                f'{host}/asset-test/asset-initialize/{account_id}/{usdt_coin_id}',
                headers=headers)
            print(res)

            admin_token = get_admin_token()
            user_res_info["admin_token"] = admin_token
            set_login_status(staff_bal_api, user_res_info['admin_token'])
            # bb_res1 = asset_api.asset_mgmt_assets_coin_id_get(coin_id=usdt_coin_id)
            # print(bb_res1)
            transload = TransferFromRequest(currency_id=usdt_coin_id, amount=100_000)
            otc_balance_api.balance_transfer_from_post(transload)
            # bb_res2 = asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
            # print(bb_res2)
            transload = TransferFromRequest(currency_id=coin_id, amount=100_000)
            otc_balance_api.balance_transfer_from_post(transload)
        bind_phone()
        individual()
        assertr_pwd()
        deposit()
        if fail_type != 'not_biz':
            biz_apply()

        return user_res_info

    return create_limit_account
