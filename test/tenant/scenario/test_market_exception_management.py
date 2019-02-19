# @Author  : ymy
# @Email   : yaomingyong@wanshare.com
# @Time    : 18-11-12 下午8:05
import time
import string
import pytest
import random
import requests
from faker import Faker
from enum import IntEnum
from pprint import pprint
from decimal import Decimal
from datetime import datetime
from test.tenant.main import Faucet
from common.utils import PlatformManager
from common.account_sign import get_sponsor_token
from dateutil.relativedelta import relativedelta
from swagger_client.tenant.rest import ApiException
from swagger_client.staff.api.audit_api import AuditApi
from common.certification_verify import individual_verify
from swagger_client.tenant.api.project_api import ProjectApi
from swagger_client.tenant.api.account_api import AccountApi
from swagger_client.sponsor.api.sponsor_api import SponsorApi
from swagger_client.tenant.api.contacts_api import ContactsApi
from swagger_client.staff.api.system_management_api import SystemManagementApi
from swagger_client.tenant.api.verification_api import VerificationApi
from swagger_client.staff.api.asset_management_api import AssetManagementApi
from swagger_client.venture.api.account_api import AccountApi as VentureAccountApi
from swagger_client.venture.models.post_plat_form_register_request import PostPlatFormRegisterRequest
from swagger_client.venture.api.project_api import ProjectApi as VentureApi
from swagger_client.tenant.api.asset_management_api import AssetManagementApi as TenantAssetManagementApi
from swagger_client.tenant.api.contacts_api import ContactsApi as TenantContactsApi
from swagger_client.sponsor.api.sponsors_project_api import SponsorsProjectApi
from swagger_client.staff.api.system_management_api import SystemManagementApi
from swagger_client.venture.api.contacts_api import ContactsApi as VentureContactsApi
from swagger_client.venture.api.project_management_api import ProjectManagementApi
from swagger_client.tenant.api.market_management_api import MarketManagementApi
from swagger_client.staff.models.post_sponsor_request import PostSponsorRequest
from swagger_client.staff.models.put_system_coins_init_request import PutSystemCoinsInitRequest
from swagger_client.venture.models.put_project_request import PutProjectRequest
from swagger_client.venture.models.application_request import ApplicationRequest
from swagger_client.main.api.favorite_management_api import FavoriteManagementApi
from swagger_client.main.api import ExchangeApi as MainExchangeApi
from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from swagger_client.staff.api.project_api import ProjectApi as StaffProjectApi
from swagger_client.staff.api.system_management_api import SystemManagementApi
from common.account_sign import register_with_login, get_admin_token, set_login_status
from swagger_client.tenant.models.put_order_market_request import PutOrderMarketRequest
from swagger_client.staff.models.put_system_config_request import PutSystemConfigRequest
from swagger_client.tenant.models.post_order_market_request import PostOrderMarketRequest
from swagger_client.tenant.models.post_market_close_request import PostMarketCloseRequest
from swagger_client.venture.models.put_project_request_setting import PutProjectRequestSetting
from swagger_client.venture.models.put_project_request_project_info import PutProjectRequestProjectInfo
from swagger_client.venture.models.put_project_request_communities import PutProjectRequestCommunities
from swagger_client.tenant.models.post_order_market_renew_request import PostOrderMarketRenewRequest
from swagger_client.venture.models.put_project_request_project_info import PutProjectRequestProjectInfo  # noqa: F401,E501
from swagger_client.staff.models.post_shutdown_market_audit_request import PostShutdownMarketAuditRequest
from swagger_client.main.models.post_favoriter_market_request import PostFavoriterMarketRequest
from swagger_client.main.api.market_api import MarketApi
from swagger_client.staff.models.post_tenant_audit_request import PostTenantAuditRequest
from swagger_client.staff.models.post_tenant_re_audit_request import PostTenantReAuditRequest
from common.utils import PlatformManager, random_get_country_code, random_get_country_ob, get_random_id_number
from swagger_client.staff.models.post_shutdown_market_re_audit_request import PostShutdownMarketReAuditRequest
from .test_exchange_management import Exchange, verify_info


class AllottedTime(IntEnum):
    _6month = 6
    _12month = 12


DEFAULT_VERIFY_CODE = "666666"


def get_token(token):
    return 'Bearer ' + token


def get_random_coin_full_name():
    res = random.sample(string.ascii_uppercase, 6)
    return ''.join(res)


def get_random_coin_short_name():
    res = random.sample(string.ascii_uppercase, 6)
    return ''.join(res)


def free_charge(token, coin_id, account_id):
    headers = {"Authorization": f"Bearer {token}"}
    # url = f'http://crush-main.crush-deploy.lan/api/asset-test/asset-initialize/{account_id}/{coin_id}'
    url = f"http://crush-tenant.s1.c58c7e25a004943cdad05a1bf31f354b7.cn-shenzhen.alicontainer.com/asset-test/asset-initialize/{coin_id}/1000000000000"
    requests.post(url, headers=headers)
    requests.post(url, headers=headers)
    requests.post(url, headers=headers)


def get_project(token):
    v_api = VentureApi()
    set_login_status(v_api, token)
    today = datetime.today().date()
    while True:
        project_name = "project" + str(random.randint(1, 10000))
        rv = v_api.applications_check_project_name_post(project_name)
        if not rv.result:
            break
    return {
        "projectName": project_name,
        "description": "XXXXXXXXXXXXXXXX",
        "officialWebsite": "www.xxxx.com",
        "whitePaperKey": "url/pdf123455",
        "areaCode": "+86",
        "projectPosterKey": 'f210c0d8a4e747cb8438031fe2b99931',
        "cellphone": "13510022445",
        "telephone": 12874846,
        "email": "1234832456@qq.com",
        "fullName": get_random_coin_full_name(),
        "shortName": get_random_coin_short_name(),
        "issuePrice": "2.24545",
        "issuedVolume": "1000000",
        "circulationVolume": "1000000",
        "issuedDate": str(today),
        "coinLogoKey": 'f210c0d8a4e747cb8438031fe2b99931',
        "blockchainType": "public_chain",
        "dataLink": "www.baidu.com",
        "blockBrowser": "www.baidu.com"
    }
    # return dict(
    #     project_name=project_name,
    #     description="hell of a project",
    #     official_website="http://showmethemoney.com",
    #     white_paper="http://showmethemoney.com/whitepaper",
    #     area_code="+86",
    #     project_poster_key="http://showmethemoney.com/poster",
    #     cellphone="13510022445",
    #     telephone="12874846",
    #     email="helloboy@icloud.com",
    #     full_name=get_random_coin_full_name(),
    #     short_name=get_random_coin_short_name(),
    #     issue_price="100",
    #     issued_volume="15",
    #     circulation_volume="13",
    #     issued_date=str(today),
    #     coin_logo_key="http://showmethemoney.com/coin_logo",
    #     blockchain_type="public_chain",
    #     data_link="link me baby",
    #     block_browser="browser what"
    # )


def get_sponsors():
    """获取保鉴机构"""
    admin_token = get_admin_token()
    s_api = SponsorsManagermentApi()
    set_login_status(s_api, admin_token)
    name = 'sponsors_name_' + str(random.randint(1, 100000))
    email = str(random.randint(100000, 50000000)) + '@qq.com'
    data = dict(
        account='s' + str(int(time.time())),
        name=name,
        password='123456789',
        phone='15526548799',
        email=email
    )
    req = PostSponsorRequest(**data)
    s_api.staff_sponsors_post(req)
    # 获取保健方id
    rv = s_api.staff_sponsors_get(page=1, name=name, email=email)
    sponsors_id = rv.items[0].id
    data['id'] = sponsors_id
    return data


def get_verify_token():
    """获取二次验证"""


class TestMarket1(object):
    """1.后台配置交易服务费率——获取交易服务费率——获取交易对市场列表——配置交易对市场——验证交易对是否存在——获取交易对市场"""
    data = {}
    service_rate = '0.00001'
    fee_rate = 0.0001

    @pytest.mark.order1
    def test_service_rate(self):
        s_api = SystemManagementApi()
        admin_token = get_admin_token()
        set_login_status(s_api, admin_token)
        # 获取服务费率
        rv = s_api.system_system_config_get()
        config_id = ''
        for each in rv:
            if each['configKey'] == 'SERVICE_RATE':
                config_id = each['id']
        # 设置服务费率
        res = PutSystemConfigRequest()
        res.config_value = TestMarket1.service_rate
        s_api.system_system_config_id_put(config_id, res)
        # 获取服务费率
        rv = s_api.system_system_config_get()
        flag = False
        for each in rv:
            if each['configKey'] == 'SERVICE_RATE':
                flag = True
                assert each['configValue'] == TestMarket1.service_rate
        assert flag

    @pytest.mark.order2
    def test_coin_market(self, with_login):
        manager = PlatformManager('tenant')
        m_api = MarketManagementApi()
        e_api = ExchangeManagementApi()
        api = manager.account_api
        verify_api = manager.verify_api
        account_api = AccountApi()
        user = register_with_login('tenant',
                                   with_login,
                                   [api, verify_api, m_api, e_api, account_api])
        self.data['user'] = user
        token = user['token']
        email = user.get('email')
        # 绑定电话
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        exchange_api = ExchangeManagementApi()
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        e_api.exchange_post(exchange)
        # 获取交易对市场列表
        try:
            m_api.markets_get()
        except ApiException as e:
            # 交易所不存在
            assert e.status == 400
        else:
            assert False, '市场应当不存在.'
        # 初审复审
        rv = account_api.accounts_account_info_get()
        account_id = rv.account_info.account_id
        self.data['account_id'] = account_id
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
        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='approved')
        audit_api.tenant_audits_re_audit_post(res)
        rv = e_api.exchange_exchange_id_get()
        exchange_id = rv.id
        self.data['exchange_id'] = exchange_id

    @pytest.mark.order3
    def test_add_market1(self, with_login):
        user = self.data['user']
        email, password = user['email'], user['password']
        m_api = MarketManagementApi()
        e_api = ExchangeManagementApi()
        s_api = SponsorApi()
        venture_api = VentureApi()
        va_api = VentureAccountApi()
        project_api = ProjectApi()
        contacts_api = ContactsApi()
        tam_api = TenantAssetManagementApi()
        v_api = VerificationApi()
        ma_api = MainExchangeApi()
        vc = VentureContactsApi()
        pm = ProjectManagementApi()
        token = with_login('tenant',
                           [pm, vc, ma_api, v_api, contacts_api, project_api, m_api, e_api, va_api, s_api, venture_api, tam_api],
                           email, password)
        # 授权
        res = PostPlatFormRegisterRequest()
        va_api.create_platform(body=res)
        # 交易币种
        rv = e_api.exchange_exchange_coin_get()
        seller_coin = rv.seller_coin
        buyer_coin = rv.buyer_coin
        b_coin = buyer_coin[0]
        if seller_coin:
            s_coin = seller_coin[0]
        else:
            sponsor = get_sponsors()
            # 登录保健方
            account, password = sponsor['account'], sponsor['password']
            sponsor_api = SponsorApi()
            sponsor_token = get_sponsor_token(account, password, email='test')
            set_login_status(sponsor_api, sponsor_token)
            project = get_project(token)
            # req = ApplicationRequest(**project)
            rv = venture_api.applications_post(body=project)
            application_id = rv.id

            # 查看申请列表
            rv = venture_api.applications_get(page=1)
            assert len(rv.items) == 1
            item = rv.items[0]
            assert item.project_name == project['projectName']
            assert item.fullname == project['fullName']
            assert item.short_name == project['shortName']
            rv = venture_api.applications_num_get(status='under_review')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='passed')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='undone')
            assert int(rv.result) == 1
            # 设置保健机构
            venture_api.applications_id_set_sponsor_put(
                application_id, {'sponsorId': sponsor['id']}
            )
            rv = venture_api.applications_num_get(status='undone')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='under_review')
            assert int(rv.result) == 1
            rv = venture_api.applications_num_get(status='passed')
            assert int(rv.result) == 0
            project_name = project['projectName']
            sponsor_project_api = SponsorsProjectApi()
            set_login_status(sponsor_project_api, sponsor_token)
            rv = sponsor_project_api.projects_get(page=1,
                                                  project_name=project_name)
            assert len(rv.items) >= 1
            rv = sponsor_project_api.projects_id_get(id=application_id)
            assert rv
            # 保健不通过
            sponsor_project_api.projects_sponsor_put({
                'id': application_id, 'status': 0, 'remark': 'test'}
            )
            rv = venture_api.applications_num_get(status='undone')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='under_review')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='passed')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='turn_down')
            assert int(rv.result) == 1

            # 保鉴成功列表
            rv = sponsor_project_api.sponsor_record_success_get(
                page=1, coin_name=project['shortName']
            )
            assert not rv.items
            # 项目列表
            rv = venture_api.projects_get(page=1)
            assert len(rv.items) == 0

    @pytest.mark.order4
    def test_add_market2(self, with_login):
        user = self.data['user']
        email, password = user['email'], user['password']
        m_api = MarketManagementApi()
        e_api = ExchangeManagementApi()
        s_api = SponsorApi()
        venture_api = VentureApi()
        va_api = VentureAccountApi()
        project_api = ProjectApi()
        contacts_api = ContactsApi()
        tam_api = TenantAssetManagementApi()
        v_api = VerificationApi()
        ma_api = MainExchangeApi()
        vc = VentureContactsApi()
        pm = ProjectManagementApi()
        tenant_ca = TenantContactsApi()
        token = with_login('tenant',
                           [pm, vc, ma_api, v_api, contacts_api, project_api,
                            m_api, e_api, va_api, s_api, venture_api, tam_api,
                            tenant_ca], email, password)
        # 交易币种
        rv = e_api.exchange_exchange_coin_get()
        seller_coin = rv.seller_coin
        buyer_coin = rv.buyer_coin
        b_coin = buyer_coin[0]
        if seller_coin:
            s_coin = seller_coin[0]
        else:
            sponsor = get_sponsors()
            # 登录保健方
            account, password = sponsor['account'], sponsor['password']
            sponsor_api = SponsorApi()
            sponsor_token = get_sponsor_token(account, password, email='test')
            set_login_status(sponsor_api, sponsor_token)
            project = get_project(token)
            # req = ApplicationRequest(**project)
            rv = venture_api.applications_post(body=project)
            application_id = rv.id

            # 查看申请列表
            rv = venture_api.applications_get(page=1, order='desc')
            assert len(rv.items) == 2
            item = rv.items[0]
            assert item.project_name == project['projectName']
            assert item.fullname == project['fullName']
            assert item.short_name == project['shortName']
            rv = venture_api.applications_num_get(status='under_review')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='passed')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='undone')
            assert int(rv.result) == 1
            # 设置保健机构
            venture_api.applications_id_set_sponsor_put(
                application_id, {'sponsorId': sponsor['id']}
            )
            rv = venture_api.applications_num_get(status='undone')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='under_review')
            assert int(rv.result) == 1
            rv = venture_api.applications_num_get(status='passed')
            assert int(rv.result) == 0
            project_name = project['projectName']
            sponsor_project_api = SponsorsProjectApi()
            set_login_status(sponsor_project_api, sponsor_token)
            rv = sponsor_project_api.projects_get(page=1,
                                                  project_name=project_name)
            assert len(rv.items) >= 1
            rv = sponsor_project_api.projects_id_get(id=application_id)
            assert rv
            sponsor_project_api.projects_sponsor_put({
                'id': application_id, 'status': 1, 'remark': 'test'}
            )
            rv = venture_api.applications_num_get(status='undone')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='under_review')
            assert int(rv.result) == 0
            rv = venture_api.applications_num_get(status='passed')
            assert int(rv.result) == 1
            rv = venture_api.applications_num_get(status='turn_down')
            assert int(rv.result) == 1
            # 保鉴成功列表
            rv = sponsor_project_api.sponsor_record_success_get(
                page=1, coin_name=project['shortName']
            )
            # 项目列表
            rv = venture_api.projects_get(page=1)
            project_id = rv.items[0].project_id
            self.data['project_id'] = project_id
            # 设置接入方式
            setting = PutProjectRequestSetting(access_method='accept', open=True)
            req = PutProjectRequest()
            req.setting = setting
            venture_api.projects_id_put(project_id, 'setting', req)
            # 获取项目详情
            rv = venture_api.projects_id_get(project_id)
            exchange_id = TestMarket1.data['exchange_id']
            rv = project_api.projects_get(coin_name=project['shortName'])
            assert len(rv.items) == 0
            # 初始化项目
            s_api = SystemManagementApi()
            staff_project_api = StaffProjectApi()
            asset_management_api = AssetManagementApi()
            admin_token = get_admin_token()
            set_login_status(staff_project_api, admin_token)
            set_login_status(asset_management_api, admin_token)
            set_login_status(s_api, admin_token)
            coin_name = project['shortName']
            rv = asset_management_api.asset_mgmt_coins_get(coin_name=coin_name)
            coin_id = rv.items[0].coin_id
            coin_config_id = rv.items[0].id
            # 修改币种配置
            res = PutSystemCoinsInitRequest()
            res.usdt_price = '1251'
            res.rc_times = 8
            res.wc_times = 8
            res.withdraw_rate = 0.1
            res.min_withdraw = 100
            res.min_withdraw_fee = 0.1
            res.max_withdraw = 1000
            res.min_recharge = 10
            res.address_tag_switch = True
            res.day_withdraw_total = 125564
            res.address_type = 'OX'
            res.address_url = 'http://unknown.com'
            res.txid_url = 'http://unknown.com'
            # asset_management_api.asset_mgmt_coins_id_put(coin_id, res)
            asset_management_api.asset_mgmt_coins_id_init_put(coin_config_id, res)

            rv = project_api.projects_get(coin_name=project['shortName'])
            assert len(rv.items) == 1
            setting = PutProjectRequestSetting(access_method='refuse', open=True)
            req = PutProjectRequest()
            req.setting = setting
            venture_api.projects_id_put(project_id, 'setting', req)  # refuse
            rv = project_api.projects_get(coin_name=project['shortName'])
            assert len(rv.items) == 0
            setting = PutProjectRequestSetting(access_method='verification', open=True)
            req = PutProjectRequest()
            req.setting = setting
            venture_api.projects_id_put(project_id, 'setting', req)
            rv = project_api.projects_get(coin_name=project['shortName'])
            assert len(rv.items) == 1
            rv = s_api.system_trading_pair_get(name=project['shortName'],
                                               partition_id=b_coin.id)
            # 对接币种
            req = {
                'exchangeId': exchange_id,
                'projectId': project_id,
                'sponsor': 'tenant'
            }
            contacts_api.contacts_post(req)
            rv = pm.projects_id_exchanges_get(project_id)
            rv = pm.projects_id_contacts_get(project_id, 'tenant')
            assert rv.items[0].exchange_id == exchange_id
            rv1 = contacts_api.contacts_check_get(
                project_id=project_id, exchange_id=exchange_id
            )
            assert rv1.result
            r1 = contacts_api.contacts_project_id_status_get(project_id)
            assert r1.status == 'pending'
            # 处理对接邀请
            contact_id = rv.items[0].contact_id
            r = tenant_ca.contacts_projects_exchange_id_get(exchange_id,
                                                            'pending')
            assert not r.items
            vc.contacts_put({
                'contactId': contact_id,
                'status': 'accepted'
            })
            rv = contacts_api.contacts_check_get(
                project_id=project_id, exchange_id=exchange_id
            )
            assert rv.result
            rv = contacts_api.contacts_project_id_status_get(project_id)
            assert rv.status == 'accepted'
            rv = e_api.exchange_exchange_coin_get()
            seller_coin = rv.seller_coin
            s_coin = seller_coin[0]

            # 主平台获取买卖方币种列表
            rv = ma_api.exchanges_exchange_coin_exchange_id_get(exchange_id)
            assert rv.seller_coin[0].name == project['shortName']
        self.data['s_coin'] = s_coin
        self.data['b_coin'] = b_coin
        res = PostOrderMarketRequest()
        res.seller_coin_id = s_coin.id
        res.buyer_coin_id = b_coin.id
        res.allotted_time = AllottedTime._6month
        res.fee_rate = TestMarket1.fee_rate
        now = datetime.now()
        disabled_at = now + relativedelta(months=AllottedTime._6month)
        rv = e_api.exchange_exchange_coin_get()
        # 配置交易对市场
        rv = e_api.exchange_order_market_post(res)
        order_id = rv.order_id
        usdt_id = b_coin.id
        data = {
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:hello.world@email.com",
            "code": "666666",
            "secondCode": "Ls1w1w",
            "type": "pay"
        }
        rv = v_api.accounts_verify_post(data)
        p = PutOrderMarketRequest(order_id=order_id, token=rv.token)
        # try:
        #     e_api.exchange_order_market_put(p)
        # except Exception as e:
        #     assert e.status == 409  # todo 暂时跳过
        # else:
        #     assert False, '没钱，不应该支付成功'
#
    @pytest.mark.order5
    def test_market_exchange(self, with_login):
        """添加测试用例，两个交易所对接同一个市场，手动在数据库中修改两者为深度共享"""
        manager = PlatformManager('tenant')
        m_api = MarketManagementApi()
        e_api = ExchangeManagementApi()
        api = manager.account_api
        verify_api = manager.verify_api
        account_api = AccountApi()
        v_api = VerificationApi()
        pm = ProjectManagementApi()
        vc = VentureContactsApi()
        user = register_with_login('tenant',
                                   with_login,
                                   [vc, pm, api, v_api, verify_api, m_api, e_api, account_api])
        self.data['user1'] = user
        token0 = user['token']
        email = user.get('email')
        # 绑定电话
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token0)
        exchange_api = ExchangeManagementApi()
        e = Exchange(exchange_api, token0)
        exchange = e.get_exchange()
        e_api.exchange_post(exchange)
        rv = account_api.accounts_account_info_get()
        account_id = rv.account_info.account_id
        audit_api = AuditApi()
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        rv = audit_api.tenant_audits_get(uid=account_id,
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
        rv = e_api.exchange_exchange_id_get()
        exchange_id = rv.id
        # 对接币种
        contacts_api = ContactsApi()
        user = self.data['user']
        email, password = user['email'], user['password']
        token = with_login('tenant', [contacts_api], email, password)
        project_id = self.data['project_id']
        req = {
            'exchangeId': exchange_id,
            'projectId': project_id,
            'sponsor': 'tenant'
        }

        rv = contacts_api.contacts_post(req)
        # 处理对接邀请
        rv = pm.projects_id_contacts_get(project_id, 'tenant')
        # 处理对接邀请
        contact_id = rv.items[0].contact_id
        vc.contacts_put({
            'contactId': contact_id,
            'status': 'accepted'
        })
        rv = contacts_api.contacts_check_get(
            project_id=project_id, exchange_id=exchange_id
        )
        assert rv.result
        rv = e_api.exchange_exchange_coin_get()
        res = PostOrderMarketRequest()
        s_coin = self.data['s_coin']
        b_coin = self.data['b_coin']
        res.seller_coin_id = s_coin.id
        res.buyer_coin_id = b_coin.id
        res.allotted_time = AllottedTime._6month
        res.fee_rate = TestMarket1.fee_rate
        rv = e_api.exchange_exchange_coin_get()
        # 配置交易对市场
        rv = e_api.exchange_order_market_post(res)
        order_id = rv.order_id
        usdt_id = b_coin.id
        # 充钱
        free_charge(token0, usdt_id, account_id)

        data = {
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:hello.world@email.com",
            "code": "666666",
            "secondCode": "Ls1w1w",
            "type": "pay"
        }
        rv = v_api.accounts_verify_post(data)
        p = PutOrderMarketRequest(order_id=order_id, token=rv.token)
        e_api.exchange_order_market_put(p)
        # 获取交易对市场
        rv = m_api.markets_get()
        items = rv.items
        assert len(items) == 1

    @pytest.mark.order10
    def test_close_market(self, with_login):
        """7.新增市场——获取交易对市场列表——关闭市场——获取交易对市场"""
        a_api = AccountApi()
        audit_api = AuditApi()
        v_api = VerificationApi()
        m_api = MarketManagementApi()
        e_api = ExchangeManagementApi()
        user = self.data['user1']
        email, password = user['email'], user['password']
        token = with_login('tenant', [a_api, m_api, v_api, e_api], email, password)
        rv = m_api.markets_get()
        market_id = rv.items[0].id
        res = PostMarketCloseRequest(id=market_id, closing_reason='a'*11)
        data = {
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:hello.world@email.com",
            "code": "666666",
            "secondCode": "Ls1w1w",
            "type": "close_market"
        }
        rv = v_api.accounts_verify_post(data)
        res.token = rv.token
        rv = m_api.markets_close_post(res)
        res = m_api.markets_get()
        item = res.items[0]
        assert item.status == 'in_review'
        # 合并测试用例
        """11.前台申请关闭交易市场——关闭交易所市场审核列表——关闭交易所市场审核详情初审
        ——提交关闭交易所审核初审——关闭交易所市场审核列表"""
        # 审核列表
        rv = e_api.exchange_exchange_id_get()
        exchange_id = rv.id
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        rv = audit_api.shutdown_market_audits_get(page=1,
                                                  exchange_id=exchange_id)
        item = rv.items[0]
        status = item.status
        assert status == 'audit'
        ticket_number = item.ticket_number
        rv = audit_api.shutdown_market_audits_id_tasks_audit_get(ticket_number)
        account_info = a_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        assert rv.uid == account_id
        assert rv.exchange_id == exchange_id
        s = self.data['s_coin'].name
        b = self.data['b_coin'].name
        assert rv.trading_pair == f'{s}/{b}'
        # 初审
        data = PostShutdownMarketAuditRequest(id=ticket_number,
                                              status='disapproved')
        audit_api.shutdown_market_audits_audit_post(data)
        res = m_api.markets_get()
        item = res.items[0]
        assert item.status == 'running'
        # 获取初审详情
        rv = audit_api.shutdown_market_audits_id_audit_get(ticket_number)
        pprint(rv)
        assert rv.audit_status == 'disapproved'
        rv = audit_api.shutdown_market_audits_get(exchange_id=exchange_id)
        item = rv.items[0]
        assert item.status == 'audit_return'
        # 复审
        data = PostShutdownMarketReAuditRequest(id=ticket_number,
                                                status='approved')
        try:
            audit_api.shutdown_market_audits_re_audit_post(data)
        except Exception as e:
            assert e.status == 400
        else:
            assert False, '初审未过，不应该复审'

    @pytest.mark.order11
    def test_close_market(self, with_login):
        """7.新增市场——获取交易对市场列表——关闭市场——获取交易对市场"""
        a_api = AccountApi()
        audit_api = AuditApi()
        v_api = VerificationApi()
        m_api = MarketManagementApi()
        e_api = ExchangeManagementApi()
        user = self.data['user1']
        email, password = user['email'], user['password']
        token = with_login('tenant', [a_api, m_api, v_api, e_api], email, password)
        rv = m_api.markets_get()
        market_id = rv.items[0].id
        res = PostMarketCloseRequest(id=market_id, closing_reason='a'*11)
        data = {
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "048ebbe51f829995db76ac4b81546403",
            "validate": "true",
            "account": "mailto:hello.world@email.com",
            "code": "666666",
            "secondCode": "Ls1w1w",
            "type": "close_market"
        }
        rv = v_api.accounts_verify_post(data)
        res.token = rv.token
        rv = m_api.markets_close_post(res)
        res = m_api.markets_get()
        assert res.items[0].status == 'in_review'
        try:
            rv = m_api.markets_close_post(res)
        except Exception as e:
            assert e.status == 400
        else:
            assert False, '审核流程中，不应该再次提交关闭请求'
        # 合并测试用例
        """11.前台申请关闭交易市场——关闭交易所市场审核列表——关闭交易所市场审核详情初审
        ——提交关闭交易所审核初审——关闭交易所市场审核列表"""
        # 审核列表
        rv = e_api.exchange_exchange_id_get()
        exchange_id = rv.id
        admin_token = get_admin_token()
        set_login_status(audit_api, admin_token)
        rv = audit_api.shutdown_market_audits_get(page=1,
                                                  exchange_id=exchange_id)
        item = rv.items[0]
        status = item.status
        assert status == 'audit'
        ticket_number = item.ticket_number
        rv = audit_api.shutdown_market_audits_id_tasks_audit_get(ticket_number)
        account_info = a_api.accounts_account_info_get()
        account_id = account_info.account_info.account_id
        assert rv.uid == account_id
        assert rv.exchange_id == exchange_id
        s = self.data['s_coin'].name
        b = self.data['b_coin'].name
        assert rv.trading_pair == f'{s}/{b}'
        # 初审
        data = PostShutdownMarketAuditRequest(id=ticket_number,
                                              status='approved')
        audit_api.shutdown_market_audits_audit_post(data)
        res = m_api.markets_get()
        item = res.items[0]
        assert item.status == 'in_review'
        # 获取初审详情
        rv = audit_api.shutdown_market_audits_id_audit_get(ticket_number)
        assert rv.audit_status == 'approved'
        rv = audit_api.shutdown_market_audits_get(exchange_id=exchange_id)
        item = rv.items[0]
        assert item.status == 're_audit'
        # 合并测试用例
        """12.申请关闭交易所市场初审通过——关闭交易所市场审核列表
        ——提交关闭交易所审核复审——关闭交易所市场审核列表"""
        rv = audit_api.shutdown_market_audits_id_tasks_re_audit_get(
            id=ticket_number
        )
        assert rv.audit_status == 'approved'
        # 复审
        data = PostShutdownMarketReAuditRequest(id=ticket_number,
                                                status='disapproved')
        audit_api.shutdown_market_audits_re_audit_post(data)
        # 复审详情
        rv = audit_api.shutdown_market_audits_id_re_audit_get(ticket_number)
        assert rv.audit_status == 'approved'
        assert rv.re_status == 'disapproved'
        rv = audit_api.shutdown_market_audits_get(exchange_id=exchange_id)
        item = rv.items[0]
        assert item.status == 're_audit_return'
        res = m_api.markets_get()
        item = res.items[0]
        assert item.status == 'running'

    @pytest.mark.order11
    def test_open_market(self, with_login):
        """8.新增市场——获取交易对市场列表——开启市场——获取交易对市场"""
        m_api = MarketManagementApi()
        user = self.data['user1']
        email, password = user['email'], user['password']
        token = with_login('tenant', [m_api], email, password)
        rv = m_api.markets_get()
        market_id = rv.items[0].id
        try:
            m_api.markets_id_open_put(id=market_id)
        except Exception as e:
            assert e.status == 400
        else:
            assert False, '市场running状态，不应该申请open'


class TestProject(object):
    """一个项目方创建多个项目"""
    data = {}

    @pytest.mark.order1
    def test_register(self, with_login):
        manager = PlatformManager('tenant')
        m_api = MarketManagementApi()
        e_api = ExchangeManagementApi()
        api = manager.account_api
        verify_api = manager.verify_api
        account_api = AccountApi()
        venture_api = VentureApi()
        va_api = VentureAccountApi()
        contacts_api = ContactsApi()
        vc = VentureContactsApi()
        pm = ProjectManagementApi()
        user = register_with_login('tenant',
                                   with_login,
                                   [api, verify_api, m_api, e_api, account_api,
                                    venture_api, va_api, contacts_api, pm, vc])
        token = user['token']
        email = user.get('email')
        self.data['token1'] = token
        # 绑定电话
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        # 授权
        res = PostPlatFormRegisterRequest()
        va_api.create_platform(body=res)
        # 申请项目
        project1 = get_project(token)
        rv = venture_api.applications_post(body=project1)
        application_id_1 = rv.id
        sponsor = get_sponsors()
        # 登录保健方
        account, password = sponsor['account'], sponsor['password']
        sponsor_token = get_sponsor_token(account, password, email='test')
        project2 = get_project(token)
        # req = ApplicationRequest(**project)
        rv = venture_api.applications_post(body=project2)
        application_id_2 = rv.id
        rv = venture_api.projects_get(page=1)
        assert len(rv.items) == 0
        rv = venture_api.applications_get(page=1)
        assert len(rv.items) == 2
        # 设置保健机构
        venture_api.applications_id_set_sponsor_put(
            application_id_1, {'sponsorId': sponsor['id']}
        )
        venture_api.applications_id_set_sponsor_put(
            application_id_2, {'sponsorId': sponsor['id']}
        )
        sponsor_project_api = SponsorsProjectApi()
        set_login_status(sponsor_project_api, sponsor_token)

        sponsor_project_api.projects_sponsor_put({
            'id': application_id_1, 'status': 1, 'remark': 'test'}
        )
        sponsor_project_api.projects_sponsor_put({
            'id': application_id_2, 'status': 1, 'remark': 'test'}
        )
        rv = venture_api.projects_get(page=1)
        project_id1 = rv.items[1].project_id
        project_id2 = rv.items[0].project_id
        self.data['project_id1'] = project_id1
        self.data['project_id2'] = project_id2
        # 设置接入方式
        setting = PutProjectRequestSetting(access_method='verification', open=True)
        req = PutProjectRequest()
        req.setting = setting
        venture_api.projects_id_put(project_id1, 'setting', req)
        venture_api.projects_id_put(project_id2, 'setting', req)
        # 获取项目详情
        # 初始化项目
        s_api = SystemManagementApi()
        staff_project_api = StaffProjectApi()
        asset_management_api = AssetManagementApi()
        admin_token = get_admin_token()
        set_login_status(staff_project_api, admin_token)
        set_login_status(asset_management_api, admin_token)
        set_login_status(s_api, admin_token)
        coin_name1 = project1['shortName']
        rv = asset_management_api.asset_mgmt_coins_get(coin_name=coin_name1)
        coin_config_id1 = rv.items[0].id
        coin_name2 = project2['shortName']
        rv = asset_management_api.asset_mgmt_coins_get(coin_name=coin_name2)
        coin_config_id2 = rv.items[0].id
        # 修改币种配置
        res = PutSystemCoinsInitRequest()
        res.usdt_price = '1251'
        res.rc_times = 8
        res.wc_times = 8
        res.withdraw_rate = 0.1
        res.min_withdraw = 100
        res.min_withdraw_fee = 0.1
        res.max_withdraw = 1000
        res.min_recharge = 10
        res.address_tag_switch = True
        res.day_withdraw_total = 125564
        res.address_type = 'OX'
        res.address_url = 'http://unknown.com'
        res.txid_url = 'http://unknown.com'
        asset_management_api.asset_mgmt_coins_id_init_put(coin_config_id1, res)
        asset_management_api.asset_mgmt_coins_id_init_put(coin_config_id2, res)

    @pytest.mark.order2
    def test_coin_market(self, with_login):
        manager = PlatformManager('tenant')
        m_api = MarketManagementApi()
        e_api = ExchangeManagementApi()
        api = manager.account_api
        verify_api = manager.verify_api
        account_api = AccountApi()
        contacts_api = ContactsApi()
        vc = VentureContactsApi()
        venture_pm = ProjectManagementApi()
        tenant_ca = TenantContactsApi()
        user = register_with_login('tenant',
                                   with_login,
                                   [api, verify_api, m_api, e_api, account_api,
                                    contacts_api, vc, venture_pm, tenant_ca])
        self.data['user2'] = user
        token = user['token']
        email = user.get('email')
        # 绑定电话
        faker = Faker('zh_CN')
        phone = faker.phone_number()
        verify = verify_info(manager, email, "bind_phone")
        manager.bind_phone(phone, DEFAULT_VERIFY_CODE,
                           area_code="+86", token=verify.token)
        id_number = get_random_id_number()
        individual_verify('tenant', id_number, token)
        exchange_api = ExchangeManagementApi()
        e = Exchange(exchange_api, token)
        exchange = e.get_exchange()
        e_api.exchange_post(exchange)
        # 获取交易对市场列表
        try:
            m_api.markets_get()
        except ApiException as e:
            # 交易所不存在
            assert e.status == 400
        else:
            assert False, '市场应当不存在'
        # 初审复审
        rv = account_api.accounts_account_info_get()
        account_id = rv.account_info.account_id
        self.data['account_id'] = account_id
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
        # 复审
        res = PostTenantReAuditRequest(id=task_id,
                                       status='approved')
        audit_api.tenant_audits_re_audit_post(res)
        rv = e_api.exchange_exchange_id_get()
        exchange_id = rv.id
        self.data['exchange_id'] = exchange_id
        rv = e_api.exchange_exchange_coin_get()
        seller_coin = rv.seller_coin
        buyer_coin = rv.buyer_coin
        b_coin = buyer_coin[0]
        if seller_coin:
            s_coin = seller_coin[0]
        else:
            # 对接币种
            # 租户主动发起对接
            project_id1 = self.data['project_id1']
            project_id2 = self.data['project_id2']
            req = {
                'exchangeId': exchange_id,
                'projectId': project_id1,
                'sponsor': 'tenant'
            }
            contacts_api.contacts_post(req)
            # 项目方主动发起对接
            req = {
                'exchangeId': exchange_id,
                'projectId': project_id2,
                'sponsor': 'venture'
            }
            vc.contacts_post(req)
            rv1 = venture_pm.projects_id_contacts_get(project_id1, 'tenant')
            rv2 = tenant_ca.contacts_projects_exchange_id_get(exchange_id, 'pending')
            # 处理对接邀请
            contact_id1 = rv1.items[0].contact_id
            contact_id2 = rv2.items[0].id
            vc.contacts_put({
                'contactId': contact_id1,
                'status': 'accepted'
            })
            rv = contacts_api.contacts_check_get(
                project_id=project_id1, exchange_id=exchange_id
            )
            # pprint(rv)
            contacts_api.contacts_put({
                'contactId': contact_id2,
                'status': 'accepted'
            })
            rv = vc.contacts_check_get(project_id2, exchange_id)
            rv = contacts_api.contacts_check_get(project_id1, exchange_id)
            assert rv.result
            rv = contacts_api.contacts_project_id_status_get(project_id1)
            assert rv.status == 'accepted'
            rv = contacts_api.contacts_project_id_status_get(project_id2)
            assert rv.status == 'accepted'
