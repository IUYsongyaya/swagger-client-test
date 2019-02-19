# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-23





import os
import logging
import json
from test.tenant.tenant import Tenant
from test.tenant.main import Main
from test.tenant.faucet import Faucet
from test.tenant.sponsor import Sponsor
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.instance import get_templated_attrs
from test.tenant.id_settings import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)

CUR_DIR=os.path.dirname(os.path.abspath(__file__))

WHITE_PAPER_URL = ""
WHITE_PAPER_KEY = ""


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    url, key = _staff.upload(CUR_DIR+"/data/white_paper_coin.pdf")
    print("white paper => url:%s key:%s" % (url, key))
    

if __name__ == '__main__':
    main()
