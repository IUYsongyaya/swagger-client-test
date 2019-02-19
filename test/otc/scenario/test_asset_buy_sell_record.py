# -*- coding: utf-8 -*-
# @File :  test_asset_buy_sell_record.py
# @Author : lh
import random
import time
import logging
import pytest
from common.account_sign import set_login_status, get_admin_token
from swagger_client.otc import PostPaymodeRequest, CreateOrderRequest
from swagger_client.otc.api import AssetManagementApi as Otcasset, BalanceApi
from swagger_client.otc.api import AccountApi, AdvertisementApi, OrderApi, PaymodeApi
from swagger_client.main.api import AssetManagementApi
from swagger_client.staff.api import BalanceApi as StaffBal
from swagger_client.staff.api import OrderApi as StaffOrder
from test.otc.scenario.data.data import get_random_data
from test.otc.scenario.util import create_ad, create_paymode
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler)

otc_bal_api = BalanceApi()
otc_ac_api = AccountApi()
otc_ad_api = AdvertisementApi()
otc_order_api = OrderApi()
otc_asset_api = Otcasset()
otc_pay_mode_api = PaymodeApi()
staff_bal_api = StaffBal()
staff_order_api = StaffOrder()


class TestAssetOrder:
    # 下一笔订单,冻结资产
    # 完成一笔买入订单，在资产明细列表中显示一笔类型为买入的记录，记录信息显示正确
    @pytest.mark.parametrize('order_direction', ['sell'])
    def testassetsell(self, order_direction, otc_user):
        """
        在资产明细列表中显示一笔类型为买入的记录
        """

        staff_token = get_admin_token()
        set_login_status(staff_bal_api, staff_token)
        one_user_info = otc_user([otc_ad_api, otc_order_api, otc_pay_mode_api, otc_bal_api, otc_asset_api])
        pay_way_id = create_paymode(otc_pay_mode_api, one_user_info['asset_password'])
        time.sleep(3)
        price, amount = get_random_data()
        if amount < 100:
            amount += 100
        # derection:订单类型 1:buy
        if order_direction == 'sell':
            # 获取买币广告
            response = create_ad(otc_ad_api, (price, amount), one_user_info['buyer_coin_id'],
                                 one_user_info['asset_password'], direction=1)
            coin_id = one_user_info['seller_coin_id']
        else:
            # 获取卖币广告
            response = create_ad(otc_ad_api, (price, amount), one_user_info['buyer_coin_id'],
                                 one_user_info['asset_password'])
            coin_id = one_user_info['seller_coin_id']
        ad_info = otc_ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        ad = ad_info.to_dict()
        # 这里为了省事直接把广告的总数买完，由于是场外不需要考虑买方资产问题
        amount = round(float(ad['amount']) - round((100 / int(float(ad['price']))), 2), 8)

        sec_user_info = otc_user([otc_pay_mode_api, otc_order_api, otc_bal_api, otc_ac_api, otc_asset_api])
        sec_pay_way_id = create_paymode(otc_pay_mode_api, sec_user_info['asset_password'])
        create_order = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
        # 创建订单
        res = otc_order_api.order_create_post(create_order)
        # 获取用户id
        user_info = otc_ac_api.accounts_account_info_get()
        ac_id = user_info.account_info.account_id

        if order_direction == 'sell':
            # 买币广告
            # 卖币订单
            set_login_status(otc_order_api, one_user_info['user_token'])
            otc_order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=sec_pay_way_id)
            # 卖家确认放行
            set_login_status(otc_order_api, sec_user_info['user_token'])
            otc_order_api.order_seller_confirm_order_id_post(order_id=res.order_id)
            # otc查看资金余额
            after_otc_asset = otc_bal_api.balance_info_currency_id_get(currency_id=coin_id)
            logger.info(f'下完单之后的资产1:{after_otc_asset}')
        else:
            # 卖币广告
            # 买币订单
            otc_order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=pay_way_id)
            # 卖家确认放行
            set_login_status(otc_order_api, one_user_info['user_token'])
            otc_order_api.order_seller_confirm_order_id_post(order_id=res.order_id)
            # otc查看资金余额
            after_otc_asset = otc_bal_api.balance_info_currency_id_get(currency_id=coin_id)
            logger.info(f'下完单之后的资产2:{after_otc_asset}')

        order_info = otc_order_api.order_info_order_id_get(order_id=res.order_id)
        # 卖出订单id
        sell_oder_id = order_info.order_id
        assert int(order_info.status) == 30

        set_login_status(staff_order_api, sec_user_info['admin_token'])
        check_info = staff_order_api.admin_order_find_page_get(ad_id=ad['ad_id'], order_id=res.order_id)
        assert int(check_info.items[0].status) == 30
        # otc查询流水转出的记录
        otc_transto_list = otc_bal_api.balance_get_flow_get()
        logger.info(f'流水记录:{otc_transto_list}')
        otc_transto_info = [float(i.amount) for i in otc_transto_list.items]
        logger.info(f'流水列表:{otc_transto_info}')
        assert float(amount) in otc_transto_info
        # 后台查询流水转出记录
        staff_transto_list = staff_bal_api.admin_balance_user_balance_flow_get(user_id=ac_id)
        staff_transto_info = [float(i.amount) for i in staff_transto_list.items]
        assert float(amount) in staff_transto_info
        staff_trace_res = [i.trace_id for i in staff_transto_list.items]
        assert sell_oder_id in staff_trace_res

    @pytest.mark.parametrize('order_direction', ['buy'])
    def testassetbuy(self, otc_user, order_direction):
        """
        在资产明细列表中显示一笔类型为卖出的记录
        """
        staff_token = get_admin_token()
        set_login_status(staff_bal_api, staff_token)
        one_user_info = otc_user([otc_ad_api, otc_order_api, otc_pay_mode_api, otc_bal_api])
        pay_way_id = create_paymode(otc_pay_mode_api, one_user_info['asset_password'])
        time.sleep(3)
        price, amount = get_random_data()
        if amount < 100:
            amount += 100
        # derection=1 : buy
        if order_direction == 'sell':
            # 获取买币广告
            response = create_ad(otc_ad_api, (price, amount), one_user_info['buyer_coin_id'],
                                 one_user_info['asset_password'], direction=1)
        else:
            # 获取卖币广告
            response = create_ad(otc_ad_api, (price, amount), one_user_info['buyer_coin_id'],
                                 one_user_info['asset_password'])
            # 获取创建卖币广告以后的资产
            coin_id = one_user_info['buyer_coin_id']
            crate_ad_asset = otc_bal_api.balance_info_currency_id_get(currency_id=coin_id)
            logger.info(f'获取创建卖币广告以后的资产:{crate_ad_asset}')
        ad_info = otc_ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        ad = ad_info.to_dict()
        # 这里为了省事直接把广告的总数买完，由于是场外不需要考虑买方资产问题
        amount = round(float(ad['amount']) - round((100 / int(float(ad['price']))), 2), 8)
        sec_user_info = otc_user([otc_pay_mode_api, otc_order_api, otc_bal_api, otc_ac_api])
        sec_pay_way_id = create_paymode(otc_pay_mode_api, sec_user_info['asset_password'])
        create_order = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
        res = otc_order_api.order_create_post(create_order)
        # 获取用户id
        user_info = otc_ac_api.accounts_account_info_get()
        ac_id = user_info.account_info.account_id
        if order_direction == 'sell':
            # 买币广告
            # 卖币订单
            set_login_status(otc_order_api, one_user_info['user_token'])
            otc_order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=sec_pay_way_id)
            # 卖家确认放行
            set_login_status(otc_order_api, sec_user_info['user_token'])
            otc_order_api.order_seller_confirm_order_id_post(order_id=res.order_id)
        else:
            # 卖币广告
            # 买币订单
            otc_order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=pay_way_id)
            # 卖家确认放行
            set_login_status(otc_order_api, one_user_info['user_token'])
            otc_order_api.order_seller_confirm_order_id_post(order_id=res.order_id)
        # 买入订单id
        order_info = otc_order_api.order_info_order_id_get(order_id=res.order_id)
        buy_oder_id = order_info.order_id
        assert int(order_info.status) == 30

        set_login_status(staff_order_api, sec_user_info['admin_token'])
        check_info = staff_order_api.admin_order_find_page_get(ad_id=ad['ad_id'], order_id=res.order_id)
        assert int(check_info.items[0].status) == 30
        # otc查询流水转出的记录
        otc_transto_list = otc_bal_api.balance_get_flow_get()
        logger.info(f'流水记录:{otc_transto_list}')
        otc_transto_info = [float(i.amount) for i in otc_transto_list.items]
        logger.info(f'流水列表:{otc_transto_info}')
        assert float(amount) in otc_transto_info
        # 后台查询流水转出记录
        staff_transto_list = staff_bal_api.admin_balance_user_balance_flow_get(user_id=ac_id)
        logger.info(f'后台流水列表:{staff_transto_list}')
        staff_transto_info = [float(i.amount) for i in staff_transto_list.items]
        assert float(amount) in staff_transto_info
        staff_trace_res = [i.trace_id for i in staff_transto_list.items]
        assert buy_oder_id in staff_trace_res

    @pytest.mark.parametrize('order_direction', ['buy'])
    def testorderforcerelease(self, otc_user, order_direction):
        """
        卖家收到钱不放行,后台强制放行,查看用户资产
        """
        staff_token = get_admin_token()
        set_login_status(staff_bal_api, staff_token)
        one_user_info = otc_user([otc_ad_api, otc_order_api, otc_pay_mode_api, otc_bal_api])
        pay_way_id = create_paymode(otc_pay_mode_api, one_user_info['asset_password'])
        time.sleep(3)
        price, amount = get_random_data()

        # direction=1 : buy
        if order_direction == 'sell':
            # 获取买币广告
            response = create_ad(otc_ad_api, (price, amount), one_user_info['buyer_coin_id'],
                                 one_user_info['asset_password'], direction=1)
        else:
            # 获取卖币广告
            response = create_ad(otc_ad_api, (price, amount), one_user_info['buyer_coin_id'],
                                 one_user_info['asset_password'])
            # 获取创建卖币广告以后的资产
            coin_id = one_user_info['buyer_coin_id']
            create_ad_asset = otc_bal_api.balance_info_currency_id_get(currency_id=coin_id)
            logger.info(f'获取创建卖币广告以后的资产:{create_ad_asset}')
        ad_info = otc_ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        ad = ad_info.to_dict()
        # 这里为了省事直接把广告的总数买完，由于是场外不需要考虑买方资产问题
        amount = round(float(ad['amount']) - round((100 / int(float(ad['price']))), 2), 8)
        logger.info(f'amount的值:{amount}')
        if amount < 100:
            amount += 100
        sec_user_info = otc_user([otc_pay_mode_api, otc_order_api, otc_bal_api, otc_ac_api])
        sec_pay_way_id = create_paymode(otc_pay_mode_api, sec_user_info['asset_password'])
        create_order = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
        res = otc_order_api.order_create_post(create_order)
        # 获取用户id
        user_info = otc_ac_api.accounts_account_info_get()
        ac_id = user_info.account_info.account_id
        if order_direction == 'sell':
            # 买币广告
            # 卖币订单
            set_login_status(otc_order_api, one_user_info['user_token'])
            otc_order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=sec_pay_way_id)
            # 后台强制确认放行
            staff_token = get_admin_token()
            set_login_status(staff_order_api, staff_token)
            staff_order_api.admin_order_force_confirm_order_id_post(order_id=res.order_id)
        else:
            # 卖币广告
            # 买币订单
            otc_order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=pay_way_id)
            # 后台强制确认放行
            staff_token = get_admin_token()
            set_login_status(staff_order_api, staff_token)
            staff_order_api.admin_order_force_confirm_order_id_post(order_id=res.order_id)
        # 买入订单id
        order_info = otc_order_api.order_info_order_id_get(order_id=res.order_id)
        buy_oder_id = order_info.order_id
        assert int(order_info.status) == 35
        set_login_status(staff_order_api, sec_user_info['admin_token'])
        check_info = staff_order_api.admin_order_find_page_get(ad_id=ad['ad_id'], order_id=res.order_id)
        assert int(check_info.items[0].status) == 35
        # otc查询流水转出的记录
        otc_transto_list = otc_bal_api.balance_get_flow_get()
        logger.info(f'流水记录:{otc_transto_list}')
        otc_transto_info = [float(i.amount) for i in otc_transto_list.items]
        logger.info(f'流水列表:{otc_transto_info}')
        assert float(amount) in otc_transto_info
        # 后台查询流水转出记录
        staff_transto_list = staff_bal_api.admin_balance_user_balance_flow_get(user_id=ac_id)
        logger.info(f'后台流水列表:{staff_transto_list}')
        staff_transto_info = [float(i.amount) for i in staff_transto_list.items]
        assert float(amount) in staff_transto_info
        staff_trace_res = [i.trace_id for i in staff_transto_list.items]
        assert buy_oder_id in staff_trace_res

    @pytest.mark.parametrize('order_direction', ['sell'])
    def testcancelorderasset(self, order_direction, otc_user):
        """
        买家下单后取消订单,资产增加
        """
        staff_token = get_admin_token()
        set_login_status(staff_bal_api, staff_token)
        one_user_info = otc_user([otc_ad_api, otc_order_api, otc_pay_mode_api, otc_bal_api, otc_asset_api])
        pay_way_id = create_paymode(otc_pay_mode_api, one_user_info['asset_password'])
        time.sleep(3)
        price, amount = get_random_data()
        # order_direction=1 : buy
        if order_direction == 'sell':
            # 获取买币广告
            response = create_ad(otc_ad_api, (price, amount), one_user_info['buyer_coin_id'],
                                 one_user_info['asset_password'], direction=1)
        else:
            # 获取卖币广告
            response = create_ad(otc_ad_api, (price, amount), one_user_info['buyer_coin_id'],
                                 one_user_info['asset_password'])
            # 获取创建卖币广告以后的资产
            coin_id = one_user_info['buyer_coin_id']
            create_ad_asset = otc_bal_api.balance_info_currency_id_get(currency_id=coin_id)
            logger.info(f'获取创建卖币广告以后的资产:{create_ad_asset}')
        ad_info = otc_ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        ad = ad_info.to_dict()
        # 这里为了省事直接把广告的总数买完, 由于是场外不需要考虑买房资产问题
        amount = round(float(ad['amount']) - round((100 / int(float(ad['price']))), 2), 8)
        logger.info(f'amount的值:{amount}')
        if amount < 100:
            amount += 100
        sec_user_info = otc_user([otc_pay_mode_api, otc_order_api, otc_bal_api, otc_ac_api, otc_asset_api])
        sec_pay_way_id = create_paymode(otc_pay_mode_api, sec_user_info['asset_password'])
        # 获取sec_user下单前的资产信息
        before_otc_bbye = otc_asset_api.asset_mgmt_assets_get()
        logger.info(f'sec_user下完卖币订单之前的bb余额:{before_otc_bbye}')
        create_order = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
        res = otc_order_api.order_create_post(create_order)
        # 获取sec_user下单后的资产信息
        before_otc_bbye = otc_asset_api.asset_mgmt_assets_get()
        logger.info(f'sec_user下完卖币订单以后的bb余额:{before_otc_bbye}')
        # 获取用户id
        user_info = otc_ac_api.accounts_account_info_get()
        ac_id = user_info.account_info.account_id
        if order_direction == 'sell':
            # 买币广告
            # 卖币订单
            set_login_status(otc_order_api, one_user_info['user_token'])
            otc_order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=sec_pay_way_id)
            # 买家取消订单
            otc_order_api.order_cancel_order_id_post(order_id=res.order_id)
            # 获取sec_user取消订单以后的资产信息
            after_otc_bbye = otc_asset_api.asset_mgmt_assets_get()
            logger.info(f'sec_user取消订单以后的资产信息:{after_otc_bbye}')
        else:
            # 卖币广告
            # 买币订单
            otc_order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=pay_way_id)
            # 卖家取消订单
            otc_order_api.order_cancel_order_id_post(order_id=res.order_id)




