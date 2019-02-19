# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-17
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


class Contacts:
    
    def __init__(self):
        super().__init__()
    
    def contacts(self, project_id, exchange_id, sponsor):
        logger.info("============contacts project:%s with exchange_id:%s" % (project_id, exchange_id))
        print("exchange_id:", exchange_id)
        print("sponsor:", sponsor)
        assert project_id, "project_id must not null"
        assert exchange_id, "exchange_id must not null"
        assert sponsor, "sponsor must not null"
        req = dict(
            exchangeId=exchange_id,
            projectId=project_id,
            sponsor=sponsor
        )
        try:
            self.api_contacts.contacts_post(body=req)
        except self.ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "对接关系已存在":
                pass
            else:
                raise

    def check_contact(self, project_id, exchange_id):
        res = self.api_contacts.contacts_check_get(project_id, exchange_id)
        print("project:", project_id)
        print("exchange:", exchange_id)
        print("result:", res.result)
        return res.result
    
    def contact_accept(self, contact_id, status):
        payload = {
            "contactId": contact_id,
            "status": status
        }
        self.api_contacts.contacts_put(body=payload)