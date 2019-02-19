import random
import pytest

FIELDS = ("market_id,price,entrust_type,trade_type,"
          "volume,trigger_price,auto_cancel_at,volume_flag")


MARKETID = ''
TENANT = 'ZXY_tenant_1@gmail.com'
TENANTPWD = 'ZXY_tenant_pwd'
BUY = 'buy'
SELL = 'sell'


def get_random_price_and_volume(precision=4, price_start=100, volume_start=1):
    price_range = (price_start+100, price_start*100)
    volume_range = (volume_start+100, volume_start*100)
    if precision:
        return round(random.uniform(*price_range), int(precision)), round(random.uniform(*volume_range), 8-int(precision))
    else:
        return int(random.uniform(*price_range)), int(random.uniform(*volume_range))


# 委托类型 limit限价 market市价 profitLoss止盈止损 timeLimit限时委托
EntrustTypeLimit = 'limit'
EntrustTypeMarket = 'market'
EntrustTypeProfitLoss = 'profitLoss'
EntrustTypeTimeLimit = "timeLimit"

# 以下为限价
# 先挂买单
# 1 价格一致，数量一致，成交
# 2 卖高买低，数量一致，不成交，撤回
# 3 卖低买高，数量一致，成交
# 4 卖低买高，买单多，成交部分买单，撤回多余买单
# 5 卖低买高，卖单多，成交部分卖单，撤回多余卖单

# 12 多笔买单一笔卖单，价格一致，买单总数与卖单数目一致
# 13 多笔买单一笔卖单，卖高，买单总数与卖单数目一致， 不成交
# 14 多笔买单一笔卖单，买高，买单总数与卖单数目一致，买单价成交
# 15 多笔买单一笔卖单，买高，买单总数小于卖单，买单价成交，卖单剩余，撤回多余
# 16 多笔买单一笔卖单，买高，买单总数大于卖单，买单价成交， 买单多余，撤回多余
# --
# 先挂卖单
# 7 价格一致，数目一致，成交
# 8 买低卖高， 买卖数量，不成交，均剩余，撤回
# 9 买高卖低，数目一致，成交
# 10 买高卖低，买多卖少， 卖价成交，  买单多余，撤回
# 11 买高卖低，买少卖多， 卖价成交， 卖单多余，撤回

# 17 多笔卖单一笔买单，价格一致，买单总数与卖单数目一致
# 18 多笔卖单一笔买单，卖高，买单总数与卖单数目一致， 不成交
# 19 多笔卖单一笔买单，买高，卖单总数与买单数目一致，卖单价成交
# 20 多笔卖单一笔买单，买高，卖单总数小于买单，卖单价成交，买单剩余，撤回多余
# 21 多笔卖单一笔买单，买高，卖单总数大于买单，卖单价成交， 卖单多余，撤回多余

# 1 卖先 相同数目相同价格
test_data1 = pytest.param(MARKETID, '', EntrustTypeLimit, SELL, '', "", "")
# 2 买先 相同数目相同价格
test_data2 = pytest.param(MARKETID, '', EntrustTypeLimit, BUY, '', "", "")
same_price_volume_entrust_data = [test_data1,
                                  test_data2
                                  ]

# 3 卖低买高，数量一致，成交
test_data3 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "same")
# 4 卖低买高，买单多，成交部分买单，撤回多余买单
test_data4 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "buy_more")
# 5 卖低买高，卖单多，成交部分卖单，撤回多余卖单
test_data5 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "buy_less")
# 9 买高卖低，数目一致，成交
test_data9 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "same")
# 10 买高卖低，买多卖少， 卖价成交，  买单多余，撤回
test_data10 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "sell_less")
# 11 买高卖低，买少卖多， 卖价成交， 卖单多余，撤回
test_data11 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "sell_more")
high_buy_test_success_data1 = [
    test_data4,
    test_data5,
    test_data10,
    test_data11]
high_buy_test_success_data2 = [test_data3,
                               test_data9]

# 14 多笔买单一笔卖单，买高，买单总数与卖单数目一致，买单价成交
price = None
volume = None
test_data14 = pytest.param(EntrustTypeLimit, BUY, "buy_multi_eq_sell")
# 15 多笔买单一笔卖单，买高，买单总数小于卖单，买单价成交，卖单剩余，撤回多余
test_data15 = pytest.param(EntrustTypeLimit, BUY, "buy_multi_lt_sell")
# 16 多笔买单一笔卖单，买高，买单总数大于卖单，买单价成交， 买单多余，撤回多余
test_data16 = pytest.param(EntrustTypeLimit, BUY, "buy_multi_gt_sell")
# 19 多笔卖单一笔买单，买高，卖单总数与买单数目一致，卖单价成交
test_data19 = pytest.param(EntrustTypeLimit, SELL, "sell_multi_eq_buy")
# 20 多笔卖单一笔买单，买高，卖单总数小于买单，卖单价成交，买单剩余，撤回多余
test_data20 = pytest.param(EntrustTypeLimit, SELL, "sell_multi_lt_buy")
# 21 多笔卖单一笔买单，买高，卖单总数大于买单，卖单价成交， 卖单多余，撤回多余
test_data21 = pytest.param(EntrustTypeLimit, SELL, "sell_multi_gt_buy")
high_buy_multi_deal = [test_data14,
                       test_data15,
                       test_data16,
                       test_data19,
                       test_data20,
                       test_data21]

# 17 多笔卖单一笔买单，价格一致，买单总数与卖单数目一致
test_data17 = [pytest.param(MARKETID, price, EntrustTypeLimit, SELL, "", "", "", "multi_sell")]
# 12 多笔买单一笔卖单，价格一致，买单总数与卖单数目一致
test_data12 = [pytest.param(MARKETID, price, EntrustTypeLimit, BUY, "", "", "", "multi_buy")]

# 18 多笔卖单一笔买单，卖高，买单总数与卖单数目一致， 不成交
test_data18 = [pytest.param(EntrustTypeLimit, SELL, "multi_sell")]
# 13 多笔买单一笔卖单，卖高，买单总数与卖单数目一致， 不成交
test_data13 = [pytest.param(EntrustTypeLimit, BUY, "multi_buy")]

#
#
#
#
#
# 先买 再卖

# 22 卖单与买单最低价格一致,买单购买数量与卖单总数量一致,应成交,无沉积单
test_data22 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, "", "", "sell_price_eq_min_buy")

# 23 卖单价格高于买单最高价格,卖单购买数量与买单总数量一致,应不成交,买卖单均剩余,测试剩余单撤销
test_data23 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, "", "", "sell_price_gt_max_buy")

# 24 卖单价格低于买单最高价格,且高于买单最低价格,且等于某一中间买单价格,卖单出售数量等于,高于卖单价格的所有买单总数量,均应以买单价格成交,买单剩余,核对数据,测试剩余单撤销
# 25 卖单价格低于买单最高价格,且高于买单最低价格,且等于某一中间买单价格,卖单出售数量小于,高于卖单价格的所有买单总数量,均应以买单价格成交,买单剩余,核对数据,测试剩余单撤销
# 26 卖单价格低于买单最高价格,且高于买单最低价格,且等于某一中间买单价格,卖单出售数量大于,高于卖单价格的所有买单总数量,均应以买单价格成交,买卖单均剩余,核对数据,测试剩余单撤销

price, volume = get_random_price_and_volume()
test_data24 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, "", "", "eq_buy_price")
test_data25 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, "", "", "eq_buy_price")
test_data26 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, "", "", "eq_buy_price")

# 27 卖单价格低于买单最高价格,且高于买单最低价格,且不等于任何买单价格,卖单出售数量等于,高于卖单价格的所有买单总数量,均应以买单价格成交,买单剩余,核对数据,测试剩余单撤销
# 28 卖单价格低于买单最高价格,且高于买单最低价格,且不等于任何买单价格,卖单出售数量小于,高于卖单价格的所有买单总数量,均应以买单价格成交,买单剩余,核对数据,测试剩余单撤销
# 29 卖单价格低于买单最高价格,且高于买单最低价格,且不等于任何买单价格,卖单出售数量大于,高于卖单价格的所有买单总数量,均应以买单价格成交,买卖单均剩余,核对数据,测试剩余单撤销
test_data27 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, "", "", "")
test_data28 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, "", "", "")
test_data29 = pytest.param(MARKETID, price, EntrustTypeLimit, BUY, volume, "", "", "")

# 先卖 再买
# 30 买单与卖单最高价格一致,买单购买数量与卖单总数量一致,应成交,无沉积单
test_data30 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, "", "", "buy_price_eq_max_sell")
# 31 买单价格低于卖单最低价格,买单购买数量与卖单总数量一致,应不成交,买卖单均剩余,测试剩余单撤销
test_data31 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, "", "", "buy_price_lt_min_sell")

# 32 买单价格高于卖单最低价格,且低于卖单最高价格,且等于某一中间卖单价格,买单购买数量等于,低于买单价格的所有卖单总数量,均应以卖单价格成交,卖单剩余,核对数据,测试剩余单撤销
# 33 买单价格高于卖单最低价格,且低于卖单最高价格,且等于某一中间卖单价格,买单购买数量小于,低于买单价格的卖单总数量,均应以卖单价格成交,卖单剩余,核对数据,测试剩余单撤销
# 34 买单价格高于卖单最低价格,且低于卖单最高价格,且等于某一中间卖单价格,买单购买数量大于,低于买单价格的卖单总数量,均应以卖单价格成交,买卖单均剩余,核对数据,测试剩余单撤销

test_data32 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, "", "", "eq_sell_price")
test_data33 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, "", "", "eq_sell_price")
test_data34 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, "", "", "eq_sell_price")

# 35 买单价格高于卖单最低价格,且低于卖单最高价格,且不等于任何卖单价格,买单购买数量等于,低于买单价格的所有卖单总数量,均应以卖单价格成交,卖单剩余,核对数据,测试剩余单撤销
# 36 买单价格高于卖单最低价格,且低于卖单最高价格,且不等于任何卖单价格,买单购买数量小于,低于买单价格的卖单总数量,均应以卖单价格成交,卖单剩余,核对数据,测试剩余单撤销
# 37 买单价格高于卖单最低价格,且低于卖单最高价格,且不等于任何卖单价格,买单购买数量大于,低于买单价格的卖单总数量,均应以卖单价格成交,买卖单均剩余,核对数据,测试剩余单撤销

test_data35 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, "", "", "")
test_data36 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, "", "", "")
test_data37 = pytest.param(MARKETID, price, EntrustTypeLimit, SELL, volume, "", "", "")

# 市价
#  38 先挂单笔限买单，再挂一笔市价卖，买卖方数量一致，应成交无积单。
test_data38 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "same_price_buy_eq")
#  39 先挂单笔限买单，再挂一笔市价卖， 买方数量多余卖方数量
test_data39 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "same_price_buy_gt")
#  40 先挂单笔限买单，再挂一笔市价卖，卖方数量多于买方数量
test_data40 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "same_price_buy_lt")
#  47 先挂单笔限卖单，再挂一笔市买，买卖方数量一致，应成交无积单。
test_data47 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "same_price_sell_eq")
#  48 先挂单笔限卖单，再挂一笔市买，买方数量多余卖方数量
test_data48 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "same_price_sell_lt")
#  49 先挂单笔限卖单，再挂一笔市买，  卖方数量多于买方数量
test_data49 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "same_price_sell_gt")
market_test_data_set1 = [test_data38,
                         test_data39,
                         test_data40,
                         test_data47,
                         test_data48,
                         test_data49]

# 41 先挂多笔价格相同限价买单，提交一笔市价卖出单，买卖单数量一致
test_data41 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "same_price_buy_eq")
# 42 先挂多笔价格相同限价买单，提交一笔市价卖出单，买方多余卖方
test_data42 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "same_price_buy_gt")
# 43 先挂多笔价格相同限价买单，提交一笔市价卖出单，卖方多余卖方
test_data43 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "same_price_buy_lt")
# 50 先挂多笔价格相同限价卖单，提交一笔市价买单，买卖单数量一致
test_data50 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "same_price_sell_eq")
# 51 先挂多笔价格相同限价卖单，提交一笔市价买单，买方多余卖方
test_data51 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "same_price_sell_lt")
# 52 先挂多笔价格相同限价卖单，提交一笔市价买单，卖方多余卖方
test_data52 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "same_price_sell_gt")
market_test_data_set2 = [test_data41,
                         test_data42,
                         test_data43,
                         test_data50,
                         test_data51,
                         test_data52]

# 44 先挂多笔价格不同限价买单，提交一笔市价卖出单，买卖单数量一致
test_data44 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "different_price_buy_eq")
# 45 先挂多笔价格不同限价买单，提交一笔市价卖出单，买方多余卖方
test_data45 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "different_price_buy_gt")
# 46 先挂多笔价格不同限价买单，提交一笔市价卖出单，卖方多余卖方
test_data46 = pytest.param(MARKETID, "", EntrustTypeLimit, BUY, "", "", "", "different_price_buy_lt")
# 53 先挂多笔价格不同限价卖单，提交一笔市价买单，买卖单数量一致
test_data53 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "different_price_sell_eq")
# 54 先挂多笔价格不同限价卖单，提交一笔市价买单，买方多余卖方
test_data54 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "different_price_sell_lt")
# 55 先挂多笔价格不同限价卖单，提交一笔市价买单，卖方多余卖方
test_data55 = pytest.param(MARKETID, "", EntrustTypeLimit, SELL, "", "", "", "different_price_sell_gt")
market_test_data_set3 = [test_data44,
                         test_data45,
                         test_data46,
                         test_data53,
                         test_data54,
                         test_data55]
