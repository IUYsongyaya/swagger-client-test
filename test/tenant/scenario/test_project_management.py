# @Author  : ymy
# @Email   : yaomingyong@wanshare.com
# @Time    : 18-11-19 下午3:44

import pytest
import random
import datetime
from enum import IntEnum
from .test_pager import Pager
from datetime import datetime
from common.utils import PlatformManager
from .test_exchange_management import new_exchange
from swagger_client.tenant.api import DashboardApi
from common.account_sign import register_with_login
from swagger_client.staff.api.audit_api import AuditApi
from swagger_client.tenant.api.account_api import AccountApi
from swagger_client.tenant.api.project_api import ProjectApi
from swagger_client.tenant.api.contacts_api import ContactsApi
from swagger_client.venture.api.project_api import ProjectApi as VentureApi
from swagger_client.main.models.post_favoriter_request import PostFavoriterRequest
from swagger_client.main.api.favorite_management_api import FavoriteManagementApi
from swagger_client.sponsor.api.sponsors_project_api import SponsorsProjectApi
from swagger_client.staff.api.system_management_api import SystemManagementApi
from swagger_client.venture.models.put_project_request import PutProjectRequest
from swagger_client.tenant.api.market_management_api import MarketManagementApi
from swagger_client.venture.models.application_request import ApplicationRequest
from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from swagger_client.staff.models.put_system_coins_request import PutSystemCoinsRequest
from swagger_client.main.models.delete_favoriter_request import DeleteFavoriterRequest
from swagger_client.staff.models.post_tenant_re_audit_request import PostTenantReAuditRequest
from swagger_client.staff.models.post_tenant_audit_request import PostTenantAuditRequest
from swagger_client.tenant.models.put_order_market_request import PutOrderMarketRequest
from swagger_client.tenant.models.post_order_market_request import PostOrderMarketRequest
from swagger_client.venture.models.put_project_request_setting import PutProjectRequestSetting
from swagger_client.venture.models.put_project_request_project_info import PutProjectRequestProjectInfo  # noqa: F401,E501
from swagger_client.staff.models.put_system_trading_pair_list_response import PutSystemTradingPairListResponse
from swagger_client.staff.models.post_sponsor_request import PostSponsorRequest


user, password = '', ''
admin, pwd = '', ''
sponsor_account, sponsor_pwd = '', ''


def get_verify_token():
    """获取二次验证"""


class AllottedTime(IntEnum):
    _6month = 6
    _12month = 12


def get_project():
    manager = PlatformManager('venture')
    token = manager.login(user, password)
    api = VentureApi()
    api.api_client.set_default_header("Authentication-Token", token)
    while True:
        project_name = "test_project_" + str(random.randint(1, 10000))
        rv = api.applications_check_project_name_post(project_name=project_name)
        if not rv.result:
            break
    return dict(
        project_name=project_name,
        description="hell of a project",
        official_website="http://showmethemoney.com",
        white_paper="http://showmethemoney.com/whitepaper",
        area_code="1333",
        project_poster="http://showmethemoney.com/poster",
        cellphone="86-123812391",
        telephone="12434234",
        email="helloboy@icloud.com",
        full_name="hellboy",
        short_name="HB",
        issue_price="100 dollors",
        issued_volume="15",
        circulation_volume="13",
        issued_at=datetime.now(),
        coin_logo="http://showmethemoney.com/coin_logo",
        blockchain_type="public_chain",
        data_link="link me baby",
        block_browser="browser what"
    )


def get_sponsors():
    """获取保鉴机构"""
    manager = PlatformManager('audit')
    token = manager.login(user, password)
    api = SponsorsManagermentApi()
    api.api_client.set_default_header("Authentication-Token", token)
    rv = api.staff_sponsors_get(status=0)
    if len(rv.items) > 0:
        return rv.items[0]
    else:
        req = PostSponsorRequest(
            account=sponsor_account,
            name='大保鉴',
            password=sponsor_pwd,
            phone='15526548799',
            email='12121525'
        )
        api.staff_sponsors_post(req)
    rv = api.staff_sponsors_get(status=0)
    return rv.items[0]


class TestProject(object):
    data = {}
    service_rate = 0.1
    fee_rate = 0.1

    @pytest.mark.order1
    def test_get_project(self, with_login):
        """1.新增项目——获取所有项目——获取项目详情"""
        sponsor = get_sponsors()
        venture_api = VentureApi()
        user_data = register_with_login('venture', with_login, [venture_api])
        TestProject.data['user'] = user_data
        project = get_project()
        TestProject.data['project'] = project
        req = ApplicationRequest(**project)
        rv = venture_api.applications_post(req)
        project_id = rv.id
        TestProject.data['project_id'] = project_id
        # 设置接入方式
        setting = PutProjectRequestSetting(access_method='accept')
        project_info = PutProjectRequestProjectInfo(access_method='accept')
        req = PutProjectRequest(project_info=project_info, setting=setting)
        venture_api.projects_id_put(req)
        # 设置保健机构

        venture_api.applications_id_set_sponsor_put(project_id,
                                                    {'sponsorId': sponsor.id})
        project_name = project['project_name']
        sponsor_api = SponsorsProjectApi()
        manager = PlatformManager('sponsor')
        token = manager.login(sponsor_account, sponsor_pwd)
        sponsor_api.api_client.set_default_header("Authentication-Token", token)
        rv = sponsor_api.projects_get(page=1, project_name=project_name)
        assert len(rv.items) == 1
        assert rv.items[0].id == project_id
        rv = sponsor_api.projects_id_get(id=project_id)
        assert rv.project_info.project_name == project['project_name']
        assert rv.coin_info.short_name == project['short_name']

        # 保健通过
        sponsor_api.projects_sponsor_put({'id': project_id, 'status': 1,
                                          'remark': 'test'})

        project_api = ProjectApi()

        project_api.api_client.set_default_header("Authentication-Token",
                                                  user_data['token'])
        rv = project_api.projects_get()
        assert len(rv.items) == 1
        p = rv.items[0]
        assert p.project_id == project_id

        # 获取项目详情
        rv = project_api.projects_id_get(id=project_id)
        assert rv.sponsor_info.sponsor_id == sponsor.id
        assert rv.project_info.id == project_id
        assert rv.coin_info.short_name == project['short_name']

        # 合并测试用例
        """1.新增项目——获取项目列表——收藏——收藏列表（项目）"""
        token = user_data['token']
        account_api = AccountApi()
        account_api.api_client.set_default_header("Authentication-Token", token)
        account_info = account_api.accounts_account_info_get()
        account_id = account_info.accountInfo.accountId

        f_api = FavoriteManagementApi()
        f_api.api_client.set_default_header("Authentication-Token", token)
        req = PostFavoriterRequest()
        req.favorite_id = project_id
        req.type = 'project'
        f_api.favorites_post(req)

        # 收藏列表
        flag = False
        pages = Pager(f_api.favorites_get)
        favorite_record_id = None
        for page in pages:
            for record in page.items:
                if record.favorite_id == project_id:
                    if record.type == 'project':
                        flag = True
                        favorite_record_id = record.id
                        break
            if flag:
                break
        assert flag

        # 合并测试用例
        """5.收藏项目成功——收藏列表（项目）——取消收藏"""
        # 取消收藏
        req = DeleteFavoriterRequest()
        req.id_items = [favorite_record_id]
        f_api.favorites_ids_delete(req)
        rv = f_api.favorites_is_favorite_get(favorite_id=project_id,
                                             type='project')
        assert not rv.status

    @pytest.mark.order2
    def test_exchange_project(self):
        """2.新增项目——对接交易所——获取交易所卖买方币种列表
            ——单一币种在单一交易所币对的行情统计"""
        exchange = new_exchange()
        exchange_api = ExchangeManagementApi()
        user_data = TestProject.data['user']
        token = user_data['token']
        exchange_api.api_client.set_default_header("Authentication-Token",
                                                   token)
        account_api = AccountApi()
        account_api.api_client.set_default_header("Authentication-Token", token)
        account_info = account_api.accounts_account_info_get()
        account_id = account_info.accountInfo.accountId
        TestProject.data['account_id'] = account_id
        exchange_api.exchange_post(exchange)
        manager = PlatformManager('tenant')
        token = manager.login(sponsor_account, sponsor_pwd)
        audit_api = AuditApi()
        audit_api.api_client.set_default_header("Authentication-Token",
                                                token)
        # 初审
        rv = audit_api.tenant_audits_get()
        audit_list = rv.items
        _id = None
        for each in audit_list:
            if each.uid == account_id:
                _id = each.id  # 工单id
        assert not _id
        res = PostTenantAuditRequest(id=_id, is_data_received=True,
                                     status='approved', failure_type=1)
        audit_api.tenant_audits_audit_post(res)
        # 复审
        PostTenantReAuditRequest(id=_id, status='approved', failure_type=None)
        exchange_id = exchange_api.exchange_exchange_id_get()
        # 对接项目方
        contacts_api = ContactsApi()
        contacts_api.api_client.set_default_header("Authentication-Token",
                                                   token)
        req = {
            'exchangeId': exchange_id,
            'projectId': TestProject.data['project_id'],
            'sponsor': 'tenant'
        }
        contacts_api.contacts_post(req)
        # 获取交易所买卖方币种
        m_api = MarketManagementApi()
        m_api.api_client.set_default_header("Authentication-Token", token)
        trading_coins = m_api.markets_trading_coins_get()
        seller_coin = trading_coins.seller_coin
        s_coin = seller_coin[0]
        buyer_coin = trading_coins.buyer_coin
        b_coin = buyer_coin[0]
        assert s_coin == TestProject.data['project']['short_name']

        # 新建市场
        res = PostOrderMarketRequest()
        res.seller_coin_id = s_coin.id
        res.buyer_coin_id = b_coin.id
        TestProject.data['s_coin'] = s_coin
        TestProject.data['b_coin'] = b_coin
        res.allotted_time = AllottedTime._6month
        res.fee_rate = TestProject.fee_rate
        # 配置交易对市场
        rv = exchange_api.exchange_order_market_post(res)
        order_id = rv.order_id
        token = get_verify_token()
        p = PutOrderMarketRequest(order_id=order_id, token=token)
        exchange_api.exchange_order_market_put(p)

        # 单一币种在单一交易所币对的行情统计
        dashboard_api = DashboardApi()
        dashboard_api.api_client.set_default_header("Authentication-Token",
                                                    token)
        dashboard_api.dashboard_quotation_historical_data_post()
        dashboard_api.dashboard_quotations_summary_get(page_no=1,
                                                       page_size=10,
                                                       seller_coin=seller_coin)
        # 3.新增项目——对接交易所——获取交易所卖买方币种列表——单一币种在各交易所的行情概要
        dashboard_api.dashboard_daily_statistics_get()

    @pytest.mark.order3
    def test_system_management(self):
        """1.前台新建市场成功——（后台）获取分区列表——交易币对配置列表
        ——修改交易币对配置——交易币对配置列表"""
        # 获取分区列表
        sys_api = SystemManagementApi()
        manager = PlatformManager('tenant')
        token = manager.login(sponsor_account, sponsor_pwd)
        sys_api.api_client.set_default_header("Authentication-Token", token)
        b_coin = TestProject.data['b_coin']
        s_coin = TestProject.data['s_coin']
        req = {
            'name':  s_coin.name,
            'partitionId': b_coin.id,
            'page': 1
        }
        rv = sys_api.system_trading_pair_get(**req)
        assert len(rv.recharge_record) == 1
        record = rv.charge_record
        _id = record[0].id  # 交易对配置id
        price = record.price
        min_trading_price = record.min_trading_price
        max_trading_price = record.max_trading_price
        req = PutSystemTradingPairListResponse()
        req.min_trading_price = min_trading_price * 2
        req.max_trading_price = max_trading_price * 2
        req.price = price * 2
        # 修改交易对配置
        """2.前台新建市场成功——（后台）获取分区列表——交易币对配置列表
        ——批量修改交易币对单价——交易币对配置列表"""
        # 合并测试用例
        sys_api.system_trading_pair_id_put(_id, req)
        rv = sys_api.system_trading_pair_get(**req)
        record_1 = rv.charge_record
        assert record_1.min_trading_price == min_trading_price * 2
        assert record_1.max_trading_price == max_trading_price * 2
        assert record_1.price == price * 2

    @pytest.mark.order4
    def test_system_coins(self):
        """5.项目申请审核成功——币种配置列表——币种配置详情"""
        # 获取币种配置列表
        sys_api = SystemManagementApi()
        manager = PlatformManager('audit')
        token = manager.login(sponsor_account, sponsor_pwd)
        sys_api.api_client.set_default_header("Authentication-Token", token)
        project = TestProject.data['project']
        coin_name = project['short_name']
        pager = Pager(sys_api.system_coins_get, coinName=coin_name)
        coin_config_id = None
        for item in pager:
            coin_info = item.coinInfo
            for each in coin_info:
                if each.coin_name == coin_name:
                    coin_config_id = each.id
                    break
            if coin_config_id is not None:
                break
        assert coin_config_id is not None
        sys_api.system_coins_id_get(id=coin_config_id)
        """6.项目申请审核成功——修改币种配置——进行充提币操作——修改币种配置——进行充提币操作"""
        # 修改币种配置列表
        req = PutSystemCoinsRequest()
        req.min_recharge = '1'
        req.min_withdraw = '100'
        req.max_withdraw = '1222'
        sys_api.system_coins_id_put(req)
        rv = sys_api.system_coins_id_get(id=coin_config_id)
        assert rv.min_withdraw == '100'
        assert rv.max_withdraw == '1222'
        assert rv.min_recharge == '1'
        # todo　进行冲提币

        """
        7.项目申请审核成功——是否可充币（是）——前台进行充币操作 
        8.项目申请审核成功——是否可提币（是）——前台进行提币操作
        9.项目申请审核成功——是否可充币（否）——前台进行充币操作 
        10.项目申请审核成功——是否可提币（否）——前台进行提币操作
        """
        # 是否可冲提币
        sys_api.system_coins_id_recharge_put(id=coin_config_id,
                                             rechargeable=False)
        sys_api.system_coins_id_recharge_put(id=coin_config_id,
                                             rechargeable=True)
        sys_api.system_coins_id_withdraw_put(id=coin_config_id,
                                             withdrawable=False)
        sys_api.system_coins_id_withdraw_put(id=coin_config_id,
                                             withdrawable=True)
        # todo 冲提币操作

        """11.项目申请审核成功——币种配置列表——获取提示信息——编辑提示——获取提示信息"""
        sys_api.system_coins_id_prompt_get(id=coin_config_id)
        # 编辑提示
        req = {
            'defaultInfo': True,
            'prompt': 'for test'
        }
        sys_api.system_coins_id_prompt_put(coin_config_id, req)
        rv = sys_api.system_coins_id_prompt_get(id=coin_config_id)
        assert rv.prompt == 'for test'

    @pytest.mark.order5
    def test_failure_reasons(self):
        """12.新增审核失败原因——获取审核失败原因"""
        sys_api = SystemManagementApi()
        manager = PlatformManager('audit')
        token = manager.login(sponsor_account, sponsor_pwd)
        sys_api.api_client.set_default_header("Authentication-Token", token)
        sys_api.system_failure_reasons_get()
        # 新增审核失败原因
        new_failure_reason = 'for testing'
        sys_api.system_failure_reasons_post(
            {'failureReason': new_failure_reason,
             'type': 'PERSONAL_AUTHENTICATE'}
        )
        rv = sys_api.system_failure_reasons_get(type='PERSONAL_AUTHENTICATE')
        flag = False
        failure_reason_id = None
        for each in rv.items:
            if each.failure_reason == new_failure_reason:
                flag = True
                failure_reason_id = each.id
                break
        assert flag

        """13.新增审核失败原因——获取审核失败原因——弃用审核失败原因——获取审核失败原因"""
        # 弃用审核失败原因
        sys_api.system_failure_reasons_delete([failure_reason_id])

        # 获取审核失败原因
        rv = sys_api.system_failure_reasons_get(type='PERSONAL_AUTHENTICATE')
        for each in rv.items:
            if each.id == failure_reason_id:
                assert False


class TestTradingRate(object):

    def test_trading_rate(self):
        """3.修改交易佣金设置——币币交易——交易所返佣管理——修改交易佣金设置
        ——币币交易——交易返佣管理"""

    def test_service_rate(self):
        """4.获取当前交易服务费率——服务费率设置——获取当前交易服务费率"""
        sys_api = SystemManagementApi()
        manager = PlatformManager('audit')
        token = manager.login(sponsor_account, sponsor_pwd)
        sys_api.api_client.set_default_header("Authentication-Token", token)
        rv = sys_api.system_system_config_get()
        value = None
        for each in rv:
            if each.config_key == 'SERVICE_RATE':
                value = each.config_vlaue
        assert value is not None
        sys_api.system_system_config_id_put(
            {'configKey': '', 'configValue': 2 * value}
        )
        rv = sys_api.system_system_config_get()
        flag = False
        for each in rv:
            if each.config_key == 'SERVICE_RATE':
                assert each.config_vlaue == 2 * value
                flag = True
        assert flag





































