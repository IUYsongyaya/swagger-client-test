# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-8
import json
from common.pager import list_items


class Asset:
    
    def __init__(self):
        super().__init__()
        
    def query_asset(self):
        rsp = self.api_asset_management.asset_mgmt_assets_get()
        return rsp.asset_info, rsp.estimates
    
    def query_coin_balance(self, coin_id):
        rsp = self.api_asset_management.asset_mgmt_balance_coin_id_get(coin_id=coin_id)
        assert hasattr(rsp, "balance")
        return rsp.balance
    
    def list_rechargable(self):
        rsp = self.api_asset_management.asset_mgmt_coins_rechargeable_lists_get()
        return rsp
    
    def get_coins_config_list(self):
        return list_items(self.api_asset_management.asset_mgmt_coins_get)
    
    def init_coin(self, usdt_price="1", config_id="", address_type="", rc_times=0, wc_times=0, address_url="", txid_url=""):
        assert config_id, "Config id must not null"
        papyload = {
            "usdt_price": str(usdt_price),
            "rc_times": rc_times or 0,
            "wc_times": wc_times or 0,
            "withdraw_rate": "0.01",
            "min_withdraw_fee": "0.01",
            "min_withdraw": "100",
            "max_withdraw": "100000",
            "day_withdraw_total": "10000000",
            "min_recharge": "1",
            "address_tag_switch": False,
            "address_type": address_type or "",
            "address_url": address_url or "",
            "txid_url": txid_url or "http://www.coin.com"
        }
        req = self.PutSystemCoinsInitRequest(**papyload)
        try:
            self.api_asset_management.asset_mgmt_coins_id_init_put(id=config_id, body=req)
        except self.ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "该项目已经初始化":
                pass
            else:
                raise e
    
    def config_coin(self, config_id="", address_type=None, rc_times=0, wc_times=0, address_url=None, txid_url=None):
    
        assert config_id, "config id must not be null"
        assert address_type, "address_type must not be null"
        
        papyload = {
            "rc_times": rc_times or 1,
            "wc_times": wc_times or 1,
            "withdraw_rate": "0.0025",
            "min_withdraw_fee": "0.1",
            "min_withdraw": "20",
            "max_withdraw": "2000",
            "day_withdraw_total": "111",
            "min_recharge": "1",
            "address_tag_switch": False,
            "address_type": address_type,
            "address_url": address_url or "123",
            "txid_url": txid_url or "123123"
        }
        req = self.PutSystemCoinsRequest(**papyload)
        self.api_asset_management.asset_mgmt_coins_id_put(id=config_id, body=req)
        
    def config_coin_rechargable(self, config_id, rechargeable):
        self.api_asset_management.asset_mgmt_coins_id_recharge_put(id=config_id, rechargeable=rechargeable)
    
    def config_coin_withdrawable(self, config_id, withdrawable):
        self.api_asset_management.asset_mgmt_coins_id_withdraw_put(id=config_id, withdrawable=withdrawable)
    
    @property
    def asset_info(self):
        asset_info, _ = self.query_asset()
        return asset_info
    
    @property
    def estimates(self):
        _, estimates = self.query_asset()
        return estimates


