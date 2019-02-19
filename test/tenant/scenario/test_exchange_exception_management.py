# @Author  : ymy
# @Email   : yaomingyong@wanshare.com
# @Time    : 18-11-12 下午2:28
import pytest
import random
import string
import requests
from faker import Faker
from pprint import pprint
from common.photo import PHOTO_KEY
from common.account_sign import register_with_login, get_admin_token, set_login_status
from common.certification_verify import individual_verify, company_verify
from common.utils import PlatformManager, random_get_country_ob, get_random_id_number
from swagger_client.tenant.rest import ApiException
from swagger_client.staff.api.audit_api import AuditApi
from swagger_client.tenant.api.account_api import AccountApi
from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
from swagger_client.staff.api.account_management_api import AccountManagementApi
from swagger_client.staff.api.website_management_api import WebsiteManagementApi
from swagger_client.staff.models.post_exchange_tags_request import PostExchangeTagsRequest
from swagger_client.tenant.models.get_exchange_request import GetExchangeRequest
from swagger_client.staff.models.post_tenant_audit_request import PostTenantAuditRequest
from swagger_client.staff.models.post_tenant_re_audit_request import PostTenantReAuditRequest


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
    """1.个人实名认证不通过——提交交易所申请信息——>异常"""

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
        individual_verify('tenant', id_number, token, 'REJECTED', 'INDIVIDUAL_PASSPORT')
        try:
            exchange_api.exchange_post(exchange)
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, '个人实名认证不通过不应该创建交易所'


class TestExchange2(object):
    """2.企业实名认证不通过——提交交易所申请信息——>异常"""

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
        company_verify('tenant', social_code, token, 'REJECTED', 'INDIVIDUAL_PASSPORT')
        a_api = AuditApi()
        admin_token = get_admin_token()
        set_login_status(a_api, admin_token)
        rv = a_api.accounts_company_audits_get(social_number=social_code,
                                               status='REJECTED')
        item = rv.items[0]
        account_id = item.account_id
        rv = a_api.accounts_company_audits_id_get(account_id)
        assert rv.account_id == account_id
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        try:
            exchange_api.exchange_post(exchange)
        except ApiException as e:
            assert e.status == 400
        else:
            assert False, '企业未认证通过，不应该创建交易所'


class TestExchange8(object):
    """8.提交交易所申请信息——获取交易所状态——后台初审不通过——复审——异常"""
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
        res = PostTenantReAuditRequest(id=task_id,
                                       status='approved')
        try:
            audit_api.tenant_audits_re_audit_post(res)
        except Exception as e:
            assert e.status == 400
        else:
            assert False, '初审未过，不应当通过复审'


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

        name = e.get_random_exchange_name()
        exchange.name = ' ' + name + ' '
        exchange_api.exchange_put(exchange)
        rv = exchange_api.exchange_get()
        assert rv.name == name


class TestExchangeExec1(object):

    def test_investors(self, with_login):
        """3.未开通交易所——获取投资人列表列表———投资人详情（exchange id is None）"""
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
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        rv = audit_api.tenant_audits_get(uid=account_id,
                                         exchange_name=exchange.name,
                                         type='audit')
        task = rv.items[0]
        task_id = task.id
        res = PostTenantAuditRequest(id=task_id, is_data_received=True,
                                     status='approved')
        audit_api.tenant_audits_audit_post(res)
        # 复审不通过
        res = PostTenantReAuditRequest(id=task_id,
                                       status='disapproved',
                                       failure_type='ENTERPRISE_LICENSE')
        audit_api.tenant_audits_re_audit_post(res)

        api = AccountManagementApi()
        admin_token = get_admin_token()
        set_login_status(api, admin_token)
        a_api = AccountApi()
        token = with_login('tenant', [a_api], email, password)
        account_info = a_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        rv = api.accounts_investors_get(account_id=account_id)
        investors = rv.items
        assert len(investors) > 0
        rv = api.accounts_accounts_id_get(id=account_id)
        assert rv.basic_info.exchange_id is None


class TestExchange11(object):
    """11.提交交易所申请信息——获取交易所状态——审核不通过——获取交易所详情——更新交易所信息——获取交易所详情"""
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
                                     status='approved')
        audit_api.tenant_audits_audit_post(res)
        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='disapproved',
                                       failure_type='ENTERPRISE_LICENSE')
        audit_api.tenant_audits_re_audit_post(res)
        rv = exchange_api.exchange_exchange_status_get()
        assert rv.status == 'disapproved'
        try:
            exchange_api.exchange_get()
        except Exception as e:
            assert e.status == 400
        else:
            assert False, '交易所审核未通过，不应当获取到交易所'
