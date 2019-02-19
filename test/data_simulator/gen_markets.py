# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-23

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


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)

    pprint(project_items)

    _ventures = list()
    _projects = list()

    for i, prj in enumerate(project_items):
        _venture = Venture(i)
        _ventures.append(_venture)
        _project = _venture.get_project(0, project_name=prj["project_name"])
        _projects.append(_project)

    coins_id = dict()
    coins_id["USDT"] = 1
    for coin in COINS[1:]:
        for p in _projects:
            print("p.short_name:%s vs coin:%s" % (p.short_name, coin))
            if p.short_name == coin.upper():
                coins_id[coin.upper()] = p.coin_id
                break
        else:
            assert 0, "No such coin:%s" % coin

    pprint(coins_id)
    _tenants = list()
    for i, exch in enumerate(exchange_items):
        _tenant = Tenant(i)
        _exchange = _tenant.get_exchange()
        for _project in _projects:
            _tenant.contacts(project_id=_project.project_id, exchange_id=_exchange.exchange_id, sponsor="tenant")
        for market_index, market in enumerate(market_items[i]):
            to_sell = market[0].upper()
            to_buy = market[1].upper()
            print("try to create %s/%s" % (to_sell, to_buy))
            _market = _tenant.get_market(buy=coins_id[to_buy], sell=coins_id[to_sell])
            if not _market:
                _faucet = Faucet(_tenant.token_mgr.token, _tenant.api_account.api_client.configuration.host)
                _faucet.free_charge(coin_id=coins_id["USDT"], amount=1000000000)
                _market, order_id = _tenant.create_market(coins_id[to_buy], coins_id[to_sell], "6", "0")
            logger.info(
                "==========  Tenant(%u) create Market(%s) Done ==========" % (i, _market.market_id))


if __name__ == '__main__':
    main()
