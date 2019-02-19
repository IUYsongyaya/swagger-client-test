# -*- coding: utf-8 -*-
# @File :  profitloss_data.py
# @Author : lh
# @time : 18-11-14 下午8:14

import random
import pytest

QUOTATIONS_FIELDS = ("market_id,price,entrust_type,trade_type,"
                     "volume,trigger_price,auto_cancel_at,exchange_ids,coin_id,sell_coin_id,trading_area_id,symbol")

FIELDS = ("market_id,price,entrust_type,trade_type,"
          "volume,trigger_price,auto_cancel_at")


def get_random_price_and_volume(precision=2, price_start=10, volume_start=1):
    price_range = (price_start + 100, price_start * 100)
    volume_range = (volume_start + 100, volume_start * 100)
    if precision:
        return round(random.uniform(*price_range), int(precision)), round(random.uniform(*volume_range),
                                                                          8 - int(precision))
    else:
        return int(random.uniform(*price_range)), int(random.uniform(*volume_range))


COINID = '1'
SELLCOIND = '7'
MARKETID = '61'
EXCHANGEID = '4'
TRADINGAREAID = '51'
SYMBOL = '4:XLM/USDT'
TENANT = 'BitMan'
TENANTPWD = 'ZXY_tenant_pwd'

BUY = 'buy'
SELL = 'sell'

TESTLESSMARKET = '171'
TESTLESSEXCHANGEID = '4'
TESTLESSSELLCOIND = '360'
TESTLESSCOINID = '8'
TESTLESSTRADINGAREAID = '169'
# 委托类型 limit限价 market市价 profit_Loss止盈止损 time_Limit限时委托
EntrustTypeLimit = 'limit'
EntrustTypeMarket = 'market'
EntrustTypeProfitLoss = 'profit_Loss'
EntrustTypeTimeLimit = "time_limit"

# 止损:当前价小于等于触发价(64)，开始委托 if（当前价<=64）挂起限价委托
# buy
# 1 成交价<=触发价、委托价>=卖一时，下一笔买单下单成功，并会与卖一进行撮合成功，生成成交记录有历史订单记录, "same_multi_buy"
price, volume = get_random_price_and_volume()
data1 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)

# 2 成交价<=触发价、委托价<卖一时，下一笔买单下单成功，挂单在买盘的盘口数据中，生成一条委托记录, "same_multi_buy"
price, volume = get_random_price_and_volume()
data2 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)
# 3 委托成功，也在盘口数据中，进行撤单在委托记录中选择需要撤单的订单，点击撤销按钮撤单成功，生成一笔历史委托订单，订单状态为撤销, "same_multi_buy"
price, volume = get_random_price_and_volume()
data3 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)
# 4 成交价<=触发价、委托价与数量>卖一时，下一笔买单，部分撮合，并挂剩余单下单成功，并会与卖一进行撮合成功，生成多笔成交记录与一笔委托订单记录
#  ，并且还有部分订单挂在盘口数据中
# 5 成交价<=触发价、委托价与数量>卖一时，下一笔买单，部分撮合，并撤销剩余单下单成功，并会与卖一进行撮合成功，生成多笔成交记录与一笔历史委托记录
#  ，历史委托记录状态显示为撤单, "commbuy_multi_eqt_sell1"
price, volume = get_random_price_and_volume()
data5 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)

# sell
# 6 成交价<=触发价，下一笔卖单下单成功，显示在委托列表记录中，查看下单记录信息
# 7 成交价<=触发价、委托价<=买一时，下一笔卖单 下单成功，并会与卖一进行撮合成功，生成成交记录有历史订单记录, "same_multi_sell"
price, volume = get_random_price_and_volume()
data7 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)
# 8 成交价<=触发价、委托价>买一时，下一笔卖单 下单成功，挂单在买盘的盘口数据中，生成一条委托记录, "same_multi_sell"
price, volume = get_random_price_and_volume()
data8 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)
# 9 委托成功，也在盘口数据中，进行撤单 在委托记录中选择需要撤单的订单，点击撤销按钮撤单成功，生成一笔历史委托订单，订单状态为撤销, "same_multi_sell"
price, volume = get_random_price_and_volume()
data9 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)

# 10 成交价<=触发价、委托价<买一、数量>买一时，下一笔卖单，部分撮合，并挂剩余单下单成功，并会与卖一进行撮合成功
#   ，生成多笔成交记录与一笔委托订单记录，并且还有部分订单挂在盘口数据中
# 11 成交价<=触发价、委托价<买一、数量>买一时，下一笔卖单，部分撮合，并撤销剩余单下单成功，并会与卖一进行撮合成功
#   ，生成多笔成交记录与一笔历史委托记录，历史委托记录状态显示为撤单, "commsell_multi_eqt_buy1"
price, volume = get_random_price_and_volume()
data11 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)

# 止盈:当前价大于等于触发价(66)，开始委托 if（当前价>=66）挂起限价委托
# buy
# 12 成交价>=触发价，下一笔买单下单成功，显示在委托列表记录中，查看下单记录信息
# 13 成交价>=触发价、委托价>=卖一时，下一笔买单 下单成功，并会与卖一进行撮合成功，生成成交记录有历史订单记录, "same_multi_buy"
price, volume = get_random_price_and_volume()
data13 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)
# 14 成交价>=触发价、委托价<卖一时，下一笔买单 下单成功，挂单在买盘的盘口数据中，生成一条委托记录, "same_multi_buy"
price, volume = get_random_price_and_volume()
data14 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)
# 15 成交价>=触发价、委托价与数量>卖一时，下一笔买单，部分撮合，并挂剩余单下单成功，并会与卖一进行撮合成功
#   ，生成多笔成交记录与一笔委托订单记录，并且还有部分订单挂在盘口数据中
# 16 成交价>=触发价、委托价与数量>卖一时，下一笔买单，部分撮合，并撤销剩余单下单成功，并会与卖一进行撮合成功, "commbuy_price_eqt_sell1"
#   ，生成多笔成交记录与一笔历史委托记录，历史委托记录状态显示为撤单
price, volume = get_random_price_and_volume()
data16 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)

# sell
# 17 成交价>=触发价、委托价<=买一时，下一笔卖单 下单成功，并会与卖一进行撮合成功，生成成交记录有历史订单记录, "same_multi_sell"
price, volume = get_random_price_and_volume()
data17 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)
# 18 成交价>=触发价、委托价>买一时，下一笔卖单 下单成功，挂单在买盘的盘口数据中，生成一条委托记录, "same_multi_sell"
price, volume = get_random_price_and_volume()
data18 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)
# 19 成交价>=触发价、委托价<买一、数量>买一时，下一笔卖单，部分撮合，并挂剩余单 下单成功，并会与卖一进行撮合成功
# ，生成多笔成交记录与一笔委托订单记录,并且还有部分订单挂在盘口数据中
# 20 成交价>=触发价、委托价<买一、数量>买一时，下一笔卖单，部分撮合，并撤销剩余单 下单成功，并会与卖一进行撮合成功, "commsell_price_eql_buy1"
#   ，生成多笔成交记录与一笔历史委托记录，历史委托记录状态显示为撤单
price, volume = get_random_price_and_volume()
data20 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)

# 21 成交价<=触发价、委托价>=卖一时，下一笔买单下单成功，并会与卖一进行撮合成功，生成成交记录有历史订单记录,查询后台管理记录和租户平台交易记录, "same_multi_price_buy"
price, volume = get_random_price_and_volume()
data21 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, None, None)

# 22下单时间>=撤单时间，下买单无法下单
price, volume = get_random_price_and_volume()
data22 = pytest.param(MARKETID, price, EntrustTypeTimeLimit, BUY, volume, "", "")
# 23下单时间<撤单时间（1分钟）、委托价格>=卖一，下买单,走限价业务买单逻辑，先挂单业务不变，提交单用提交，只需要测试成交场景
price, volume = get_random_price_and_volume()
data23 = pytest.param(MARKETID, price, EntrustTypeTimeLimit, BUY, volume, "", "")
# 24下单时间<撤单时间（1分钟）、委托价格<卖一，下卖单,走限价业务卖单逻辑，先挂单业务不变，提交单用提交，只需要测试挂单场景
price, volume = get_random_price_and_volume()
data24 = pytest.param(MARKETID, price, EntrustTypeTimeLimit, SELL, volume, "", "")
# 25下单时间>=撤单时间，下卖单,无法下单
price, volume = get_random_price_and_volume()
data25 = pytest.param(MARKETID, price, EntrustTypeTimeLimit, SELL, volume, "", "")
# 26下单时间<撤单时间（1分钟）、委托价格>=买一，下买单,走限价业务卖单逻辑，先挂单业务不变，提交单用提交，只需要测试挂单场景
price, volume = get_random_price_and_volume()
data26 = pytest.param(MARKETID, price, EntrustTypeTimeLimit, BUY, volume, "", "")
# 27下单时间<撤单时间（1分钟）、委托价格<买一，下卖单,走限价业务买单逻辑，先挂单业务不变，提交单用提交，只需要测试成交场景
price, volume = get_random_price_and_volume()
data27 = pytest.param(MARKETID, price, EntrustTypeTimeLimit, SELL, volume, "", "")

# 28行情数据
price, volume = get_random_price_and_volume()
data28 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, None, None, EXCHANGEID, COINID, SELLCOIND,
                      TRADINGAREAID, SYMBOL)
# 29测试less撮合单数据
price, volume = get_random_price_and_volume()
data29 = pytest.param(TESTLESSMARKET, price, EntrustTypeLimit, BUY, volume, None, None, TESTLESSEXCHANGEID,
                      TESTLESSCOINID, TESTLESSSELLCOIND, TESTLESSTRADINGAREAID, SYMBOL)

stoploss_buy = [
    data1
]

stop_buy_fail = [
    data2
]

stoploss_buy_fail = [
    data7
]

stoploss_sell = [
    data8
]

stoploss_sell_fail = [
    data8
]

stoploss_cancel_sell_order = [
    data3
]

stoploss_multi_differ_buy = [
    data5
]

stoploss_multi_differ_sell = [
    data11
]

stopprofit_buy = [
    data13
]

stopprofit_buy_fail = [
    data14
]
stopprofit_sell = [
    data17
]

stopprofit_sell_fail = [
    data18
]

stopprofit_cancel_buy_order = [
    data9
]

stopprofit_multi_differ_buy = [
    data16
]

stopprofit_multi_differ_sell = [
    data20
]

staff_tenant_stopprofit = [
    data21
]
quotation_data = [
    data28
]
test_less_entrust_data = [
    data29
]
