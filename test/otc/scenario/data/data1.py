# -*- coding: utf-8 -*-
# @File :  data1.py
# @Author : lh
import random
import pytest


def get_random_data():
    total_spend_range = (101, 100_00)
    price_range = (1, 50)
    price = round(random.uniform(*price_range), 2)
    volume = round(random.uniform(*total_spend_range) / price, 2)
    return price, volume


def get_random_min_amount():
    amount_range = (0.0001, 0.99999999)
    amount = round(random.uniform(*amount_range), 8)
    return amount


def get_random_max_amount():
    amount_range = (100000, 9999999)
    amount = random.randint(*amount_range)
    return amount


FIELDS = 'amount, coin_name'
# 获取资产信息，资产信息显示正确，币币余额与主平台用户资产数据一致
amount = get_random_min_amount()
test_data1 = pytest.param(amount, 'USDT')  # TODO
# test_data2 = pytest.param(3, 'COIN2S')
# test_data3 = pytest.param('COIN00', 5)
# test_data4 = pytest.param('USDT', 1)
# test_data5 = pytest.param('COIN2T', 7)
# test_data6 = pytest.param('COIN2U', 8)
# test_data7 = pytest.param('COIN2V', 9)
# test_data8 = pytest.param('COIN2W', 10)
# test_data9 = pytest.param('COIN2X', 11)
# test_data10 = pytest.param('COIN2Y', 12)
# test_data11 = pytest.param('COIN2Z', 13)
# test_data12 = pytest.param('COIN30', 14)
# test_data13 = pytest.param('COIN31', 15)
# test_data15 = pytest.param('COIN32', 17)
# test_data16 = pytest.param('COIN33', 18)
# test_data17 = pytest.param('COIN34', 19)
# test_data18 = pytest.param('COIN35', 20)
# test_data19 = pytest.param('COIN36', 21)
# test_data20 = pytest.param('COIN37', 22)

# 币币划转到法币-》 选择某一币种，点击立即划转-》在资金划转页面中，选择需要划转的币种与数量、划转平台为币币，点击确定 -》 资产划转陈工，币币余额减少，法币余额增加，主平台资产余额余币币余额资产数量一致
amount = get_random_min_amount()
test_data21 = pytest.param(amount, 'USDT')  #
# 法币到币币 -》选择某一币种，点击立即划转-》 在资金划转页面中，选择需要划转的币种与数量、划转平台为法币，点击确定 -》 资产划转成功，法币余额减少，币币余额增加，主平台资产余额余币币余额资产数量一致
amount = get_random_min_amount()
test_data22 = pytest.param(amount, 'USDT')
# 法币到币币 -》选择某一币种，划转数量超出币币余额点击立即划转-》失败，提示余额不足
amount = 1000000000000
test_data23 = pytest.param(amount, 'USDT')
# 币币划转到法币-》 选择某一币种，划转数量超出币币余额点击立即划转-》失败，提示余额不足
amount = 1000000000000
test_data24 = pytest.param(amount, 'USDT')
# 进行一笔币币划转到法币平台，划转成功，在资产明细列表中显示一笔类型为转入的记录，记录信息显示正确
# 进行一笔法币划转到币币平台，划转成功，在资产明细列表中显示一笔类型为转出的记录，记录信息显示正确
# 完成一笔买入订单，在资产明细列表中显示一笔类型为买入的记录，记录信息显示正确
# 完成一笔卖出订单，在资产明细列表中显示一笔类型为卖出的记录，记录信息显示正确

test_asset_Data = [
    test_data1
]

# test_asset_Data = [
#     test_data1, test_data2, test_data3, test_data5, test_data6, test_data7, test_data8, test_data9, test_data10,
#     test_data11, test_data12, test_data13, test_data15, test_data16, test_data17, test_data18, test_data19,
#     test_data20
# ]

test_trans_coin_legals = [
    test_data21
]

test_trans_legals_coin = [
    test_data22
]

test_trans_coin_legals_fail = [
    test_data23
]

test_trans_legals_coin_fail = [
    test_data24
]
