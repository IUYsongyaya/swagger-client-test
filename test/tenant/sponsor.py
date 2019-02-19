#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-13
import json
import logging
from common.pager import query_items, query_unique_item, list_items
from swagger_client.sponsor import *
from test.tenant.account import Account
from swagger_client.sponsor.rest import ApiException
from test.tenant.instance import Instance, get_templated_attrs
from test.tenant.id_settings import *
from test.tenant.token_manager import TokenManager
from common.photo import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


class Sponsor(Instance, Account):
    _instances = dict()
    
    attrs_template = dict(
        email=lambda name, index: "%s_%s_%u@gmail.com" % (CONFIG.TESTER.upper(), name, index),
        password=lambda name, index: "%s_%s_pwd" % (CONFIG.TESTER.upper(), name),
        name=lambda name, index: "%s%s%u" % (CONFIG.TESTER.upper(), name, index),
        logo=PHOTO_URL,
        account=lambda name, index: "_%s%s%u" % (CONFIG.TESTER.upper(), name, index),
        phone=lambda name, index: "18%s%s%04d" % (platfrom_id(name), name_hash(CONFIG.TESTER.upper()), index),
        identity=lambda name, index: "23233219%s%s%05d" % (platfrom_id(name), name_hash(CONFIG.TESTER.upper()), index))
        
    def __init__(self, index, attrs=None):
        super().__init__(index, attrs=attrs)
        if attrs:
            for key, val in attrs.items():
                setattr(self, key, val)
        self._inited = False
        self.token_mgr = None
        
        self.api_sponsor = SponsorApi()
        self.api_sponsors_management = SponsorsManagermentApi()
        self.api_sponsors_project = SponsorsProjectApi()
        self.api_verification = VerificationApi()
    
    def init_instance(self):
        req = PostLoginRequest(account=self.account, password=self.password, challenge="", seccode="", validate="true")
        rsp = self.api_sponsor.sponsor_login_post(sponsor_login=req)
        base = rsp.base_token
        req = {
            "uri": "mailto:%s" % self.email,
            "code": "666666",
            "baseToken": base
        }
        rsp = self.api_sponsor.sponsor_login_verify_post(post_login_verify_request=req)
        self.token_mgr = TokenManager(rsp.token)
        self.token_mgr.auth_headers(self)
        
        # logger.info("<<<<<   %s   >>>>>", type(self))
        # logger.info("account %s:", self.account)
        # logger.info("password %s:", self.password)
        # logger.info("email : %s", self.email)
        # logger.info("identity : %s", self.identity)
        # logger.info("<<<<<<<<<<<<<>>>>>>>>>>>")
        self._inited = True
    
    def list_applying_projects(self):
        return list_items(self.api_sponsors_project.projects_get)
    
    def query_project_application_id(self, project_name):
        rsp = self.api_sponsors_project.projects_get(page=1, project_name=project_name)
        if rsp.items:
            return rsp.items[0].id
        else:
            return ""
    
    def sponsor_project(self, application_id, status=1):
        req = PutProjectSponsorRequest(id=application_id, status=status, remark="Nice job!")
        try:
            self.api_sponsors_project.projects_sponsor_put(put_project_sponsor_request=req)
        except ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "币种已经存在":
                pass
            else:
                raise
    
    @property
    def inited(self):
        return self._inited


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    sponsor_info = get_templated_attrs(Sponsor, CONFIG.SPONSOR_INDEX)
    if _staff.create_sponsor(**sponsor_info):
        _sponsor = Sponsor(CONFIG.SPONSOR_INDEX)
    else:
        assert 0, "staff create sponsor failed!"


if __name__ == '__main__':
    from test.tenant.staff import Staff
    
    main()
