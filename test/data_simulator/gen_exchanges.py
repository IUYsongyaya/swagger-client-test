# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-22


import json
import logging
from pprint import pprint
from test.tenant.tenant import Tenant
from test.tenant.main import Main
from test.tenant.faucet import Faucet
from test.tenant.sponsor import Sponsor
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.instance import get_templated_attrs
from test.data_simulator.data.data_exchanges import exchange_items
from test.tenant.id_settings import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    
    with open(CUR_DIR + "/data/exchange_logos/photo.json", "r") as f:
        logos = json.loads(f.read())
        pprint(logos)

    assert len(logos) >= len(exchange_items), "Exchanges logo count is invalid"

    for i, exch in enumerate(exchange_items):
        _tenant = Tenant(i)
        exchange_logo = logos[i]
        _tenant.request_individual_cert()
        _staff.verify_individual(identity=_tenant.identity, approval="ACCEPTED")
        assert _tenant.audit_accepted(), "Audit not accepted!"
        _exchange = _tenant.get_exchange()
        if not _exchange:
            _exchange = _tenant.create_exchange(attrs=dict(
                exchange_name=exch["name"],
                nationality=exch["nationality"],
                tags=exch["tags"],
                logo_url=exchange_logo["url"],
                logo_key=exchange_logo["key"]
            ))

        audits = _staff.query_audits_tenant(uid=_tenant.account_id, status="audit")
        
        for audit in audits:
            print("audit.id:", audit.id)
            _staff.audits_tenants(task_id=audit.id, approval="approved")
    
            result = _staff.get_tenant_indiv_audits_result(audit_id=audit.id)
            assert result.audit_status == "approved"
    
        re_audits = _staff.query_audits_tenant(uid=_tenant.account_id, status="re_audit")
        for re_audit in re_audits:
            _staff.reaudits_tenants(task_id=re_audit.id, approval="approved")
    
            result = _staff.get_tenant_indiv_re_audits_result(audit_id=re_audit.id)
            assert result.re_status == "approved"
    
        if _tenant.is_exchange_approved():
            _exchange = _tenant.update_exchange_info()
        else:
            assert 0, "exchange should be approved here"

        logger.info("==========  exchange_id:%s ready ==========" % _exchange.exchange_id)


if __name__ == '__main__':
    main()
