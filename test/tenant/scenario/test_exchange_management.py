# @Author  : ymy
# @Email   : yaomingyong@wanshare.com
# @Time    : 18-11-12 下午2:28
import time
import pytest
import random
import string
import requests
from faker import Faker
from common.photo import PHOTO_KEY
from swagger_client.main.api.account_api import AccountApi as MainAccountApi
from common.account_sign import register_with_login, get_admin_token, set_login_status
from common.certification_verify import individual_verify, company_verify
from common.utils import PlatformManager, random_get_country_ob, get_random_id_number
from swagger_client.tenant.rest import ApiException
from swagger_client.staff.rest import ApiException as StaffApiException
from swagger_client.staff.api.audit_api import AuditApi
from swagger_client.main.api.exchange_api import ExchangeApi
from swagger_client.tenant.api.account_api import AccountApi
from swagger_client.main.models.post_plat_form_register_request import PostPlatFormRegisterRequest
from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
from swagger_client.staff.api.account_management_api import AccountManagementApi
from swagger_client.staff.api.website_management_api import WebsiteManagementApi
from swagger_client.main.api.favorite_management_api import FavoriteManagementApi
from swagger_client.main.models.post_favoriter_request import PostFavoriterRequest
from swagger_client.staff.models.post_exchange_tags_request import PostExchangeTagsRequest
from swagger_client.tenant.models.get_exchange_request import GetExchangeRequest
from swagger_client.staff.models.post_tenant_audit_request import PostTenantAuditRequest
from swagger_client.staff.models.post_tenant_re_audit_request import PostTenantReAuditRequest
from swagger_client.staff.api.exchange_management_api import ExchangeManagementApi as StaffExchangeManagementApi


img = PHOTO_KEY
img1 = PHOTO_KEY
admin, admin_password = 'admin', 'Lx123456'
tenant_url = 'http://crush-tenant.s1.c58c7e25a004943cdad05a1bf31f354b7.cn-shenzhen.alicontainer.com'
# tenant_url = 'http://crush-tenant.crush-deploy.lan/api'
DEFAULT_VERIFY_CODE = "666666"


def get_bearer(token):
    bearer = f'Bearer {token}'
    return {'Authorization': bearer}


def exchange_name_verify(token, name):
    url = f'{tenant_url}/exchange/exchange-name-verify'
    headers = get_bearer(token)
    rv = requests.get(url, params={'name': name}, headers=headers).json()
    return rv['bit']


def verify_info(manager, account, verify_type):
    verify_ = {"challenge": "",
               "seccode": "",
               "validate": "",
               "account": "mailto:" + account,
               "code": DEFAULT_VERIFY_CODE,
               "type": verify_type}
    if verify_type in ["alter_phone", "alter_google"]:
        verify_.update({"secondCode": DEFAULT_VERIFY_CODE})
    return manager.verify(verify_)


def get_social_code():
    """长度8-64字符串"""
    length = random.choice(range(8, 65))
    base_string = string.ascii_letters + string.digits
    return ''.join(random.choice(base_string) for _ in range(length))


class Exchange(object):
    def __init__(self, manager, token):
        self.manager = manager
        self.token = token

    def get_random_exchange_name(self):
        name = 'exchange' + str(random.randint(1, 1000))
        url = f"{tenant_url}/exchange/exchange-name-verify"
        bearer = f'Bearer {self.token}'
        headers = {'Authorization': bearer}
        while True:
            rsp = requests.get(url, params={'name': name}, headers=headers)
            rv = rsp.json()
            if not rv['bit']:
                break
            name = 'exchange' + str(random.randint(1, 10000))
        return name

    def get_random_tags(self):
        rv = self.manager.tags_get()
        tags = rv.tags
        if tags:
            amount = random.randint(1, min(3, len(tags)))
            rv = random.sample(tags, amount)
            tag = ','.join(rv)
            return tag
        else:
            admin_token = get_admin_token()
            api = WebsiteManagementApi()
            set_login_status(api, admin_token)
            res = PostExchangeTagsRequest()
            res.name = 'tag_' + str(random.randint(1, 122222))
            res.other_language = [{
              "key": "英语",
              "value": "public_chain"
            }]
            api.exchange_tags_post(res)
            return res.name

    def get_exchange(self):
        faker = Faker('zh_CN')
        random_country = random_get_country_ob()
        tags = self.get_random_tags()
        g = GetExchangeRequest()
        g.name = self.get_random_exchange_name()
        g.nationality = '+' + random_country.get('k')
        g.logo = img
        g.tags = tags
        g.phone = faker.phone_number()
        g.email = faker.email()
        return g


class TestExchange1(object):
    """1.个人实名认证通过——提交交易所申请信息——>获取交易所状态"""

    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant',
                                   with_login,
                                   [api, verify_api])
        self.data['user'] = user
        email = user.get('email')
        account_info = api.accounts_account_info_get()
        # 绑定电话
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email = user.get('email')
        password = user.get('password')
        token = with_login('tenant', [exchange_api], email, password)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        self.data['exchange'] = exchange
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        exchange_api.exchange_post(exchange)

    @pytest.mark.order3
    def test_exchange_get(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email = user['email']
        password = user['password']
        with_login('tenant', [exchange_api], email, password)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'


class TestExchange2(object):
    """2.企业实名认证通过——提交交易所申请信息——>获取交易所状态"""

    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login, [api, verify_api])
        self.data['user'] = user

        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

    @pytest.mark.order2
    def test_apply_company_verify(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email, password = user['email'], user['password']
        social_code = get_social_code()
        token = with_login('tenant', [exchange_api], email, password)
        company_verify('tenant', social_code, token)
        a_api = AuditApi()
        admin_token = get_admin_token()
        set_login_status(a_api, admin_token)
        rv = a_api.accounts_company_audits_get(social_number=social_code,
                                               status='ACCEPTED')
        item = rv.items[0]
        account_id = item.account_id
        rv = a_api.accounts_company_audits_id_get(account_id)
        assert rv.account_id == account_id
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)

    @pytest.mark.order3
    def test_exchange_get(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email = user['email']
        password = user['password']
        with_login('tenant', [exchange_api], email, password)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'


class TestExchange3(object):
    """3.个人实名认证不通过——提交交易所申请信息"""

    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login, [api, verify_api])
        self.data['user'] = user

        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email = user['email']
        password = user['password']
        token = with_login('tenant', [exchange_api], email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token, 'REJECTED',
                          'INDIVIDUAL_PASSPORT')
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        try:
            exchange_api.exchange_post(exchange)
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, '审核未过不应该创建交易所'


class TestExchange4(object):
    """4.企业实名认证不通过——提交交易所申请信息"""

    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login, [api, verify_api])
        self.data['user'] = user

        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

    @pytest.mark.order2
    def test_apply_company_verify(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email, password = user['email'], user['password']
        social_code = get_social_code()
        token = with_login('tenant', [exchange_api], email, password)
        company_verify('tenant', social_code, token, 'REJECTED',
                       'ENTERPRISE_LICENSE')
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        try:
            exchange_api.exchange_post(exchange)
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, '企业实名认证不通过，不应当创建交易所'


class TestExchange5(object):
    """5.提交交易所申请信息——获取交易所名称状态——获取交易所详情"""
    pass  # 已经合并到TestExchange1和TestExchange２中


class TestExchange6(object):
    """6.提交交易所申请信息（已注册的交易所名称）——获取交易所名称状态"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        account_api = AccountApi()
        manager = PlatformManager('tenant')
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login, [api, verify_api, account_api])
        self.data['user'] = user
        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        self.data['account_id'] = account_id
        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        user1 = register_with_login('tenant', with_login, [api, verify_api])
        self.data['user1'] = user1
        # 绑定电话
        email1 = user1.get('email')
        phone1 = faker.phone_number()
        verify = verify_info(manager, email1, "bind_phone")
        manager.bind_phone(phone1, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        audit_api = AuditApi()
        user = self.data['user']
        email = user['email']
        password = user['password']
        exchange_api = ExchangeManagementApi()
        token = with_login('tenant', [exchange_api], email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)

        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        # 初审
        uid = self.data['account_id']
        rv = audit_api.tenant_audits_get(uid=uid,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='approved', failure_type=1)
        audit_api.tenant_audits_audit_post(res)
        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='approved',
                                       failure_type=None)
        audit_api.tenant_audits_re_audit_post(res)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'approved'
        try:
            user1 = self.data['user1']
            email1, password1 = user1['email'], user1['password']
            exchange_api1 = ExchangeManagementApi()
            token1 = with_login('tenant', [exchange_api1], email1, password1)
            id_number = get_random_id_number()
            individual_verify('tenant', id_number, token1)
            # print(token1)
            exchange1 = e.get_exchange()
            exchange1.name = exchange.name
            # pprint(exchange1)
            exchange_api1.exchange_post(exchange1)
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, '交易所名称重复不应当创建'
        assert exchange_name_verify(token, exchange.name), '交易所名称应当已经存在'


class TestExchange7(object):
    """7.提交交易所申请信息——获取交易所状态——后台初审、复审通过——获取交易所状态"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        self.data['user'] = user

        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        self.data['account_id'] = account_id

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        audit_api = AuditApi()
        user = self.data['user']
        email = user['email']
        password = user['password']
        exchange_api = ExchangeManagementApi()
        e_api = ExchangeApi()
        ma_api = MainAccountApi()
        f_api = FavoriteManagementApi()
        token = with_login('tenant',
                           [exchange_api, e_api, f_api, ma_api],
                           email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        # 初审
        uid = self.data['account_id']
        rv = audit_api.tenant_audits_get(uid=uid,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='approved')
        audit_api.tenant_audits_audit_post(res)
        # 初审详情
        rv = audit_api.tenant_audits_results_id_company_audit_get(task_id)
        assert rv.audit_status == 'approved'
        assert rv.uid == uid

        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='approved')
        audit_api.tenant_audits_re_audit_post(res)
        # 复审详情
        rv = audit_api.tenant_audits_results_id_company_re_audit_get(task_id)
        assert rv.audit_status == 'approved'
        assert rv.uid == uid
        assert rv.re_status == 'approved'

        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'approved'

        # 合并测试用例
        """2.新增交易所——交易所列表模糊查询——收藏——收藏列表（交易所）"""
        # res = PostPlatFormRegisterRequest()
        # ma_api.create_platform(body=res)
        rv = e_api.exchanges_suggestion_get(name=exchange.name)
        assert len(rv) >= 1
        exchange_id = rv[0]['id']
        # 收藏
        req = PostFavoriterRequest()
        req.favorite_id = exchange_id
        req.type = 'exchange'
        f_api.favorites_post(req)
        # 收藏列表
        rv = f_api.favorites_get(type='exchange')
        items = rv.items
        assert len(items) == 1
        item = items[0]
        assert item.favorite_id == exchange_id
        favorite_record_id = item.id

        """6.收藏交易所成功——收藏列表（交易所）——取消收藏"""
        # 取消收藏
        f_api.favorites_delete(favorite_record_id)
        rv = f_api.favorites_is_favorite_get(favorite_id=exchange_id,
                                             type='exchange')
        assert not rv.status


class TestExchange8(object):
    """8.提交交易所申请信息——获取交易所状态——后台初审不通过——获取交易所状态——获取交易所详情"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        self.data['user'] = user
        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        self.data['account_id'] = account_id

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email = user['email']
        password = user['password']
        token = with_login('tenant', [exchange_api], email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)

        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'

        # 初审不通过
        audit_api = AuditApi()
        uid = self.data['account_id']
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        rv = audit_api.tenant_audits_get(uid=uid,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='disapproved',
                                     failure_type='ENTERPRISE_LICENSE')
        audit_api.tenant_audits_audit_post(res)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'disapproved'


class TestExchange9(object):
    """9.提交交易所申请信息——获取交易所状态——后台复审不通过——获取交易所状态——获取交易所详情"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        self.data['user'] = user

        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        self.data['account_id'] = account_id

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email, password = user['email'], user['password']
        token = with_login('tenant', [exchange_api], email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'
        # 初审
        audit_api = AuditApi()
        uid = self.data['account_id']
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        rv = audit_api.tenant_audits_get(uid=uid,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='approved',
                                     failure_type='ENTERPRISE_LICENSE')
        audit_api.tenant_audits_audit_post(res)
        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='disapproved',
                                       failure_type=1)
        audit_api.tenant_audits_re_audit_post(res)

        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'disapproved'


class TestExchange10(object):
    """10.提交交易所申请信息——获取交易所状态——审核通过——更新交易所信息——提交交易所名称已注册"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        self.data['user'] = user
        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        self.data['account_id'] = account_id

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        user = self.data['user']
        exchange_api = ExchangeManagementApi()
        email, password = user['email'], user['password']
        token = with_login('tenant', [exchange_api], email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'
        audit_api = AuditApi()
        uid = self.data['account_id']
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        rv = audit_api.tenant_audits_get(uid=uid,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='approved',
                                     failure_type='ENTERPRISE_LICENSE')
        audit_api.tenant_audits_audit_post(res)
        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='approved',
                                       failure_type='ENTERPRISE_LICENSE')
        audit_api.tenant_audits_re_audit_post(res)

        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'approved'
        rv = exchange_api.exchange_exchange_id_get()
        exchange_id = rv.id
        TestExchange10.data['exchange_id'] = exchange_id
        TestExchange10.data['exchange'] = exchange
        # 用另外一个账号再创建一个交易所
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        token1 = user['token']
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token1)
        exchange1 = e.get_exchange()
        exchange_api.exchange_get()
        name_used = exchange1.name
        # 用已有的交易所名称更新前一个交易所
        r = GetExchangeRequest(name=name_used)
        try:
            exchange_api.exchange_put(r)
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, '交易所名称已经注册'

    @pytest.mark.order3
    def test_exchange_list(self):
        """1.前台申请交易所并审核成功——获取交易所列表——获取交易所详情"""
        # 获取交易所列表
        api = StaffExchangeManagementApi()
        admin_token = get_admin_token()
        set_login_status(api, admin_token)
        exchange_id = TestExchange10.data['exchange_id']
        res = api.exchanges_get(exchange_id=exchange_id)
        assert len(res.items) == 1
        exchange_name = TestExchange10.data['exchange'].name
        assert len(res.items) >= 1
        # 获取交易所详情
        rv = api.exchange_id_get(id=exchange_id)
        assert rv.exchange_name == exchange_name
        assert rv.exchange_id == exchange_id

    @pytest.mark.order4
    def test_investors(self, with_login):
        """3.前台已开通交易所——获取用户列表——获取账号信息详情"""
        api = AccountManagementApi()
        admin_token = get_admin_token()
        set_login_status(api, admin_token)
        a_api = AccountApi()
        user = self.data['user']
        email, password = user['email'], user['password']
        token = with_login('tenant', [a_api], email, password)
        account_info = a_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        rv = api.accounts_investors_get(account_id=account_id)
        investors = rv.items
        assert len(investors) > 0
        rv = api.accounts_accounts_id_get(id=account_id)
        exchange_id = TestExchange10.data['exchange_id']
        assert rv.basic_info.exchange_id == exchange_id


class TestExchange11(object):
    """11.提交交易所申请信息——获取交易所状态——审核通过——获取交易所详情——更新交易所信息——获取交易所详情"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        self.data['user'] = user

        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        self.data['account_id'] = account_id

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        exchange_api = ExchangeManagementApi()
        user = self.data['user']
        email, password = user['email'], user['password']
        token = with_login('tenant', [exchange_api], email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'
        # 初审
        audit_api = AuditApi()
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        uid = self.data['account_id']
        rv = audit_api.tenant_audits_get(uid=uid,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='approved',
                                     failure_type='ENTERPRISE_LICENSE')
        audit_api.tenant_audits_audit_post(res)
        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='approved',
                                       failure_type='ENTERPRISE_LICENSE')
        audit_api.tenant_audits_re_audit_post(res)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'approved'
        rv = exchange_api.exchange_get()
        assert rv.name == exchange.name
        assert rv.logo_key == exchange.logo
        assert rv.email == exchange.email
        assert rv.nationality == exchange.nationality
        exchange.logo = img1
        exchange_api.exchange_put(exchange)
        rv = exchange_api.exchange_get()
        assert rv.name == exchange.name
        assert rv.logo_key == exchange.logo
        assert rv.email == exchange.email
        assert rv.nationality == exchange.nationality

        """合并测试用例"""
        """12.交易所审核通过——获取交易所ID——获取交易所买卖方币种列表"""
        coin = exchange_api.exchange_exchange_coin_get()
        assert coin.seller_coin == []

# class TestExchange13(object):
#     """13.市场挂单——获取委托订单列表"""
#
#
# class TestExchange14(object):
#     """14.市场成交——获取委托成交订单列表——获取成交记录列表"""


class TestExchange15(object):
    """2.用户前台未开通交易所——后台开通交易所——交易所账号审核列表（后台审核）
    ——前台获取交易所行情"""
    def test_exchange(self, with_login):
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, user['token'])

        e_api = StaffExchangeManagementApi()
        a_api = AccountManagementApi()
        admin_token = get_admin_token()
        audit_api = AuditApi()
        set_login_status(audit_api, admin_token)
        set_login_status(e_api, admin_token)
        set_login_status(a_api, admin_token)
        # 用户列表
        rv = a_api.accounts_investors_get(account_id=account_id)
        assert rv.items

        # 后台开通交易所
        req = {
            "accountId": account_id,
            "area": "+86",
            "email": str(int(time.time())) + "@qq.com",
            "logo": "",
            "name": str(int(time.time())),
            "phone": "15548494655",
            "tags": ""
        }
        e_api.exchange_post(req)
        # 交易所审核列表
        rv = audit_api.tenant_audits_get(uid=account_id)
        item = rv.items[0]
        assert item.status == 'approved'


class TestExchange(object):
    def test_get_exchanges(self):
        """获取交易所列表"""
        api = StaffExchangeManagementApi()
        admin_token = get_admin_token()
        set_login_status(api, admin_token)
        rv = api.exchanges_get()

    def test_post_tag(self):
        """创建tag"""
        api = WebsiteManagementApi()
        admin_token = get_admin_token()
        set_login_status(api, admin_token)
        res = PostExchangeTagsRequest()
        res.name = 'test_tag_' + str(random.randint(1, 10000))
        res.other_language = [
            {
                'key': '英语',
                'value': 'public_chain'
            }
        ]
        api.exchange_tags_post(res)


class TestExchange16(object):
    """7.提交交易所申请信息——获取交易所状态——后台初审不通过--后台复审异常（不允许初审不通过时复审）——获取交易所状态"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        self.data['user'] = user

        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        self.data['account_id'] = account_id

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        audit_api = AuditApi()
        user = self.data['user']
        email = user['email']
        password = user['password']
        exchange_api = ExchangeManagementApi()
        e_api = ExchangeApi()
        f_api = FavoriteManagementApi()
        token = with_login('tenant',
                           [exchange_api, e_api, f_api],
                           email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        # 初审
        uid = self.data['account_id']
        rv = audit_api.tenant_audits_get(uid=uid,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='disapproved')
        audit_api.tenant_audits_audit_post(res)
        # 初审详情
        rv = audit_api.tenant_audits_results_id_company_audit_get(task_id)
        assert rv.audit_status == 'disapproved'
        assert rv.uid == uid

        # 复审
        try:
            res = PostTenantReAuditRequest(id=task_id,
                                           status='disapproved')
            audit_api.tenant_audits_re_audit_post(res)
        except StaffApiException as e:
            assert e.status == 400
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'disapproved'


class TestExchange17(object):
    """7.提交交易所申请信息——获取交易所状态——后台初审通过--后台复审通过——获取交易所状态"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        account_api = AccountApi()
        api = manager.account_api
        verify_api = manager.verify_api
        user = register_with_login('tenant', with_login,
                                   [api, verify_api, account_api])
        self.data['user'] = user

        # 绑定电话
        email = user.get('email')
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)

        account_info = account_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        self.data['account_id'] = account_id

    @pytest.mark.order2
    def test_exchange_post(self, with_login):
        audit_api = AuditApi()
        user = self.data['user']
        email = user['email']
        password = user['password']
        exchange_api = ExchangeManagementApi()
        e_api = ExchangeApi()
        f_api = FavoriteManagementApi()
        token = with_login('tenant',
                           [exchange_api, e_api, f_api],
                           email, password)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        exchange_api.exchange_post(exchange)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'pending'
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        # 初审
        uid = self.data['account_id']
        rv = audit_api.tenant_audits_get(uid=uid,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='approved')
        audit_api.tenant_audits_audit_post(res)
        # 初审详情
        rv = audit_api.tenant_audits_results_id_company_audit_get(task_id)
        assert rv.audit_status == 'approved'
        assert rv.uid == uid
        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='disapproved')
        audit_api.tenant_audits_re_audit_post(res)
        # 复审详情
        rv = audit_api.tenant_audits_results_id_company_re_audit_get(task_id)
        assert rv.audit_status == 'approved'
        assert rv.uid == uid
        assert rv.re_status == 'disapproved'

        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'disapproved'
