# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-17

from common.pager import list_items


class Dealer:
    
    def __init__(self):
        super().__init__()
    
    def entrust(self, market_id, entrust_type, trade_type, price, volume, trigger_price, auto_cancel_at):
        payload = self.PostEntrustsRequest()
        payload.market_id = market_id
        print('下单价格:', price)
        payload.price = price
        payload.entrust_type = entrust_type
        payload.trade_type = trade_type
        payload.trigger_price = trigger_price
        payload.volume = volume
        payload.auto_cancel_at = auto_cancel_at
        return self.api_entrust.entrusts_post(body=payload)
    
    def buy(self, market_id, price, volume):
        return self.entrust(market_id=market_id, entrust_type="limit", trade_type="buy", price=price, volume=volume, trigger_price=None, auto_cancel_at=None)
    
    def sell(self, market_id, price, volume):
        return self.entrust(market_id=market_id, entrust_type="limit", trade_type="sell", price=price, volume=volume, trigger_price=None,
                            auto_cancel_at=None)
    
    def get_trades(self, order_id, pair):
        return list_items(self.api_entrust.trades_get, order_id=order_id, trading_pair=pair)
    
    def get_orders(self, status=None):
        return list_items(self.api_entrust.entrusts_get, status=status)

    def withdraw(self, order_id):
        return self.api_entrust.entrusts_id_cancel_post(order_id)
        