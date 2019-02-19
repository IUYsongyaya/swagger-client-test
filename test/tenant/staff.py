# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-14
import json
import logging

from common.certification_verify import individual_verify, company_verify
from swagger_client.staff import *
from swagger_client.staff.rest import ApiException
from test.tenant.account import Account
from test.tenant.asset import Asset
from test.tenant.util_upload import UtilUpload
from test.tenant.instance import Instance
from test.tenant.token_manager import TokenManager
from test.tenant.id_settings import *
from common.pager import query_unique_item, query_items, list_items, Pager
from common.photo import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


class Staff(Instance, Account, Asset, UtilUpload):
    
    _instances = dict()

    # ================= platform depend model type =================
    PutSystemCoinsRequest = PutSystemCoinsRequest
    PutSystemCoinsInitRequest = PutSystemCoinsInitRequest
    PutSponsorRequest = PutSponsorRequest
    
    attrs_template = dict(
        email=lambda name, index: "user_%s_%u@gmail.com" % (name, index),
        password="19831116zxy",
        name=lambda name, index: "%s_%u" % (name, index),
        logo=PHOTO_URL,
        account="zhangxuyi",
        phone=lambda name, index: "1%s%s%05d" % (platfrom_id(name), name_hash(CONFIG.TESTER), index),
        identity=lambda name, index: "23233219%s%s%05d" % (platfrom_id(name), name_hash(CONFIG.TESTER.upper()), index))

    def __init__(self, index, attrs=None):
        super().__init__(index, attrs=attrs)
        if attrs:
            for key, val in attrs.items():
                setattr(self, key, val)
        self.api_sponsors_management = SponsorsManagermentApi()
        self.api_venture_management = VentureManagementApi()
        self.api_exchange_management = ExchangeManagementApi()
        self.api_audit = AuditApi()
        self.api_announcement_management = AnnouncementManagementApi()
        self.api_project = ProjectApi()
        self.api_asset_management = AssetManagementApi()
        self.api_staff_management = StaffManagementApi()
        self.api_account_management = AccountManagementApi()
        self.api_website_management = WebsiteManagementApi()
        self.api_market_management = MarketManagementApi()
        self.api_advertisement = AdvertisementApi()
        self.api_business = BussinessApi()
        self.api_content_management = ContentManagementApi()
        self.api_order_management = OrderManagementApi()
        self.api_project_management = ProjectManagementApi()
        self.api_file_upload = FileUploadApi()
        self.ApiException = ApiException
        self._inited = False
        self.token_mgr = None

    def init_instance(self):
        rsp = self.api_staff_management.login_post(body=PostLoginRequest(account=self.account, password=self.password))
        payload = {
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "string",
            "validate": "true",
            "account": "number:"+rsp.phone,
            "code": "666666",
            "baseToken": rsp.token
        }
        rsp = self.api_account_management.accounts_verify_post(verify_info=payload)
        self.token_mgr = TokenManager(rsp.token)
        self.token_mgr.auth_headers(self)
        logger.info("<<<<<   %s   >>>>>", type(self))
        logger.info("account %s:", self.account)
        logger.info("password %s:", self.password)
        logger.info("email : %s", self.email)
        logger.info("identity : %s", self.identity)
        logger.info("<<<<<<<<<<<<<>>>>>>>>>>>")
        self._inited = True
        
    def approve_first_instance(self, ticket_number, approval='approved'):
        self.api_audit.tenant_audits_tasks_id_individual_audit_get(id=ticket_number)
        req = PostTenantAuditRequest(id=ticket_number,
                                     is_data_received=True,
                                     status=approval,
                                     failure_type=0)
        
        self.api_audit.tenant_audits_audit_post(body=req)
        return True

    def approve_review(self, ticket_number, approval='approved'):
        self.api_audit.tenant_audits_tasks_id_individual_re_audit_get(id=ticket_number)
        req = PostTenantReAuditRequest(
            id=ticket_number,
            status=approval,
            failure_type=0
        )
        self.api_audit.tenant_audits_re_audit_post(body=req)
        return True
    
    def receive_indiv_audit(self, ticket_number):
        rsp = self.api_audit.accounts_individual_audits_tasks_receive_get(id=ticket_number)
        print("receive audit ===> ", rsp)

    def indivdual_audit(self, ticket_number, approval):
        assert ticket_number, "Ticket number should not be null"
        post_info = PostIndividualAuditRequest(
            id=ticket_number,
            status=approval,
            reject_type="INDIVIDUAL_ID")
        try:
            self.api_audit.accounts_individual_audits_post(body=post_info)
        except ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "Do not repeat the review":
                pass
            else:
                print("Exception message: ", json.loads(e.body)["message"])
                raise
    
    def verify_individual(self, identity, approval):
        app = query_unique_item(self.api_audit.accounts_individual_audits_get, id_number=identity, status="APPLIED")
        
        if app:
            self.receive_indiv_audit(ticket_number=app.id)
            self.indivdual_audit(ticket_number=app.id, approval=approval)
        
    def verify_company(self, social_number, approval):
        company_verify(platform="staff",
                       social_number=social_number,
                       token=self.token_mgr.token,
                       verify_status=approval,
                       reject_type="INDIVIDUAL_ID")
        
    def create_sponsor(self, account, name, password, phone, email, *args, **kwargs):
        print("sponsor account:%s name:%s password:%s phone:%s email:%s" % (account, name, password, phone, email))
        payload = {
          "account": account,
          "name": name,
          "password": password,
          "phone": phone,
          "email": email
        }
        try:
            self.api_sponsors_management.staff_sponsors_post(post_sponsor=PostSponsorRequest(**payload))
            
        except ApiException as e:
            print("message =================>", json.loads(e.body)["message"])
            if e.status == 400 and (
                    json.loads(e.body)["message"].strip("\"") == "account or realName or email already exists" or
                    json.loads(e.body)["message"].strip("\"") == "新建保荐方账户失败，账户或名称或邮箱已存在"):
                print("sponsor account %s exists" % account)
                return True
            else:
                raise
        return True

    def list_sponsors(self):
        return list_items(self.api_sponsors_management.staff_sponsors_get)

    def update_sponsor(self, sponsor_id, logo, website, summary, phone):
        req = PutSponsorRequest(id=sponsor_id, logo=logo, website=website, summary="helloworld", phone=phone)
        self.api_sponsors_management.staff_sponsors_put(put_sponsor=req)

    def get_exchange_details(self, exchange_id):
        print("exchange_id ====>", exchange_id)
        rsp = self.api_exchange_management.exchange_id_get(id=exchange_id)
        return rsp

    def query_audits_tenant(self, uid, status="audit"):
        audits = query_items(self.api_audit.tenant_audits_get, uid=uid, type=status)
        return audits

    def audits_tenants(self, task_id, approval):
        self.approve_first_instance(ticket_number=task_id, approval=approval)
        
    def reaudits_tenants(self, task_id, approval):
        self.approve_review(ticket_number=task_id, approval=approval)
        
    def open_exchange(self, account_id, name, tags, area, logo, phone, email):
        req = PostExchangeRequest(account_id, name, tags, area, logo, phone, email)
        self.api_exchange_management.exchange_post(body=req)

    def lock_account(self, account_id, is_blocked=True, block_reason="i like it"):
        req = PutAccountsLockRequest(is_blocked=is_blocked, blocked_reason=block_reason)
        self.api_account_management.accounts_id_lock_account_put(id=account_id, body=req)

    def unlock_account(self, account_id, is_blocked=False):
        req = PutAccountsUnlockRequest(is_blocked=is_blocked)
        self.api_account_management.accounts_id_unlock_account_put(id=account_id, body=req)
        
    def create_tag(self, tag, other_language):
        req = PostExchangeTagsRequest(name=tag, other_language=other_language)
        self.api_website_management.exchange_tags_post(body=req)
        
    def list_tags(self):
        return list_items(self.api_website_management.exchange_tags_get)
    
    def query_tags(self, filter=None):
        return query_items(self.api_website_management.exchange_tags_get, filter=filter)
    
    def get_tag(self, tag_id):
        return self.api_website_management.exchange_tags_id_get(id=tag_id)
    
    def update_tag(self, tag_id, tag_name, other_language=None):
        req = PostExchangeTagsRequest(name=tag_name, other_language=other_language)
        self.api_website_management.exchange_tags_id_put(id=tag_id, body=req)
    
    def delete_tag(self, tag_id):
        self.api_website_management.exchange_tags_id_delete(id=tag_id)
    
    def list_exchanges(self):
        return list_items(self.api_exchange_management.exchanges_get)
    
    def open_market(self, market_id):
        return self.api_market_management.markets_id_open_put(market_id)

    def close_market(self, market_id):
        return self.api_market_management.markets_id_close_put(market_id, remarks="Just for fun, xy.zhang")
  
    def list_announcements_all_exchanges(self):
        return list_items(self.api_announcement_management.announcements_exchanges_get)

    def query_unique_announcement_all_exchanges(self, filter=None):
        return query_unique_item(self.api_announcement_management.announcements_exchanges_get, filter=filter)

    def list_announcements_by_exchange_id(self, exchange_id):
        return list_items(self.api_announcement_management.announcements_exchanges_list_exchange_id_get, exchange_id=exchange_id)

    def list_announcements_project(self, project_id):
        return list_items(self.api_announcement_management.announcements_projects_list_project_id_get, project_id=project_id)

    def query_announcements_project(self, project_id, filter=None):
        return query_items(
            self.api_announcement_management.announcements_projects_list_project_id_get,
            project_id=project_id,
            filter=filter
        )
    
    def query_announcements_by_exchange_id(self, exchange_id):
        return query_items(
            self.api_announcement_management.announcements_exchanges_list_exchange_id_get,
            exchange_id=exchange_id)
    
    def query_unique_announcement_by_exchange_id(self, exchange_id, filter=None):
        return query_unique_item(
            self.api_announcement_management.announcements_exchanges_list_exchange_id_get,
            exchange_id=exchange_id,
            filter=filter
        )
    
    def get_announcement(self, announcement_id):
        return self.api_announcement_management.announcements_id_get(id=announcement_id)

    def enable_announcement(self, announcement_id, status):
        self.api_announcement_management.announcements_id_status_put(id=announcement_id, status=status)
        
    @property
    def inited(self):
        return self._inited
    
    def list_projects(self, open=True):
        return list_items(self.api_project.projects_get, open=open)

    def list_ventures(self):
        return list_items(self.api_venture_management.accounts_ventures_get)

    def query_unique_venture(self, filter=None):
        return query_unique_item(self.api_venture_management.accounts_ventures_get, filter=filter)

    def query_project(self, open=True, filter=None):
        return query_items(self.api_project.projects_get, filter=filter, open=open)

    def list_projects_by_account_id(self, account_id):
        return list_items(self.api_project.projects_account_id_get, id=account_id)

    def query_exchange_by_project_id(self, project_id, filter=None):
        return query_items(self.api_project_management.get_project_exchange_list, id=project_id, filter=filter)

    def list_exchange_by_project_id(self, project_id):
        return list_items(self.api_project_management.get_project_exchange_list, id=project_id)

    def list_banners(self):
        return list_items(self.api_content_management.banners_get)

    def query_banners(self, filter=None):
        return query_items(self.api_content_management.banners_get, filter=filter)

    def add_banner(self, title, banner, platform, position, language, order, status, url):
        req = PostBannerRequest(title=title, banner=banner, platform=platform, position=position, language=language,
                                order=order, status=status, url=url)
        return self.api_content_management.banners_post(body=req)
    
    def get_banner(self, banner_id):
        return self.api_content_management.banners_id_get(id=banner_id)
    
    def delete_banner(self, banner_id):
        return self.api_content_management.banners_id_delete(id=banner_id)
    
    def update_banner(self, banner_id, title, banner, platform, position, language, order, status, url):
        req = PostBannerRequest(title=title, banner=banner, platform=platform, position=position, language=language,
                                order=order, status=status, url=url)
        return self.api_content_management.banners_id_put(id=banner_id, body=req)
        
    def list_orders(self):
        return list_items(self.api_order_management.orders_orders_get)
    
    def query_unique_order(self, order_id):
        return query_unique_item(self.api_order_management.orders_orders_get, order_id=order_id)
    
    def get_market_adding_order_details(self, order_id):
        return self.api_order_management.orders_details_add_market_id_get(id=order_id)

    def get_market_recharge_order_datails(self, order_id):
        return self.api_order_management.orders_details_recharge_market_id_get(id=order_id)

    def recharge_market(self, market_id, alloted_time):
        req = PutMarketRechargeRequest(market_id=market_id, allotted_time=alloted_time)
        return self.api_exchange_management.exchange_recharge_market_put(body=req)

    def get_tenant_indiv_audits_result(self, audit_id):
        return self.api_audit.tenant_audits_results_id_individual_audit_get(id=audit_id)

    def get_tenant_indiv_re_audits_result(self, audit_id):
        return self.api_audit.tenant_audits_results_id_individual_re_audit_get(id=audit_id)

    def get_indiv_audits_result(self, account_id):
        return self.api_audit.accounts_individual_audits_id_get(id=account_id)
    
    def get_indiv_audits_pending_num(self):
        rsp = self.api_audit.accounts_individual_audits_tasks_audit_pending_num_get()
        
        return rsp.pending_num


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    for item in _staff.list_tags():
        if item.name == CONFIG.MY_TAG:
            break
    else:
        _staff.create_tag(tag=CONFIG.MY_TAG, other_language=[{"key": "英语", "value": "public_chain"}])
    print("sponsor list:")
    print(_staff.list_sponsors())
    print("project list:")
    print(_staff.list_projects())
    print("tags list:")
    print(_staff.list_tags())
    print("finished ====>")


if __name__ == '__main__':
    main()
