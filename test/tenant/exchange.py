#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-6
import json
import logging

from common.photo import *
from test.tenant.instance import get_templated_attrs
from test.tenant.id_settings import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


class Exchange:

    attrs_template = dict(
        nationality="CN",
        exchange_name=lambda name, index: "%s_exch_%u" % (CONFIG.TESTER, index),
        tag_idx=0,
        tags=CONFIG.MY_TAG,
        logo_url=PHOTO_URL,
        logo_key=PHOTO_KEY,
        exchange_id="",
    )

    def __init__(self, index=None, attrs=None):
        attrs = attrs or dict()
        if index is None:
            assert attrs.get("exchange_name", ""), "Index and exchange name can't be None at the same time"
            index = 0
         
        for key, val in get_templated_attrs(type(self), index).items():
            if key not in attrs:
                attrs[key] = val
            setattr(self, key, attrs[key])
            
    def __repr__(self):
        cls_name = f"< {type(self).__name__}"
        attrs_info = ""
        for key, val in self.__dict__.items():
            if not callable(val):
                attrs_info += f"  {key}: {val}  "
        else:
            attrs_info += " >"
        return cls_name+attrs_info
    

def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    
    _exchange = _tenant.get_exchange()
    if not _exchange:
        _exchange = _tenant.create_exchange()

    audits = _staff.query_audits_tenant(uid=_tenant.account_id, status="audit")

    for au in audits:
        print(au)
    for audit in audits:
        _staff.audits_tenants(task_id=audit.id, approval="approved")

        result = _staff.get_tenant_indiv_audits_result(audit_id=audit.id)
        assert result.audit_status == "approved"

    re_audits = _staff.query_audits_tenant(uid=_tenant.account_id, status="re_audit")
    for re_audit in re_audits:
        _staff.reaudits_tenants(task_id=re_audit.id, approval="approved")

        result = _staff.get_tenant_indiv_re_audits_result(audit_id=re_audit.id)
        assert result.re_status == "approved"
    print("exchange ==============>", _tenant.get_exchange())
    assert _tenant.is_exchange_approved(), "exchange should be approved here"

    # logger.info("==========  Exchange(%s) exchange_id:%s ready ==========" % (_exchange.exchange_id))
    

if __name__ == '__main__':
    from test.tenant.staff import Staff
    from test.tenant.tenant import Tenant
    main()
