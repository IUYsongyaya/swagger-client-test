# !/usr/bin/env python3
# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-22

import json
import logging
from test.tenant.tenant import Tenant
from test.tenant.main import Main
from test.tenant.faucet import Faucet
from test.tenant.sponsor import Sponsor
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.instance import get_templated_attrs
from test.tenant.id_settings import *
from test.data_simulator.data.data_sponsors import sponsor_items

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    logger.info("==========  Staff(%u) ready  ==========" % CONFIG.STAFF_INDEX)
    with open(CUR_DIR + "/data/sponsor_logos/photo.json") as f:
        sponsor_logos = json.loads(f.read())
    if len(sponsor_logos) != len(sponsor_items):
        assert "sponsor logo count:%u vs sponsors count:%u" % (len(sponsor_logos), len(sponsor_items))
    
    for i, sponsor in enumerate(sponsor_items):
        info = get_templated_attrs(Sponsor, i)
        info["name"] = sponsor["name"]
        assert _staff.create_sponsor(**info), "Create sponsor:%u failed" % i
        s = Sponsor(i, attrs=info)
        print("%u ===> %s:" % (i,sponsor["name"]), s)
    
    for i, sponsor in enumerate(sponsor_items):
        for sp in _staff.list_sponsors():
            if sp.name == sponsor["name"]:
                info = get_templated_attrs(Sponsor, i)
                print("sponsor_id:", sp.id)
                _staff.update_sponsor(sponsor_id=sp.id, logo=sponsor_logos[i]["key"], website=sponsor["official_url"],
                                      summary=sponsor["summary"], phone=info["phone"])


if __name__ == '__main__':
    main()
