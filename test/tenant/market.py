#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-6
import logging
from test.tenant.id_settings import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


class Market:
    
    attrs_template = dict(
        buy_coin="",
        sell_coin="",
        allotted_time="6",
        free_rate="0",
        market_id="")
    
    def __init__(self, attrs=None):
        assert attrs, "Market attrs must not be null"
        for key, val in attrs.items():
            setattr(self, key, val)
            
        logger.info("Market(%s) buy/sell %s/%s" % (self.market_id, self.buy_coin, self.sell_coin))

    def __repr__(self):
        cls_name = f"< {type(self).__name__}"
        attrs_info = ""
        for key, val in self.__dict__.items():
            if not callable(val):
                attrs_info += f"  {key}: {val}  "
        else:
            attrs_info += " >"
        return cls_name + attrs_info


def main():
    _venture = Venture(CONFIG.VENTURE_INDEX)
    usdt_id = _venture.get_usdt_coin_id()
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    _faucet = Faucet(CONFIG.FAUCET_INDEX)
    _project = _venture.get_project(CONFIG.PROJECT_INDEX)
    assert _project, "Must have a project first to create market"
    _market = _tenant.get_market(buy=usdt_id, sell=_project.coin_id)
    print("list markets: ", _tenant.list_markets())
    if not _market:
        _faucet.free_charge(coin_id=_venture.get_usdt_coin_id(), account_id=_tenant.account_id)
        logger.info("==========  Faucet(%s) charge Tenant(%u) Done ==========" % (CONFIG.FAUCET_INDEX, CONFIG.TENANT_INDEX))
        _market, create_order_id = _tenant.create_market(usdt_id, _project.coin_id, "6", "0")
        assert create_order_id, "Market create order id should not be null"
        print("coin verify ==>", _tenant.verify_market_trading_coin(buy_coin=usdt_id, sell_coin=_project.coin_id))
        assert _tenant.list_markets()


if __name__ == '__main__':
    from test.tenant.tenant import Tenant
    from test.tenant.venture import Venture
    from test.tenant.main import Faucet
    main()
