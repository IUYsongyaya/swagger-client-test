import random
import pytest
import string


def get_random_data():
    total_spend_range = (101, 100_00)
    price_range = (1, 50)
    price = round(random.uniform(*price_range), 2)
    volume = round(random.uniform(*total_spend_range) / price, 2)
    return price, volume


def get_random_uppercase(n=4):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def get_random_lowercase(n=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


# transaction
## 购买USDT异常
# 未登录，购买失败，提示登陆后下单
# 未设置实名认证，在购买窗口中点击下单-》 下单失败
# 未绑定手机号，在购买窗口中点击下单-》 下单失败，提示未进行实名认证
# 未设置昵称，在购买窗口中点击下单-》 下单失败，提示未设置昵称
# 未设置资金密码，在购买窗口中点击下单-》 下单失败，提示未设置资金密码
# 企业实名认证通过，其他限制条件已经满足，在购买窗口中点击下单-》下单失败，提示企业认证用户不可用
## 购买USDT
# 1限制条件满足，下单购买-》选择需要购买的广告订单，点击购买 -》 在购买USDT窗口中输入参数，点击下单 -》 商家放行，放行成功
# 2限制条件满足，下单购买-》选择需要购买的广告订单，点击购买 -》 在购买USDT窗口中输入数量超出商家的指定数量，点击下单 -》 下单失败，提示数量超出商家数量
# 3限制条件满足，下单购买-》选择需要购买的广告订单，点击购买 -》 在购买USDT窗口中输入总价超出商家的指定限额，点击下单 -》 下单失败，提示总价超出商家限额
# 4限制条件满足，下单购买-》选择需要购买的广告订单，点击购买 -》 在支付页面取消订单成功-》 在订单管理的取消订单中出现
# 6取消三次，限制条件满足，下单购买-》无法下单
## 出售USDT异常
# 未登录，出售失败，提示登陆后下单
# 未设置实名认证，在出售窗口中点击下单-》 下单失败
# 未绑定手机号，在出售窗口中点击下单-》 下单失败，提示未进行实名认证
# 未设置昵称，在出售窗口中点击下单-》 下单失败，提示未设置昵称
# 未设置资金密码，在出售窗口中点击下单-》 下单失败，提示未设置资金密码
# 未设置收款方式，在出售窗口中点击下单-》 下单失败，提示未设置资金密码
# 企业实名认证通过，其他限制条件已经满足，在出售窗口中点击下单-》下单失败，提示企业认证用户不可用
## 出售USDT
# 7限制条件满足，下单购买-》选择需要购买的广告订单，点击购买 -》 在出售USDT窗口中输入参数，点击下单 -》 用户支付成功，放行成功 -》 资产减少
# 8限制条件满足，下单购买-》选择需要购买的广告订单，点击购买 -》 在出售USDT窗口中输入数量超出商家的指定数量，点击下单 -》 下单失败，提示数量超出商家数量
# 9限制条件满足，下单购买-》选择需要购买的广告订单，点击购买 -》 在出售USDT窗口中输入总价超出商家的指定限额，点击下单 -》 下单失败，提示总价超出商家限额
# 10限制条件满足，下单购买-》选择需要购买的广告订单，点击购买 -》 在支付页面取消订单成功-》 在订单管理的取消订单中出现

CURRENCYID = 6  # 币种
FIELDS = 'direction,status,fail_type'
#  direction(sell or buy), status (success, fail, cancel) , fail_type(amount, price)
# data1 = pytest.param(direction, status, fail_type)
data1 = pytest.param('buy', 'success', '')
data7 = pytest.param('sell', 'success', '')
data2 = pytest.param('buy', 'fail', 'amount')
data8 = pytest.param('sell', 'fail', 'amount')
data4 = pytest.param('buy', 'cancel', '')
data10 = pytest.param('sell', 'cancel', '')

test_transaction_data = [data1, data7, data2, data8, data4, data10]

# order
# direction(sell or buy), status (success, fail, cancel) , fail_type(amount, price)
# 产生一笔出售待支付订单，查看订单信息， 点击订单管理， 进行中的列表信息中需要存在
# 产生一笔购买待放行订单，查看订单信息， 点击订单管理，列表信息中需要存在
# 产生一笔出售申诉中订单， 查看订单信息， 点击订单管理，列表信息中需要存在
data11 = pytest.param('sell', 'in_pay', '')
data12 = pytest.param('buy', 'in_release', '')
data13 = pytest.param('sell', 'in_complain', '')

test_order_processing = [data11, data12, data13]

# 已完成，产生一笔出售成功订单，查看信息，点击订单管理，列表信息存在
# 已完成，产生一笔购买成功订单， 查看信息， 点击订单管理， 列表信息存在
data14 = pytest.param('sell', 'success', '')
data15 = pytest.param('buy', 'success', '')
test_order_done = [data14, data15]


# 已取消，产生一笔出售取消订单，查看信息，点击订单管理，列表信息存在
# 已取消，产生一笔购买取消订单， 查看信息， 点击订单管理， 列表信息存在
data16 = pytest.param('sell', 'cancel', '')
data17 = pytest.param('buy', 'cancel', '')
data16_1 = pytest.param('sell', 'force_cancel', '')
data17_1 = pytest.param('buy', 'force_cancel', '')
test_order_cancel = [data16, data17, data16_1, data17_1]

data17_2 = pytest.param('buy', 'fail', 'lt')
data17_3 = pytest.param('buy', 'fail', 'gt')
data17_4 = pytest.param('sell', 'fail', 'lt')
data17_5 = pytest.param('sell', 'fail', 'gt')
test_limit_order = [data17_2, data17_3, data17_4, data17_5]
test_limit_ad = [data17_2, data17_3, data17_4, data17_5]

# ad
# 条件满足》在发布广告页面，选择广告类型为：购买、交易币种为：USDT、收款方式，输入价格、交易设置、资金密码，点击提交 -》 广告发布成功，在交易大厅的出售USDT列表中显示发布的广告信息
data18 = pytest.param('buy', 'success')
# 条件满足-》在发布广告页面，选择广告类型为：出售、交易币种为：USDT、收款方式，输入价格、交易设置、资金密码，点击提交 -》 广告发布成功，在交易大厅的购买USDT列表中显示发布的广告信息，法币余额冻结的数量与发布的数量一致
data19 = pytest.param('sell', 'success')
test_create_ad_data = [data18, data19]

# 编辑已上架且有成交订单的广告，点击编辑按钮-》编辑失败，提示该广告无法进行编辑
# status, action, type
# has_transaction, up, fail
data21 = pytest.param('up_has_transaction', 'edit', 'fail')
data22 = pytest.param('up_has_transaction', 'edit', 'success')
test_edit_ad_data = [data21, data22]

# 手动下架 -》 广告发布成功，且没有订单在进行中时，点击广告下架 -》广告下架成功，在交易大厅中不会显示该比广告，在广告管理中显示该比广告信息
data23 = pytest.param('up_no_transaction', 'down', 'success')
# 自动下架 -》 广告发布成功，且最后一笔订单完成后交易单间*数量<最小交易限额则广告自动下架 -》广告下架成功，在交易大厅中不会显示该笔广告信息，在广告管理中显示该笔广告信息
data24 = pytest.param('up_has_transaction', 'auto_down', 'success')
test_down_ad_data = [data23, data24]

# 删除上架广告 -》 广告发布成功，在广告管理页面中，选择需要删除的广告，点击删除按钮 -》删除失败，提示该广告已上架
data25 = pytest.param('up_ad', 'delete', 'fail')
# 删除下架广告 -》 广告发布成功，在广告管理页面中，选择需要删除的广告，点击删除按钮 -》 删除成功，在交易大厅中不会显示该笔广告，广告管理中也不会显示该笔广告
data26 = pytest.param('down_ad', 'delete', 'success')
test_delete_ad_data = [data25, data26]

# 广告发布成功且已下架-》 选择需要上架的广告，点击上架按钮 -》 输入上架数量，数量范围：100/价格<数量<1000000/价格，点击确定 -》上架广告成功，在交易大厅中显示该笔广告，广告管理中的这笔广告操作显示上架按钮变成下架
data27 = pytest.param('up_ad', 'up_normal', 'success')
# 广告发布成功且已下架-》 选择需要上架的广告，点击上架按钮 -》输入比最小值还小的上架数量，点击确定 -》上架广告失败，提示上架数量值低于最小值
data28 = pytest.param('up_ad', 'up_mini', 'fail')
# 广告发布成功且已下架-》 选择需要上架的广告，点击上架按钮 -》输入比最大值还大的上架数量，点击确定 -》上架广告失败，提示上架数量值大于最大值
data29 = pytest.param('up_ad', 'up_large', 'fail')
test_up_ad_data = [data27, data28, data29]
