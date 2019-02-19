import random
import pytest

from swagger_client.main.api.entrust_api import EntrustApi  # noqa: E501
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from swagger_client.tenant.api.market_management_api import MarketManagementApi
from swagger_client.tenant.api.exchange_entrust_api import ExchangeEntrustApi
from .data import (FIELDS, EntrustTypeMarket,  get_random_price_and_volume, market_test_data_set1, market_test_data_set2, market_test_data_set3)

api = EntrustApi()
tenant_market_api = MarketManagementApi()
tenant_exchange_api = ExchangeEntrustApi()


class TestMarketEntrust:
    @pytest.mark.parametrize(FIELDS, market_test_data_set1)
    def test_one_buy_one_sell(self, market_id, price, entrust_type, trade_type,
                              volume, trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        # payload.trigger_price = trigger_price
        payload.volume = 1000_00
        # payload.auto_cancel_at = auto_cancel_at
        # login
        special_info = special_login([api, tenant_market_api, tenant_exchange_api])
        payload.market_id = special_info['market_id']
        # 清空

        before_market_buy = api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        before_makret_sell = api.entrusts_post(body=payload)
        # 恢复限价

        payload.entrust_type = entrust_type
        payload.trade_type = trade_type

        precision = special_info['precision']
        inc_range = 1 / (10 ** (int(precision)-1))
        sub_range = 1 / (10 ** (int(precision)-1))

        if 'buy' in volume_flag:
            payload.trade_type = 'buy'

        else:
            payload.trade_type = 'sell'

        payload.price, payload.volume = get_random_price_and_volume(precision)
        first = api.entrusts_post(body=payload)  # 限价单
        first_id = first.order_id

        if 'buy' in volume_flag:
            payload.trade_type = 'sell'
            payload.entrust_type = EntrustTypeMarket
        else:
            payload.trade_type = 'buy'
            payload.trade_type = EntrustTypeMarket

        # 获取服务费率
        market_rate = tenant_market_api.markets_id_get(payload.market_id)
        if 'eq' in volume_flag:
            market_volume = round(payload.volume * payload.price, int(precision))
            fee_volume = round(market_volume * float(market_rate.totalRate), int(precision))
        elif 'gt' in volume_flag:
            # 买方大于卖方
            payload.volume = round(sub_range, int(precision))
            market_volume = round(payload.volume * payload.price, int(precision))
            fee_volume = round(market_volume * float(market_rate.totalRate), int(precision))
        else:
            # 买方小于卖方
            payload.volume = round(payload.volume + inc_range, int(precision))
            market_volume = round(payload.volume * payload.price, int(precision))
            fee_volume = round(market_volume * float(market_rate.totalRate), int(precision))

        payload.volume = round(market_volume, int(precision))
        r = api.entrusts_post(body=payload)
        second_trade_id = r.order_id

        first_order_info = tenant_exchange_api.exchange_entrusts_get(id=first_id)

        assert first_order_info.status == 'done'
        # 获取委托单详情
        second_order_info = tenant_exchange_api.exchange_entrusts_get(id=second_trade_id)
        # 市价单
        assert second_order_info.volume == first_order_info.volume
        trade_info = api.trades_get(order_id=first_id)
        # 手续费验证
        assert fee_volume == trade_info.items.fee

    # 44 先挂多笔价格不同限价买单，提交一笔市价卖出单，买卖单数量一致  different_price_buy_eq
    # 45 先挂多笔价格不同限价买单，提交一笔市价卖出单，买方多余卖方     different_price_buy_gt
    # 46 先挂多笔价格不同限价买单，提交一笔市价卖出单，卖方多余买方     different_price_buy_lt

    # 53 先挂多笔价格不同限价卖单，提交一笔市价买单，买卖单数量一致     different_price_sell_eq
    # 54 先挂多笔价格不同限价卖单，提交一笔市价买单，买方多余卖方      different_price_sell_lt
    # 55 先挂多笔价格不同限价卖单，提交一笔市价买单，卖方多余买方      different_price_sell_gt
    @pytest.mark.parametrize(FIELDS, market_test_data_set3)
    def test_different_price(self, market_id, price, entrust_type, trade_type,
                             volume, trigger_price, auto_cancel_at, volume_flag, special_login):
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        # payload.trigger_price = trigger_price
        payload.volume = 1000_00
        # payload.auto_cancel_at = auto_cancel_at
        # login
        special_info = special_login([api, tenant_market_api, tenant_exchange_api])
        payload.market_id = special_info['market_id']
        # 清空

        before_market_buy = api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        before_makret_sell = api.entrusts_post(body=payload)
        # 恢复限价

        payload.entrust_type = entrust_type
        payload.trade_type = trade_type

        precision = special_info['precision']
        inc_range = 1 / (10 ** (int(precision) - 1))
        sub_range = 1 / (10 ** (int(precision) - 1))

        # buy first
        if 'buy' in volume_flag:
            payload.trade_type = 'buy'
        # sell first
        else:
            payload.trade_type = 'sell'
        trades = []
        for i in range(5):
            payload.price, payload.volume =  get_random_price_and_volume(precision)
            r = api.entrusts_post(body=payload)
            trades.append({'order_id': r['orderId'],
                           'price': payload.price,
                           'volume': payload.volume})

        # 多限价的单子，要依据市价的买卖不同，从卖一往上或者买一往下去验证
        sorted_trades = sorted(trades, key=lambda x: x['price'])

        if 'buy' in volume_flag:
            payload.trade_type = 'sell'
            payload.entrust_type = EntrustTypeMarket
        else:
            payload.trade_type = 'buy'
            payload.trade_type = EntrustTypeMarket

        # 获取服务费率
        market_rate = tenant_market_api.markets_id_get(payload.market_id)
        if 'eq' in volume_flag:
            if 'buy' in volume_flag:
                volume = sum([i['volume'] for i in trades])
            else:
                # 市价买，提供的是资金不是数量，所以需要算汇率
                volume = sum([i['volume'] * i['price'] for i in trades])
            market_volume = round(volume, int(precision))
            fee_volume = round(market_volume * float(market_rate.totalRate), int(precision))
        elif 'gt' in volume_flag:
            # 45 先挂多笔价格不同限价买单，提交一笔市价卖出单，买方多余卖方     different_price_buy_gt
            # 55 先挂多笔价格不同限价卖单，提交一笔市价买单，卖方多余买方      different_price_sell_gt
            if 'buy' in volume_flag:
                volume = sum([i['volume'] for i in trades])
            else:
                # 市价买，提供的是资金不是数量，所以需要算汇率
                volume = sum([i['volume'] * i['price'] for i in trades])
            market_volume = round(volume - sub_range, int(precision))
            fee_volume = market_volume * float(market_rate.totalRate)
        else:
            # 46 先挂多笔价格不同限价买单，提交一笔市价卖出单，卖方多余买方     different_price_buy_lt
            # 54 先挂多笔价格不同限价卖单，提交一笔市价买单，买方多余卖方      different_price_sell_lt
            if 'buy' in volume_flag:
                volume = sum([i['volume'] for i in trades])
            else:
                # 市价买，提供的是资金不是数量，所以需要算汇率
                volume = sum([i['volume'] * i['price'] for i in trades])
            market_volume = round(volume + inc_range, int(precision))
            fee_volume = round(market_volume * float(market_rate.totalRate), int(precision))

        payload.volume = round(market_volume, int(precision))
        r = api.entrusts_post(body=payload)
        single_trade_id = r.order_id

        # 计算逻辑
        # 限价卖单，市价买单，从最低价卖单开始买起, mark_volume是买方币资金
        result = api.entrusts_get(status=['done'])
        trade_ids = [i.id for i in result]
        if 'sell' in volume_flag:
            tmp = market_volume
            for i in sorted_trades:
                # 市价买，提供的是资金不是数量，所以需要算汇率
                tmp = round(tmp-(i["volume"] * i['price']), int(precision))
                if tmp >= 0:
                    assert i['order_id'] in trade_ids

        # 限价买单，市价卖单，从最高价买单开始卖起，提供的mark_volume是卖方币种
        elif 'buy' in volume_flag:
            tmp = market_volume
            for i in sorted_trades[::-1]:
                # 市价卖，提供的是数量不是资金，所以不需要算汇率
                tmp = round(tmp - i["volume"], int(precision))
                if tmp >= 0:
                    assert i['order_id'] in trade_ids
        trade_info = api.trades_get(order_id=single_trade_id)
        # 手续费验证
        assert fee_volume == trade_info.items.fee

    # 41 先挂多笔价格相同限价买单，提交一笔市价卖出单，买卖单数量一致  same_price_buy_eq
    # 42 先挂多笔价格相同限价买单，提交一笔市价卖出单，买方多余卖方   same_price_buy_gt
    # 43 先挂多笔价格相同限价买单，提交一笔市价卖出单，卖方多余买方   same_price_buy_lt
    # 50 先挂多笔价格相同限价卖单，提交一笔市价买单，买卖单数量一致   same_price_sell_eq
    # 51 先挂多笔价格相同限价卖单，提交一笔市价买单，买方多余卖方     same_price_sell_lt
    # 52 先挂多笔价格相同限价卖单，提交一笔市价买单，卖方多余买方     same_price_sell_gt

    @pytest.mark.parametrize(FIELDS, market_test_data_set2)
    def test_same_price(self, market_id, price, entrust_type, trade_type,
                        volume, trigger_price, auto_cancel_at, volume_flag, special_login):

        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        # payload.trigger_price = trigger_price
        payload.volume = 1000_00
        # payload.auto_cancel_at = auto_cancel_at
        # login
        special_info = special_login([api, tenant_market_api, tenant_exchange_api])
        payload.market_id = special_info['market_id']
        # 清空

        before_market_buy = api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        before_makret_sell = api.entrusts_post(body=payload)
        # 恢复限价

        payload.entrust_type = entrust_type
        payload.trade_type = trade_type

        precision = special_info['precision']

        # 添加多笔买单和一笔卖单
        trades = []
        inc_range = 1 / 10 ** (int(precision) - 1)
        sub_range = 1 / 10 ** (int(precision) -1)
        if 'buy' in volume_flag:
            payload.trade_type = 'buy'
        else:
            payload.trade_type = 'sell'
        payload.price, _ = get_random_price_and_volume(precision)
        for i in range(5):
            _, payload.volume = get_random_price_and_volume(precision)
            r = api.entrusts_post(body=payload)
            trades.append({'order_id': r['orderId'],
                           'price': payload.price,
                           'volume': payload.volume})

        if 'buy' in volume_flag:
            payload.trade_type = 'sell'
            payload.entrust_type = EntrustTypeMarket
        else:
            payload.trade_type = 'buy'
            payload.trade_type = EntrustTypeMarket

        # 获取服务费率
        market_rate = tenant_market_api.markets_id_get(payload.market_id)
        if 'eq' in volume_flag:
            if 'buy' in volume_flag:
                volume = sum([i['volume'] for i in trades])
            else:
                # 市价买，提供的是资金不是数量，所以需要算汇率
                volume = sum([i['volume'] * i['price'] for i in trades])
            market_volume = round(volume, int(precision))
            fee_volume = round(market_volume * float(market_rate.totalRate), int(precision))
        elif 'gt' in volume_flag:
            # 42 先挂多笔价格相同限价买单，提交一笔市价卖出单，买方多余卖方   same_price_buy_gt
            # 52 先挂多笔价格相同限价卖单，提交一笔市价买单，卖方多余买方     same_price_sell_gt
            if 'buy' in volume_flag:
                volume = sum([i['volume'] for i in trades])
            else:
                # 市价买，提供的是资金不是数量，所以需要算汇率
                volume = sum([i['volume'] * i['price'] for i in trades])
            market_volume = round(volume - sub_range, int(precision))
            fee_volume = round(market_volume * float(market_rate.totalRate), int(precision))
        else:
            # 43 先挂多笔价格相同限价买单，提交一笔市价卖出单，卖方多余买方   same_price_buy_lt
            # 51 先挂多笔价格相同限价卖单，提交一笔市价买单，买方多余卖方     same_price_sell_lt
            if 'buy' in volume_flag:
                volume = sum([i['volume'] for i in trades])
            else:
                # 市价买，提供的是资金不是数量，所以需要算汇率
                volume = sum([i['volume'] * i['price'] for i in trades])
            market_volume = round(volume + inc_range, int(precision))
            fee_volume = round(market_volume * float(market_rate.totalRate), int(precision))

        payload.volume = round(market_volume)
        r = api.entrusts_post(body=payload)
        single_trade_id = r.order_id

        # 计算逻辑
        # 限价卖单，市价买单，买单能买多少买多少, mark_volume是买方币资金
        result = api.entrusts_get(trade_type='sell', status=['done'])
        trade_ids = [i.id for i in result.items]
        if 'sell' in volume_flag:
            tmp = market_volume  # 提供的资金
            for i in trades:
                # 市价买，提供的是资金不是数量，所以需要乘以汇率
                tmp -= (i["volume"] * i['price'])
                if tmp >= 0:
                    assert i['order_id'] in trade_ids

        # 限价买单，市价卖单，卖单能卖多少卖多少，提供的mark_volume是卖方币种
        elif 'buy' in volume_flag:
            tmp = market_volume  # 提供的货物
            for i in trades[::-1]:  # 先买再卖，从买价最高交易起
                # 市价卖，提供的是数量不是资金，所以不需要算汇率
                tmp -= i["volume"]
                if tmp >= 0:
                    assert i['order_id'] in trade_ids
        trade_info = api.trades_get(order_id=single_trade_id)
        # assert trade_info.items.fee - deviation <= fee_volume <= trade_info.items.fee + deviation
