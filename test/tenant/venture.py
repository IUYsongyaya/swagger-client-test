#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-13
import json
import logging
from swagger_client.venture import *
from swagger_client.venture.rest import ApiException

from common.pager import query_items, list_items, query_unique_item
from test.tenant.account import Account
from test.tenant.asset import Asset
from test.tenant.project import Project
from test.tenant.contacts import Contacts
from test.tenant.instance import Instance, get_templated_attrs
from test.tenant.id_settings import *
from common.photo import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


class Venture(Instance, Account, Asset, Contacts):
    
    _instances = dict()
    
    # ================= platform depend model type =================

    PostRegisterRequest = PostRegisterRequest
    ApiException = ApiException
    PostLoginRequest = PostLoginRequest
    PostBindPhoneRequest = PostBindPhoneRequest
    PostIndividualCertificationRequest = PostIndividualCertificationRequest
    PutProjectRequest = PutProjectRequest
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

        self.api_account = AccountApi()
        self.api_contacts = ContactsApi()
        self.api_project = ProjectApi()
        self.api_project_management = ProjectManagementApi()
        self.api_news_management = NewManagementApi()
        self.api_report_management = ReportManagementApi()
        self.api_sponsors_management = SponsorsManagermentApi()
        self.api_verification = VerificationApi()
        self.api_asset_management = AssetManagementApi()
        self.api_announcement_management = AnnouncementManagementApi()
        
    def list_coins(self, init):
        rsp = self.api_project.projects_coins_init_get(init=init)
        return rsp
    
    def get_usdt_coin_id(self):
        coin_list = self.list_rechargable()
        for coin in coin_list:
            if coin["shortName"] == "USDT" or coin["shortName"] == "usdt":
                return coin["coinId"]
        return None
        
    def list_sponsors(self):
        return list_items(self.api_sponsors_management.sponsors_get)
    
    def query_sponsor_id(self, sponsor_name):
        sponsors = self.list_sponsors()
        ids = [s.id for s in sponsors if s.name == sponsor_name]
        return ids[0]

    def list_applications(self):
        return list_items(self.api_project.applications_get, order_rule="appliedAt")

    def set_sponsor(self, sponsor_id, application_id):
        assert isinstance(application_id, str)
        req = dict(
            sponsorId=sponsor_id
        )
        self.api_project.applications_id_set_sponsor_put(id=application_id, sponsor_request=req)

    def contact_project_with_exchange(self, project_id, exchange_id, sponsor):
        payload = {
            "exchange_id": exchange_id,
            "project_id": project_id,
            "sponsor": sponsor
        }
        self.api_contacts.contacts_post(body=payload)
    
    def check_cert_accepted(self):
        rsp = self.api_account.accounts_account_info_get()
        print(rsp)
        return rsp.certification_audit.certification_status == "accepted"

    def list_projects(self):
        return list_items(self.api_project.projects_get)

    def list_contacts(self, project_id, sponsor):
        return list_items(self.api_project_management.projects_id_contacts_get, id=project_id, sponsor=sponsor)

    def query_contact(self, project_id, sponsor, filter=None):
        return query_unique_item(self.api_project_management.projects_id_contacts_get,
                                 id=project_id,
                                 sponsor=sponsor,
                                 filter=filter)

    def get_project(self, index=None, project_name=None):
        assert isinstance(index, int) or project_name, "Index or project name must be set one at least"
        if not project_name:
            project_name = get_templated_attrs(Project, index)["project_name"]
        for prj in self.list_projects():
            print("prj[%s] vs project[%s]" %(prj.project_name, project_name))
            if prj.project_name == project_name:
                details = self.get_details(prj.project_id)
                _project = Project(attrs=dict(
                    project_name=details.project_info.project_name,
                    coin_id=details.coin_info.id,
                    project_id=details.project_info.id,
                    short_name=details.coin_info.short_name,
                    full_name=details.coin_info.full_name,
                    sponsor_id=details.sponsor_info.sponsor_id))
                return _project

    def create_project(self, index=None, attrs=None):
        if not attrs:
            _attrs = get_templated_attrs(Project, index)
        else:
            _attrs = attrs.copy()
        project_name = _attrs.get("project_name")
        full_name = _attrs.get("full_name")
        short_name = _attrs.get("short_name")
        rsp = self.api_project.applications_check_project_name_post(project_name=project_name)
        print("check project name: ", rsp.result)
        print("project_name:%s  full_name:%s  short_name:%s" % (project_name, full_name, short_name))
        payload = {
            'project_name': project_name,
            'description': _attrs.get("description", "") or f'{project_name} go go go',
            'official_website': attrs.get("official_website", "") or f'www.{project_name}.com',
            'white_paper_key': _attrs.get("white_paper_key", "") or f'1234555',
            'area_code': attrs.get("area_code", "") or '+86',
            'project_poster_key': attrs.get("project_poster_key", "") or "1234555",
            'cellphone': attrs.get("cellphone", "") or '13510022445',
            'telephone': attrs.get("telephone", "") or '12874846',
            'email': attrs.get("email", "") or '1234832456@qq.com',
            'full_name': full_name,
            'short_name': short_name,
            'issue_price': attrs.get("issue_price", "") or '2.24545',
            'issued_volume': attrs.get("issued_volume", "") or '1000000',
            'circulation_volume': attrs.get("circulation_volume", "") or '1000000',
            'issued_date': attrs.get("issued_date", "") or '2018-08-08',
            "coin_logo_key": attrs.get("coin_logo_key", "") or PHOTO_KEY,
            'blockchain_type': attrs.get("blockchain_type", "") or 'public_chain',
            'data_link': attrs.get("data_link", "") or f'www.{project_name}.com',
            'block_browser': attrs.get("block_browser", "") or f'http://coin.{project_name}.com'
        }
        req = ApplicationRequest(**payload)
        # 申请项目
        try:
            res = self.api_project.applications_post(body=req)
        except ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "项目名称已经存在":
                logger.warn("项目正在申请中，属于自己的项目,但是还未完成")
                application_id = self.query_application_id(project_name=project_name)
                _attrs["application_id"] = application_id
            else:
                raise
        else:
            _attrs["application_id"] = res.id
        return Project(0, attrs=_attrs)

    def get_details(self, project_id):
        # logger.info("project details for project_id:%s" % (str(project_id)))
        rsp = self.api_project.projects_id_get(str(project_id))
        return rsp

    def update_project_setting(self, project_id, open=True, access_method="verification"):
        req = PutProjectRequest(setting=dict(open=open, accessMethod=access_method))
        return self.api_project.projects_id_put(id=project_id, type="setting", body=req)

    def update_project_info(self, project_name):
        project = self.get_project(project_name=project_name)
        return project

    def query_project_id(self, project_name):
        projects = self.list_projects()
        ids = [p.project_id for p in projects if p.project_name == project_name]
        return ids[0]

    def query_application_id(self, project_name):
        applications = self.list_applications()
        ids = [ap.id for ap in applications if ap.project_name == project_name]
        if ids:
            return ids[0]

    def list_announcements(self, project_id):
        return list_items(self.api_announcement_management.announcements_project_id_get, project_id=project_id)
    
    def query_announcement(self, project_id, filter=None):
        return query_items(self.api_announcement_management.announcements_project_id_get, project_id=project_id, filter=filter)

    def query_unique_announcement(self, project_id, filter=None):
        return query_unique_item(self.api_announcement_management.announcements_project_id_get, project_id=project_id, filter=filter)

    def post_announcement(self, title, content, language, project_id):
        req = PostNoticesRequest(title=title, content=content, language=language, project_id=project_id)
        self.api_announcement_management.announcements_post(body=req)
    
    def get_announcement(self, announcement_id):
        rsp = self.api_announcement_management.announcements_id_notice_get(id=announcement_id)
        return rsp
    
    def delete_announcement(self, announcement_id):
        self.api_announcement_management.announcements_id_notice_delete(id=announcement_id)

    def get_application(self, application_id):
        return self.api_project.applications_id_get(id=application_id)

    def get_application_num(self, status="undone"):
        rsp = self.api_project.applications_num_get(status=status)
        return rsp.result
    
    def list_market_by_coin_id(self, coin_id):
        return list_items(self.api_project_management.get_project_market_list, coin_id=coin_id)
    
    def list_exchanges_without_contact_by_project_id(self, project_id):
        return list_items(self.api_project_management.projects_id_exchanges_get, id=project_id)
    
    def query_exchanges_without_contact_by_project_id(self, project_id, filter=None):
        return query_items(self.api_project_management.projects_id_exchanges_get, id=project_id, filter=filter)

    def query_unique_exchange_without_contact_by_project_id(self, project_id, filter=None):
        return query_unique_item(self.api_project_management.projects_id_exchanges_get, id=project_id, filter=filter)

    def get_inviting_contact_num(self, project_id):
        rsp = self.api_contacts.contacts_invite_number_get(id=project_id)
        return rsp.result
        
        
def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    _venture = Venture(CONFIG.VENTURE_INDEX)
    _venture.request_individual_cert()
    _venture.get_usdt_coin_id()
    _staff.verify_individual(identity=_venture.identity, approval="ACCEPTED")
    logger.info("==  Venture(%u) ready  ==" % CONFIG.VENTURE_INDEX)
    print(_venture.api_account.accounts_account_info_get())
    print("project[%u] ====> %s" % (CONFIG.PROJECT_INDEX, _venture.get_project(index=CONFIG.PROJECT_INDEX)))
    
    
if __name__ == '__main__':
    from test.tenant.staff import Staff
    main()
    

