#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-14
import json
import requests
from test.tenant.account import Account
from test.tenant.asset import Asset
from test.tenant.dealer import Dealer
from test.tenant.faucet import Faucet
from common.photo import *


from test.tenant.instance import Instance
from common.pager import list_items, query_unique_item, query_items, Pager

from swagger_client.main.rest import ApiException
from swagger_client.main import *
from test.tenant.id_settings import *


class Main(Instance, Account, Asset, Dealer):
    
    _instances = dict()
    
    # ================= platform depend model type =================

    ApiException = ApiException
    PostRegisterRequest = PostRegisterRequest
    PostLoginRequest = PostLoginRequest
    PostBindPhoneRequest = PostBindPhoneRequest
    PostIndividualCertificationRequest = PostIndividualCertificationRequest
    PostEntrustsRequest = PostEntrustsRequest
    
    # ================== attrs auto set by meta class ==================
    
    attrs_template = dict(
        email=lambda name, index: "%s_%s_%u@gmail.com" % (CONFIG.TESTER.upper(), name, index),
        password=lambda name, index: "%s_%s_pwd" % (CONFIG.TESTER.upper(), name),
        name=lambda name, index: "%s%s%u" % (CONFIG.TESTER.upper(), name, index),
        logo=PHOTO_URL,
        account=lambda name, index: "_%s%s%u" % (CONFIG.TESTER.upper(), name, index),
        phone=lambda name, index: "18%s%s%04d" % (platfrom_id(name), name_hash(CONFIG.TESTER.upper()), index),
        identity=lambda name, index: "23233219%s%s%05d" % (platfrom_id(name), name_hash(CONFIG.TESTER.upper()), index),
        nationality_code=lambda name, index: "CN")
    
    def __init__(self, index, attrs=None):
        super().__init__(index, attrs=attrs)
        if attrs:
            for key, val in attrs.items():
                setattr(self, key, val)

        self.api_verification = VerificationApi()
        self.api_announcement_management = AnnouncementManagementApi()
        self.api_market = MarketApi()
        self.api_account = AccountApi()
        self.api_asset_management = AssetManagementApi()
        self.api_exchange = ExchangeApi()
        self.api_entrust = EntrustApi()
        self.api_project = ProjectApi()
        self.api_banner_management = BannerMangementApi()
        self.api_project_center = ProjectCenterApi()

        self.api_entrust = EntrustApi()
        self.api_quota = QuotationApi()
        
    def list_exchanges(self):
        return list_items(self.api_exchange.exchanges_exchanges_get)

    def list_market_on_line(self, project_id):
        return list_items(self.api_project_center.project_center_projects_id_markets_get, project_id=project_id)

    def query_unique_market_on_line(self, project_id, filter=None):
        return query_unique_item(
            self.api_project_center.project_center_projects_id_markets_get,
            id=project_id,
            filter=filter
        )
    
    def list_projects(self):
        return list_items(self.api_project.projects_get, sort_key="volume", limit=1000)

    def get_banners_by_exchagne_id(self, exchange_id):
        return self.api_banner_management.banners_exchange_id_get(exchange_id=exchange_id).items
    
    def query_banners_by_exchange_id(self, exchange_id, filter=None):
        banners = list()
        for ban in self.get_banners_by_exchagne_id(exchange_id=exchange_id):
            for key, val in filter.items():
                if getattr(ban, key) != val:
                    break
            else:
                banners.append(ban)
        return banners
    
    def query_banners(self, language, position=None, platform=None):
        return self.api_banner_management.banners_get(language=language, position=position, platform=platform)
        
    def list_announcements_by_exchange_id(self, exchange_id):
        return list_items(self.api_announcement_management.exchange_announcements_exchange_id_exchange_get, exchange_id=exchange_id)
    
    def list_announcements_by_project_id(self, project_id):
        return list_items(self.api_announcement_management.project_announcements_project_id_announcement_get, project_id=project_id)
    
    def get_project_announcement(self, announcemen_id):
        return self.api_announcement_management.project_announcements_id_get(id=announcemen_id)

    def get_exchange_announcement(self, announcemen_id):
        return self.api_announcement_management.exchange_announcements_id_get(id=announcemen_id)

    def get_market_suggestion(self, trading_pair, exchange_id):
        rsp = self.api_market.markets_suggestion_get(name=trading_pair, exchange_id=exchange_id)
        return rsp.items
    
    def get_newest_announcement(self, target_id, ann_type):
        return self.api_announcement_management.newest_announcements_get(ids=target_id, type=ann_type)

    def get_market_details(self, market_id):
        return self.api_market.markets_id_get(id=market_id)
    
    def free_charge(self, coin_id, amount):
        headers = {"Authorization": f"Bearer {self.token_mgr.token}"}
        host = self.api_market.api_client.configuration.host
        print("host: ===========>", host)
        rsp = requests.post(
            f"{host}/asset-test/asset-initialize/{coin_id}/{amount}",
            headers=headers
        )
        if rsp.status_code != 200:
            rsp.raise_for_status()
            
            
def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    _main = Main(CONFIG.MAIN_INDEX)
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    _main.request_individual_cert()
    _staff.verify_individual(identity=_main.identity, approval="ACCEPTED")
    
    _venture = Venture(CONFIG.VENTURE_INDEX)
    _venture.request_individual_cert()
    _staff.verify_individual(identity=_venture.identity, approval="ACCEPTED")
    
    print(_main.api_account.accounts_account_info_get())
    usdt_id = _venture.get_usdt_coin_id()
    print("usdt_id ==>", )
    _faucet = Faucet(_main.token_mgr.token, _main.api_account.api_client.configuration.host)
    _faucet.free_charge(coin_id=usdt_id, amount=10000000000000)
    
    print("tenant:", _tenant.account_id)
    print("main usdt balance:", _main.query_coin_balance(usdt_id))
    print("tenant usdt balance:", _tenant.query_coin_balance(usdt_id))
    print("entrusts ===============>", _main.api_entrust.entrusts_get())
    print("projects list =============>", _main.list_projects())
    print("exchanges list=============>", _main.list_exchanges())
    
    
if __name__ == '__main__':
    from test.tenant.staff import Staff
    from test.tenant.venture import Venture
    from test.tenant.tenant import Tenant
    
    main()
