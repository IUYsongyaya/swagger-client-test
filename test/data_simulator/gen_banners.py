# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-24


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
from test.data_simulator.data.data_markets import market_items, COINS
from test.data_simulator.data.data_exchanges import exchange_items
from test.data_simulator.data.data_projects import project_items
from test.tenant.id_settings import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


FRONT_PAGE_TITLE = "金猫交易系统"
FRONT_PAGE_URL = "http://www.kinmall.com"

EXCHANGE_TITLE = "生态系统"
EXCHANGE_URL = "http://www.kinmall.com"

EXCHANGE_INTERNAL_TITLE = "公平透明"
EXCHANGE_INTERNAL_URL = "http://www.kinmall.com"


def load_banners_json(directory):
    with open(CUR_DIR + f"/data/{directory}/photo.json", "r") as f:
        return json.loads(f.read())


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    for ban in _staff.list_banners():
        _staff.delete_banner(ban.id)

    for i, ban in enumerate(load_banners_json("web_front_banners")):
        _staff.add_banner(title=FRONT_PAGE_TITLE, platform="pc", position="homepage", banner=ban["key"], order=i,
                          url=FRONT_PAGE_URL, language="zh_cn", status=True)

    for i, ban in enumerate(load_banners_json("web_exchange_banners")):
        _staff.add_banner(title=FRONT_PAGE_TITLE, platform="pc", position="exchange_homepage", banner=ban["key"], order=i,
                          url=FRONT_PAGE_URL, language="zh_cn", status=True)

    for i, ban in enumerate(load_banners_json("app_front_banners")):
        _staff.add_banner(title=EXCHANGE_TITLE, platform="mobile", position="homepage", banner=ban["key"], order=i,
                          url=EXCHANGE_URL, language="zh_cn", status=True)

    for i, ban in enumerate(load_banners_json("app_exchange_banners")):
        _staff.add_banner(title=EXCHANGE_TITLE, platform="mobile", position="exchange_homepage", banner=ban["key"],
                          order=i, url=EXCHANGE_URL, language="zh_cn", status=True)

    for i, exchage in enumerate(exchange_items):
        _tenant = Tenant(i)
        for ban in _tenant.list_banners():
            _tenant.delete_banner(banner_id=ban.id)
        for ban in load_banners_json("web_exchange_private_banners"):
            _tenant.add_banner(title=EXCHANGE_INTERNAL_TITLE, url=EXCHANGE_INTERNAL_URL, banner=ban["key"])



if __name__ == '__main__':
    main()
