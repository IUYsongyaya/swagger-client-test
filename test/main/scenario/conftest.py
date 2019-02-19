# @author: lj lh
import random
import pytest

import requests
from faker import Faker
from swagger_client.main.configuration import Configuration
from swagger_client.main.api import MarketApi, ExchangeApi, AccountApi
from swagger_client.main.api import AssetManagementApi
from swagger_client.tenant.api import AccountApi as TenantAccountApi
from swagger_client.tenant.api import MarketManagementApi
from common.account_sign import register_with_login, set_login_status
from common.utils import PlatformManager, get_random_id_number
from common.certification_verify import individual_verify

configuration = Configuration()
exchange_api = ExchangeApi()
market_api = MarketApi()
TURN_ON = 1
TURN_OFF = 0
DEFAULT_VERIFY_CODE = "666666"
EXCHANGE_NAME = 'BitMan'
# ENTRUST_EXCHANGE_NAME = 'zxy_exch_1'
ENTRUST_EXCHANGE_NAME = 'BitMan'


# ENTRUST_EXCHANGE_NAME = 'zxy_exch_99'


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
def special_login(entrust_login):
    def login(api_list, platform='main'):
        # 注册
        # 登录
        manager = PlatformManager(platform)
        account_api = manager.account_api
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        tenant_market_api = MarketManagementApi()
        user = register_with_login(platform, entrust_login, [
            account_api, asset_api, exchange_api, verify_api, market_api,
            tenant_market_api
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
        verify_info_res = verify_info(manager, email, 'edit_asset_pwd')
        base_token = verify_info_res.token
        asset_api.asset_mgmt_asset_password_put(
            body={
                "password": user.get("password"),
                "traPassword": assert_password,
                "baseToken": base_token
            })
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set

        # 获取交易所
        exchange_items = exchange_api.exchanges_suggestion_get(EXCHANGE_NAME)
        # 获取市场
        markets = market_api.markets_get(
            exchange_id=exchange_items[0]['id'], page=1)
        market_item = random.choice(markets.items)
        # print('市场信息:', markets)
        market_info = market_api.markets_id_get(market_item.id)

        buyer_coin_id = market_info.buyer_coin_id
        coin_id = market_info.seller_coin_id

        # 充币金手指
        headers = {"Authorization": "Bearer {}".format(user.get('token'))}
        host = configuration.host
        user_info = account_api.accounts_account_info_get()
        account_id = user_info.account_info.account_id
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{coin_id}/100000000000',
            headers=headers)
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{buyer_coin_id}/100000000000',
            headers=headers)

        result = {
            "coin_id": coin_id,
            "buyer_coin_id": buyer_coin_id,
            "account_id": account_id,
            "headers": headers,
            "market_id": market_item.id,
            "exchange_id": exchange_items[0]['id'],
            "precision": market_info.price_places
        }
        return result
        # return coin_id

    return login


@pytest.fixture(scope='function')
def entrust_special_login(entrust_login):
    def login(api_list, platform='main'):
        # 注册
        # 登录
        manager = PlatformManager(platform)
        account_api = manager.account_api
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        tenant_market_api = MarketManagementApi()
        main_asset_api = AssetManagementApi()
        user = register_with_login(platform, entrust_login, [
            account_api, asset_api, exchange_api, verify_api, market_api, tenant_market_api, main_asset_api
        ] + api_list)

        email = user.get('email')
        password = user.get('password')
        token = user.get('token')
        print('主平台用户邮箱,密码:', email, password)

        # 个人实名认证
        id_number = get_random_id_number()
        individual_verify(platform, id_number, user.get('token'))
        # 绑定手机号码
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, 'bind_phone')
        manager.bind_phone(
            phone, DEFAULT_VERIFY_CODE, area_code='+86', token=verify.token)
        # 随机资金密码
        asset_password = faker.password()
        # 设置资金密码,
        # 需要二次验证才能设置资金密码
        verify_info_res = verify_info(manager, email, 'edit_asset_pwd')
        base_token = verify_info_res.token
        asset_api.asset_mgmt_asset_password_put(
            body={
                'password': user.get('password'),
                'traPassword': asset_password,
                'baseToken': base_token
            }
        )
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set
        # 获取交易所
        # exchange_item = exchange_api.exchanges_suggestion_get(name=ENTRUST_EXCHANGE_NAME)
        exchange_item = exchange_api.exchanges_suggestion_get(name=ENTRUST_EXCHANGE_NAME)
        exchange_id = exchange_item[0]['id']
        # 获取市场
        markets = market_api.markets_get(
            exchange_id=exchange_id, page=1)
        print('市场列表信息:', markets)
        # market_item = random.choice(markets.items)
        market_item = [i for i in markets.items if i.id == '61']
        # market_item = [i for i in markets.items if i.id == '218']
        market_info = market_api.markets_id_get(market_item[0].id)
        print('市场信息:', market_info)
        buy_coin_id = market_info.buyer_coin_id
        sell_coin_id = market_info.seller_coin_id

        # 冲币金手指
        headers = {'Authorization': 'Bearer {}'.format(user.get('token'))}
        host = configuration.host
        user_info = account_api.accounts_account_info_get()
        account_id = user_info.account_info.account_id
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{buy_coin_id}/100000000000',
            headers=headers)
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{sell_coin_id}/100000000000',
            headers=headers)
        print('res:', res)
        main_bb_bal = main_asset_api.asset_mgmt_assets_get()
        asset_res_list = [i for i in main_bb_bal.asset_info if i.coin_id == '1']
        print('主平台bb余额:', asset_res_list)
        result = {
            'buy_coin_id': buy_coin_id,
            'sell_coin_id': sell_coin_id,
            'account_id': account_id,
            'headers': headers,
            'market_id': market_item[0].id,
            'exchange_id': exchange_id,
            'precision': market_info.price_places,
            'total_rate': market_info.total_rate,
            'token': token
        }
        return result

    return login


@pytest.fixture(scope='function')
def less_entrust_special_login(entrust_login):
    def login(api_list, platform='main'):
        # 注册
        # 登录
        manager = PlatformManager(platform)
        account_api = manager.account_api
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        tenant_market_api = MarketManagementApi()
        user = register_with_login(platform, entrust_login, [
            account_api, asset_api, exchange_api, verify_api, market_api, tenant_market_api
        ] + api_list)

        email = user.get('email')
        token = user.get('token')
        # 个人实名认证
        id_number = get_random_id_number()
        individual_verify(platform, id_number, user.get('token'))
        # 绑定手机号码
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, 'bind_phone')
        manager.bind_phone(
            phone, DEFAULT_VERIFY_CODE, area_code='+86', token=verify.token)
        # 随机资金密码
        asset_password = faker.password()
        # 设置资金密码,
        # 需要二次验证才能设置资金密码
        verify_info_res = verify_info(manager, email, 'edit_asset_pwd')
        base_token = verify_info_res.token
        asset_api.asset_mgmt_asset_password_put(
            body={
                'password': user.get('password'),
                'traPassword': asset_password,
                'baseToken': base_token
            }
        )
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set
        # 获取交易所
        exchange_item = exchange_api.exchanges_suggestion_get(name=ENTRUST_EXCHANGE_NAME)
        exchange_id = exchange_item[0]['id']
        print('交易所id:', exchange_id)
        # 获取市场
        markets = market_api.markets_get(
            exchange_id=exchange_id, page=1)
        print('市场列表信息:', markets)
        # market_item = random.choice(markets.items)
        market_item = [i for i in markets.items if i.id == '61']
        # market_item = [i for i in markets.items if i.id == '218']
        market_info = market_api.markets_id_get(market_item[0].id)
        print('市场信息:', market_info)
        buy_coin_id = market_info.buyer_coin_id
        sell_coin_id = market_info.seller_coin_id

        # 冲币金手指
        headers = {'Authorization': 'Bearer {}'.format(user.get('token'))}
        host = configuration.host
        user_info = account_api.accounts_account_info_get()
        account_id = user_info.account_info.account_id
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{buy_coin_id}/100000000000',
            headers=headers)
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{sell_coin_id}/100000000000',
            headers=headers)
        result = {
            'buy_coin_id': buy_coin_id,
            'sell_coin_id': sell_coin_id,
            'account_id': account_id,
            'headers': headers,
            'market_id': market_item[0].id,
            'exchange_id': exchange_id,
            'precision': market_info.price_places,
            'total_rate': market_info.total_rate,
            'token': token
        }
        return result

    return login


@pytest.fixture(scope="function")
def quotation_special_login(entrust_login):
    def login(api_list, platform='main'):
        # 注册
        # 登录
        tenant_ac_api = TenantAccountApi()
        manager = PlatformManager(platform)
        account_api = manager.account_api
        tenant_market_api = MarketManagementApi()
        market_api = MarketApi()
        main_asset_api = AssetManagementApi()
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        user = register_with_login(platform, entrust_login, [
            account_api, asset_api, verify_api, market_api, tenant_ac_api,
            main_asset_api, tenant_market_api
        ] + api_list)

        # 租户平台授权登录
        # tenant_ac_api.create_platform()
        email = user.get("email")
        token = user.get('token')
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
        verify_info_res = verify_info(manager, email, 'edit_asset_pwd')
        print('二次验证信息:', verify_info_res)
        base_token = verify_info_res.token
        asset_api.asset_mgmt_asset_password_put(
            body={
                "password": user.get("password"),
                "traPassword": assert_password,
                "baseToken": base_token
            })
        res = asset_api.asset_mgmt_asset_password_get()
        assert res.is_set
        # 获取市场交易服务费率
        tenant_market_api.service_rate_get()
        # 获取交易所
        exchange_item = exchange_api.exchanges_suggestion_get(name=ENTRUST_EXCHANGE_NAME)
        exchange_id = exchange_item[0]['id']
        print('交易所id:', exchange_id)
        # 获取市场
        markets = market_api.markets_get(
            exchange_id=exchange_id, page=1)
        print('市场列表信息:', markets)
        # market_item = random.choice(markets.items)
        market_info = market_api.markets_id_get(markets.items[2].id)
        # market_item = [i for i in markets.items if i.id == '61']
        # market_info = market_api.markets_id_get(market_item[0].id)
        print('市场信息:', market_info)
        buy_coin_id = market_info.buyer_coin_id
        sell_coin_id = market_info.seller_coin_id
        # 充币金手指
        headers = {"Authorization": "Bearer {}".format(user.get('token'))}
        host = configuration.host
        user_info = account_api.accounts_account_info_get()
        account_id = user_info.account_info.account_id
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{buy_coin_id}/100000000000',
            headers=headers)
        print('res:', res)
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{sell_coin_id}/100000000000',
            headers=headers)
        # print('res:', res)
        # 获取币币余额
        main_bb_bal = main_asset_api.asset_mgmt_assets_get()
        asset_res_list = [i for i in main_bb_bal.asset_info if i.coin_id == buy_coin_id]
        print('主平台bb余额:', asset_res_list)
        result = {
            'buy_coin_id': buy_coin_id,
            'sell_coin_id': sell_coin_id,
            'account_id': account_id,
            'headers': headers,
            'market_id': markets.items[2].id,
            'exchange_id': exchange_id,
            'precision': market_info.price_places,
            'total_rate': market_info.total_rate,
            'token': token
        }
        return result

    return login


@pytest.fixture(scope='function')
def set_tenant_login(with_login):
    def login(api_list, platform='main'):
        # 注册
        # 登录
        tenant_ac_api = TenantAccountApi()
        manager = PlatformManager(platform)
        account_api = manager.account_api
        user = {
            'email': 'ZXY_tenant_1@gmail.com',
            'password': 'ZXY_tenant_pwd',
            'token': ''
        }
        user_token = with_login(
            platform, [account_api, tenant_ac_api] + api_list,
            account=user['email'],
            password=user['password'])

        user['token'] = user_token
        # 租户平台授权登录
        # tenant_ac_api.create_platform()
        return user

    return login


@pytest.fixture(scope="function")
def set_user_login(entrust_login):
    def login(api_list, platform='main'):
        # 注册
        # 登录
        manager = PlatformManager(platform)
        account_api = manager.account_api
        market_api = MarketApi()
        asset_api = manager.asset_api
        verify_api = manager.verify_api
        user = {'email': 'xjtuab@gmail.com', 'password': '12345678a', 'token': ''}
        user_token = entrust_login(
            platform,
            [account_api, asset_api, verify_api, market_api] + api_list,
            account=user['email'],
            password=user['password'])
        user['token'] = user_token

        email = user.get("email")
        # 实名认证
        # id_number = get_random_id_number()
        # individual_verify(platform, id_number, user.get('token'))
        # 绑定手机号码
        faker = Faker('zh_CN')
        # phone = faker.phone_number()
        # verify = verify_info(manager, email, "bind_phone")
        # manager.bind_phone(
        # phone, DEFAULT_VERIFY_CODE, area_code="+86", token=verify.token)
        # 随机资金密码
        # assert_password = faker.password()
        # 设置资金密码，
        # 需要二次验证才能设置资金密码
        # verify_info_res = verify_info(manager, email, 'edit_asset_pwd')
        # base_token = verify_info_res.token
        # asset_api.asset_mgmt_asset_password_put(
        # body={
        # "password": user.get("password"),
        # "traPassword": assert_password,
        # "baseToken": base_token
        # })
        # res = asset_api.asset_mgmt_asset_password_get()
        # assert res.is_set

        exchange_item = exchange_api.exchanges_suggestion_get(name=ENTRUST_EXCHANGE_NAME)
        exchange_id = exchange_item[0]['id']
        # 获取市场
        markets = market_api.markets_get(
            exchange_id=exchange_id, page=1)
        # market_item = random.choice(markets.items)
        market_item = [i for i in markets.items if i.id == '2']
        # print('市场列表信息:', markets)
        market_info = market_api.markets_id_get(market_item[0].id)
        # print('市场信息:', market_info)
        buy_coin_id = market_info.buyer_coin_id
        sell_coin_id = market_info.seller_coin_id

        # 冲币金手指
        headers = {'Authorization': 'Bearer {}'.format(user.get('token'))}
        host = configuration.host
        user_info = account_api.accounts_account_info_get()
        account_id = user_info.account_info.account_id
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{coin_id}/1000000000',
            headers=headers)
        res = requests.post(
            f'{host}/asset-test/asset-initialize/{usdt_coin_id}/1000000000',
            headers=headers)
        print(res)
        return

    return login
