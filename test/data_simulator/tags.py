#!/usr/bin/env python3
# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-22


import logging
from test.tenant.tenant import Tenant
from test.tenant.main import Main
from test.tenant.faucet import Faucet
from test.tenant.sponsor import Sponsor
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.instance import get_templated_attrs
from test.tenant.id_settings import *
from test.data_simulator.data.data_tags import tag_items

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    
    for t in tag_items:
        for item in _staff.list_tags():
            if item.name == t["name"]:
                break
        else:
            _staff.create_tag(tag=t["name"], other_language=[t["other_language"]])
        logger.info("==========  tag < %s > ready  ==========" % t["name"])


if __name__ == '__main__':
    main()
