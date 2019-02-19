#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-13

import json
import random
import logging
from swagger_client.tenant import *
from swagger_client.tenant.rest import ApiException

from test.tenant.instance import Instance, get_templated_attrs
from common.pager import list_items, query_items, query_unique_item, Pager
from common.photo import *
from test.tenant.account import Account
from test.tenant.market import Market
from test.tenant.asset import Asset
from test.tenant.exchange import Exchange
from test.tenant.staff import Staff
from test.tenant.contacts import Contacts
from test.tenant.util_upload import UtilUpload
from test.tenant.id_settings import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)

DEFAULT_VERIFY_CODE = "666666"


class NoSuchMarket(Exception):
    pass


class Tenant(Instance, Account, Asset, Contacts, UtilUpload):
    _instances = dict()

    # ================= platform depend model type =================
    
    PostRegisterRequest = PostRegisterRequest
    ApiException = ApiException
    PostLoginRequest = PostLoginRequest
    PostBindPhoneRequest = PostBindPhoneRequest
    PostIndividualCertificationRequest = PostIndividualCertificationRequest
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
    
    def __init__(self, index, attrs=None, *args, **kwargs):
        super().__init__(index, attrs=attrs)
        if attrs:
            for key, val in attrs.items():
                setattr(self, key, val)
        self.api_account = AccountApi()
        self.api_banner_management = BannerManagementApi()
        self.api_contacts = ContactsApi()
        self.api_dashboard = DashboardApi()
        self.api_exchange_announcement = ExchangeAnnouncementApi()
        self.api_exchange_management = ExchangeManagementApi()
        self.api_project = ProjectApi()
        self.api_market_management = MarketManagementApi()
        self.api_verification = VerificationApi()
        self.api_asset_management = AssetManagementApi()
        self.api_order_management = OrderManagementApi()
        self.api_file_upload = FileUploadApi()
        
    def list_contacts(self, exchange_id, status):
        return list_items(self.api_contacts.contacts_projects_exchange_id_get, exchange_id=exchange_id, status=status)
    
    def list_orders(self):
        return list_items(self.api_asset_management.orders_get)
    
    def list_projects(self):
        return list_items(self.api_project.projects_get)
    
    def get_contacts_status_by_project_id(self, project_id):
        return self.api_contacts.contacts_project_id_status_get(project_id=project_id)
    
    def list_announcements(self):
        return list_items(self.api_exchange_announcement.announcements_exchanges_get)
    
    def query_unique_announcement(self, filter=None):
        return query_unique_item(self.api_exchange_announcement.announcements_exchanges_get, filter=filter)
    
    def post_announcement(self, title, content, language):
        req = PostNoticesRequest(title=title, content=content, language=language)
        self.api_exchange_announcement.announcements_post(body=req)
    
    def get_announcement(self, announcement_id):
        rsp = self.api_exchange_announcement.announcements_id_get(id=announcement_id)
        return rsp
    
    def update_announcement(self, announcement_id, title, content, language):
        req = PostNoticesRequest(title=title, content=content, language=language)
        self.api_exchange_announcement.announcements_id_put(id=announcement_id, body=req)
    
    def enable_announcement(self, announcement_id, status):
        self.api_exchange_announcement.announcements_id_enable_put(id=announcement_id, status=status)
    
    def delete_announcement(self, announcement_id):
        self.api_exchange_announcement.announcements_id_delete(id=announcement_id)
    
    def get_pending_contacts(self):
        rsp = self.api_exchange_management.exchange_exchange_id_get()
        rsp = self.api_contacts.contacts_projects_exchange_id_get(exchange_id=rsp.id, status="pending")
        contacts = rsp.items()
        return [c.id for c in contacts]

    def get_market_details(self, market_id):
        details = self.api_market_management.markets_id_get(market_id)
        return details

    def get_market(self, buy, sell):
        info = self.get_market_info(buy_id=buy, sell_id=sell)
        if info:
            details = self.get_market_details(info["market_id"])
            market = Market(attrs=dict(
                buy_coin=details.buyer_coin_id,
                sell_coin=details.seller_coin_id,
                fee_rate=details.fee_rate,
                alloted_time="6",
                market_id=info["market_id"]))
            return market
    
    def recharge_market(self, market_id, allotted_time):
        req = PostOrderMarketRenewRequest(market_id=market_id, allotted_time=allotted_time)
        rsp = self.api_exchange_management.exchange_order_market_renew_post(body=req)
        order_id = rsp.order_id
        assert order_id, "recharge market order id can't be null"

        payment_token = self.verify_payment_token()
        req = PutOrderMarketRequest(order_id=order_id, token=payment_token)
        self.api_exchange_management.exchange_order_market_renew_put(body=req)

        details = self.get_market_details(market_id=market_id)

        renew_market = Market(attrs=dict(
            buy_coin=details.buyer_coin_id,
            sell_coin=details.seller_coin_id,
            disabled_at=details.disabled_at,
            fee_rate=details.fee_rate,
            market_id=details.id
        ))

        return renew_market, order_id
        
    def create_market(self, buy, sell, allotted_time, fee_rate):
        print("create market buy:%s sell:%s allotted_time:%s" %(buy, sell, allotted_time))
        req = PostOrderMarketRequest(seller_coin_id=sell, buyer_coin_id=buy, allotted_time=allotted_time, fee_rate=fee_rate)
        order_id = ""
        try:
            rsp = self.api_exchange_management.exchange_order_market_post(body=req)
        except ApiException as e:
            if e.status == 400 and (json.loads(e.body)["message"] == "市场已存在" or json.loads(e.body)["message"] == "The market already exists"):
                logger.warn("市场已经存在，无法重复创建")
            else:
                raise
        else:
            order_id = rsp.order_id
            assert order_id, "create market order id can't be null"
            payment_token = self.verify_payment_token()
            req = PutOrderMarketRequest(order_id=order_id, token=payment_token)
            self.api_exchange_management.exchange_order_market_put(body=req)

        info = self.get_market_info(buy, sell)
        
        new_market = Market(attrs=dict(
            buy_coin=buy,
            sell_coin=sell,
            alloted_time=allotted_time,
            fee_rate=fee_rate,
            market_id=info["market_id"] if info else ""
        ))
        
        return new_market, order_id
    
    def open_market(self, market_id):
        self.api_market_management.markets_id_open_put(market_id)

    def close_market(self, market_id):
        token = self.verify_close_market_token()
        req = PostMarketCloseRequest(id=market_id, token=token, closing_reason="i like it, come on baby,hahaha")
        self.api_market_management.markets_close_post(body=req)

    def get_market_price(self, buy, sell):
        rsp = self.api_market_management.markets_price_get(buyer_coin_id=buy, seller_coin_id=sell)
        return rsp.price
    
    def list_markets(self):
        try:
            ret = list_items(self.api_market_management.markets_get)
        except ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "exchange not exist":
                logger.warning("No exchange under tenant:%s", self.email)
            else:
                raise
        else:
            return ret
        
    def get_pair_name(self, buy_id, sell_id):
        buy_name = ""
        sell_name = ""
        pairs = self.api_market_management.markets_trading_coins_get()
        
        for buy in pairs.buyer_coin:
            # print("====> %s vs %s" % (buy_id, buy.id))
            if buy_id == str(buy.id):
                buy_name = buy.name
        for sell in pairs.seller_coin:
            # print("====> %s vs %s" % (sell_id, sell.id))
            if sell_id == str(sell.id):
                sell_name = sell.name
        return buy_name, sell_name

    def get_pair_id(self, buy_name, sell_name):
        buy_id = ""
        sell_id = ""
        pairs = self.api_market_management.markets_trading_coins_get()
        for buy in pairs.buyer_coin:
            if buy_name == buy.name:
                buy_id = buy.id
        for sell in pairs.seller_coin:
            if sell_name == sell.name:
                sell_id = sell.id
        return buy_id, sell_id

    def get_market_info(self, buy_id, sell_id):
        buy_name, sell_name = self.get_pair_name(buy_id, sell_id)
        trading_pair = "%s/%s" % (sell_name, buy_name)
        for market in self.list_markets():
            if market.trading_pair == trading_pair:
                return dict(market_id=market.id, trading_pair=trading_pair)
        
    def is_exchange_approved(self):
        try:
            rsp = self.api_exchange_management.exchange_exchange_status_get()
        except ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "交易所不存在":
                print("交易所不存在")
            else:
                raise
        else:
            # print("exchange approved ===>", rsp.status == "approved")
            if rsp.status == "approved":
                return True
            
    def get_exchange_id(self):
        return self.api_exchange_management.exchange_exchange_id_get().id

    def create_exchange(self, index=None, attrs=None):
        assert not (index is None and attrs is None), "Both index and attrs can't be None at the same time"
        
        exchange = Exchange(index=index, attrs=attrs)
        print("========> try to create exchange:",exchange.exchange_name)
        req = GetExchangeRequest(name=exchange.exchange_name,
                                 nationality=exchange.nationality,
                                 logo=exchange.logo_url,
                                 tags=exchange.tags,
                                 phone=self.phone,
                                 email=self.email)
        try:
            self.api_exchange_management.exchange_post(body=req)
        except ApiException as e:
            if e.status == 400 and (json.loads(e.body)["message"] == "审核中不可以在次提交审核"
                                    or json.loads(e.body)["message"] == "Duplicate exchange name"):
                logger.warning(json.loads(e.body)["message"])
            else:
                raise
        
        return exchange

    def get_exchange(self):
        if self.is_exchange_approved():
            rsp_details = self.api_exchange_management.exchange_get()
            rsp_id = self.api_exchange_management.exchange_exchange_id_get()
            exchange = Exchange(attrs=dict(
                exchange_name=rsp_details.name,
                exchange_id=rsp_id.id,
                logo_url=rsp_details.logo_url,
                logo_key=rsp_details.logo_key,
                nationality=rsp_details.nationality,
                tags=rsp_details.tags))
            
            return exchange

    def update_exchange_info(self):
        rsp_details = self.api_exchange_management.exchange_get()
        rsp_id = self.api_exchange_management.exchange_exchange_id_get()
        exchange = Exchange(attrs=dict(
            exchange_name=rsp_details.name,
            exchange_id=rsp_id.id,
            logo_url=rsp_details.logo_url,
            logo_key=rsp_details.logo_key,
            nationality=rsp_details.nationality,
            tags=rsp_details.tags))
    
        return exchange

    def verify_market_trading_coin(self, buy_coin, sell_coin):
        
        rsp = self.api_market_management.markets_trading_coins_verify_get(buyer_coin_id=buy_coin, seller_coin_id=sell_coin)
        print("verify %s/%s " % (buy_coin, sell_coin))
        print("rsp : ", rsp)
        return rsp
    
    def get_market_adding_order_details(self, order_id):
        return self.api_order_management.orders_details_add_market_id_get(id=order_id)

    def get_market_recharge_order_datails(self, order_id):
        return self.api_order_management.orders_details_recharge_market_id_get(id=order_id)

    def list_banners(self):
        rsp = self.api_banner_management.banners_get()
        return rsp.items if rsp else None
    
    def query_unique_banner(self, filter=None):
        assert filter, "banner filter must not be null"
        banners = list()
        for ban in self.list_banners():
            for key, val in filter.items():
                if getattr(ban, key) != val:
                    break
            else:
                banners.append(ban)
        assert len(banners) <= 1, "Result is not not unique banner "
        if banners:
            return banners[0]
        
    def query_banners(self, filter=None):
        assert filter, "banner filter must not be null"
        banners = list()
        for ban in self.list_banners():
            for key, val in filter.items():
                if getattr(ban, key) != val:
                    break
            else:
                banners.append(ban)
        return banners
        
    def add_banner(self, title, banner, url):
        req = PostBannerRequest(title=title, banner=banner, url=url)
        return self.api_banner_management.banners_post(body=req)
    
    def get_banner(self, banner_id):
        return self.api_banner_management.banners_id_get(id=banner_id)

    def update_banner(self, banner_id, title, banner, url):
        req = PostBannerRequest(title=title, banner=banner, url=url)
        return self.api_banner_management.banners_id_put(banner_id, body=req)
    
    def delete_banner(self, banner_id):
        return self.api_banner_management.banners_id_delete(id=banner_id)
    
    def update_banner_status(self, banner_id, status):
        return self.api_banner_management.banners_id_status_put(id=banner_id, status=status)
    
    def reset_banner(self, banner_id):
        return self.api_banner_management.banners_id_reduction_put(id=banner_id)

    def get_exchange_tags(self):
        rsp = self.api_exchange_management.tags_get()
        return rsp.tags

    def get_daily_statistics(self):
        return self.api_dashboard.dashboard_daily_statistics_get()

    def list_contacts_project(self, exchange_id, status):
        return list_items(self.api_contacts.contacts_projects_exchange_id_get, exchange_id=exchange_id, status=status)
    

def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    _tenant.request_individual_cert()
    print("identity:%s, email:%s password:%s",_tenant.identity, _tenant.email, _tenant.password)
    _staff.verify_individual(identity=_tenant.identity, approval="approved")
    assert _tenant.audit_accepted()
    print(_tenant.api_account.accounts_account_info_get())
    for market in _tenant.list_markets():
        print(_tenant.get_market_details(market_id=market.id))
    # logger.info("==========  Tenant(%u) ready  ==========" % CONFIG.TENANT_INDEX)
    print("daily statistics ===>", _tenant.get_daily_statistics())
    print("test photo:", _tenant.upload(path="/home/xy/repos/gitlab/java-crush-test2.0/test/tenant/python.jpg"))


if __name__ == '__main__':
    main()
