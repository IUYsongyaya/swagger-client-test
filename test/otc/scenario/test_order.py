# @author: lj
import time
import pytest

from swagger_client.otc.api import OrderApi, AdvertisementApi, BalanceApi, PaymodeApi
from swagger_client.otc.models import CreateOrderRequest, OrderComplainRequest
from swagger_client.staff.api import OrderApi as StaffOrderApi
from swagger_client.otc.rest import ApiException
from test.otc.scenario.data.data import FIELDS, test_order_processing, test_order_done, test_order_cancel, test_limit_order
from .util import create_ad, get_random_data, create_paymode

from common.account_sign import set_login_status

order_api = OrderApi()
ad_api = AdvertisementApi()
balance_api = BalanceApi()
pay_mode_api = PaymodeApi()
staff_order_api = StaffOrderApi()


class TestTransaction:
    # 产生一笔出售待支付订单，查看订单信息， 点击订单管理， 进行中的列表信息中需要存在
    # 产生一笔购买待放行订单，查看订单信息， 点击订单管理，列表信息中需要存在
    # 产生一笔出售申诉中订单， 查看订单信息， 点击订单管理，列表信息中需要存在
    @pytest.mark.parametrize(FIELDS, test_order_processing)
    def test_processing(self, direction, status, fail_type, otc_user):
        ad_creator = otc_user([ad_api, pay_mode_api])
        pay_way_id = create_paymode(pay_mode_api,
                                    ad_creator['asset_password'])
        price, amount = get_random_data()
        if direction == 'sell':
            # 获取买币广告
            response = create_ad(
                ad_api, (price, amount),
                ad_creator['buyer_coin_id'],
                ad_creator['asset_password'],
                direction=1)
        else:
            # 获取卖币广告
            response = create_ad(ad_api, (price, amount),
                                 ad_creator['buyer_coin_id'],
                                 ad_creator['asset_password'])
        ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        print(f"ad_info: {ad_info}")


        ad = ad_info.to_dict()
        amount = float(
            ad['amount']) - round(100 / int(float(ad['price'])),
                                  2)  # 这里为了省事直接把广告的总数买完，由于是场外不需要考虑买方资产问题

        order_creator = otc_user([order_api, pay_mode_api, balance_api])
        sec_pay_way_id = create_paymode(pay_mode_api,
                                        order_creator['asset_password'])

        coin_info = balance_api.balance_info_currency_id_get(currency_id=order_creator['buyer_coin_id'])
        print(f"coin_info{coin_info}")

        print(order_creator)
        # import pdb;
        # pdb.set_trace()
        if status == 'in_pay':
            payload = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
            res = order_api.order_create_post(payload)
            order_info = order_api.order_info_order_id_get(
                order_id=res.order_id)
            assert int(order_info.status) == 10

            set_login_status(staff_order_api, order_creator['admin_token'])
            check_info = staff_order_api.admin_order_find_page_get(
                ad_id=ad['ad_id'], order_id=res.order_id)
            assert int(check_info.items[0].status) == 10

        if status == 'in_release':
            payload = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
            res = order_api.order_create_post(payload)
            # 确认付款
            order_api.order_buyer_paid_order_id_paymode_id_post(
                order_id=res.order_id, paymode_id=pay_way_id)
            order_info = order_api.order_info_order_id_get(
                order_id=res.order_id)
            assert int(order_info.status) == 20

            set_login_status(staff_order_api, order_creator['admin_token'])
            check_info = staff_order_api.admin_order_find_page_get(
                ad_id=ad['ad_id'], order_id=res.order_id)
            assert int(check_info.items[0].status) == 20

            # 强制放行
            staff_order_api.admin_order_force_confirm_order_id_post(
                order_id=res.order_id)
            check_info = staff_order_api.admin_order_find_page_get(
                ad_id=ad['ad_id'], order_id=res.order_id)
            assert int(check_info.items[0].status) == 35  # 强制放行

        if status == 'in_complain':
            payload = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
            res = order_api.order_create_post(payload)

            # 广告方确认付款
            set_login_status(order_api, ad_creator['user_token'])
            order_api.order_buyer_paid_order_id_paymode_id_post(
                order_id=res.order_id, paymode_id=sec_pay_way_id)
            order_info = order_api.order_info_order_id_get(
                order_id=res.order_id)
            assert int(order_info.status) == 20
            # 申诉
            set_login_status(order_api, order_creator['user_token'])
            complain_load = OrderComplainRequest(
                order_id=res.order_id, complain='test')
            order_api.order_complain_post(complain_load)

            order_info = order_api.order_info_order_id_get(
                order_id=res.order_id)
            assert int(order_info.status) == 25

            set_login_status(staff_order_api, order_creator['admin_token'])
            check_info = staff_order_api.admin_order_find_page_get(
                ad_id=ad['ad_id'], order_id=res.order_id)
            assert int(check_info.items[0].status) == 25

    @pytest.mark.parametrize(FIELDS, test_limit_order)
    def test_limit_order(self, direction, status, fail_type, otc_user):
        ad_creator = otc_user([ad_api, order_api, pay_mode_api])
        create_paymode(pay_mode_api, ad_creator['asset_password'])
        price, amount = get_random_data()
        if direction == 'sell':
            # 获取买币广告
            response = create_ad(
                ad_api, (price, amount),
                ad_creator['buyer_coin_id'],
                ad_creator['asset_password'],
                direction=1)
        else:
            # 获取卖币广告
            response = create_ad(ad_api, (price, amount),
                                 ad_creator['buyer_coin_id'],
                                 ad_creator['asset_password'])
        ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        ad = ad_info.to_dict()
        amount = float(
            ad['amount']) - round(float(ad['min_limit']) / int(float(ad['price'])),
                                  2)  # 这里为了省事直接把广告的总数买完，由于是场外不需要考虑买方资产问题

        order_creator = otc_user([pay_mode_api, order_api])
        create_paymode(pay_mode_api, order_creator['asset_password'])

        if fail_type == 'lt':
            amount = round(float(ad['min_limit']) / float(ad['price']), 2) - 1

        if fail_type == 'gt':
            amount = round(float(ad['max_limit']) / float(ad['price']), 2) + 100

        try:
            create_order = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
            order_api.order_create_post(create_order)
        except ApiException as e:
            assert 400 <= e.status < 500
            print(e.status)
        else:
            raise ApiException

    # 已完成，产生一笔出售成功订单，查看信息，点击订单管理，列表信息存在
    # 已完成，产生一笔购买成功订单， 查看信息， 点击订单管理， 列表信息存在
    @pytest.mark.parametrize(FIELDS, test_order_done)
    def test_done(self, direction, status, fail_type, otc_user):
        ad_creator = otc_user([ad_api, order_api, pay_mode_api])
        pay_way_id = create_paymode(pay_mode_api,
                                    ad_creator['asset_password'])
        price, amount = get_random_data()
        if direction == 'sell':
            # 获取买币广告
            response = create_ad(
                ad_api, (price, amount),
                ad_creator['buyer_coin_id'],
                ad_creator['asset_password'],
                direction=1)
        else:
            # 获取卖币广告
            response = create_ad(ad_api, (price, amount),
                                 ad_creator['buyer_coin_id'],
                                 ad_creator['asset_password'])
        ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        ad = ad_info.to_dict()
        print(ad_info)
        amount = float(
            ad['amount']) - round(100 / int(float(ad['price'])),
                                  2)  # 这里为了省事直接把广告的总数买完，由于是场外不需要考虑买方资产问题

        order_creator = otc_user([pay_mode_api, order_api])
        sec_pay_way_id = create_paymode(pay_mode_api,
                                        order_creator['asset_password'])
        create_order = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
        res = order_api.order_create_post(create_order)

        if direction == 'sell':
            # 买币广告
            # 卖币订单
            set_login_status(order_api, ad_creator['user_token'])
            order_api.order_buyer_paid_order_id_paymode_id_post(
                order_id=res.order_id, paymode_id=sec_pay_way_id)
            # 卖家确认放行
            set_login_status(order_api, order_creator['user_token'])
            order_api.order_seller_confirm_order_id_post(order_id=res.order_id)
            set_login_status(order_api, ad_creator['user_token'])
            order_count = order_api.order_complete_order_count_get()
            assert order_count.count == 1
        else:
            # 卖币广告
            # 买币订单
            order_api.order_buyer_paid_order_id_paymode_id_post(
                order_id=res.order_id, paymode_id=pay_way_id)
            # 卖家确认放行
            set_login_status(order_api, ad_creator['user_token'])
            order_api.order_seller_confirm_order_id_post(order_id=res.order_id)

            set_login_status(order_api, order_creator['user_token'])
            order_count = order_api.order_complete_order_count_get()
            assert order_count.count == 1

            paymode_list = order_api.order_paymode_list_order_id_get(
                order_id=res.order_id)
            assert pay_way_id in [i.id for i in paymode_list.items]

        order_list = order_api.order_list_get()
        assert len(order_list.items) == 1
        order_info = order_api.order_info_order_id_get(order_id=res.order_id)
        assert int(order_info.status) == 30

        set_login_status(staff_order_api, order_creator['admin_token'])
        check_canel_info = staff_order_api.admin_order_complete_order_count_get(order_creator['account_id'])
        assert check_canel_info.count == 1

        check_info = staff_order_api.admin_order_find_page_get(
            ad_id=ad['ad_id'], order_id=res.order_id)
        assert int(check_info.items[0].status) == 30


    # 已取消，产生一笔出售取消订单，查看信息，点击订单管理，列表信息存在
    # 已取消，产生一笔购买取消订单， 查看信息， 点击订单管理， 列表信息存在
    # 后台强制取消，产生一笔出售取消订单， 查看信息， 点击订单管理， 列表信息存在
    # 后台强制取消，产生一笔购买取消订单， 查看信息， 点击订单管理， 列表信息存在
    @pytest.mark.parametrize(FIELDS, test_order_cancel)
    def test_cancel(self, direction, status, fail_type, otc_user):
        ad_creator = otc_user([ad_api, order_api, pay_mode_api])
        create_paymode(pay_mode_api, ad_creator['asset_password'])
        price, amount = get_random_data()
        if direction == 'sell':
            # 获取买币广告
            response = create_ad(
                ad_api, (price, amount),
                ad_creator['buyer_coin_id'],
                ad_creator['asset_password'],
                direction=1)
        else:
            # 获取卖币广告
            response = create_ad(ad_api, (price, amount),
                                 ad_creator['buyer_coin_id'],
                                 ad_creator['asset_password'])
        ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        ad = ad_info.to_dict()
        amount = float(
            ad['amount']) - round(100 / int(float(ad['price'])),
                                  2)  # 这里为了省事直接把广告的总数买完，由于是场外不需要考虑买方资产问题
        order_creator = otc_user([order_api, pay_mode_api])
        create_paymode(pay_mode_api, order_creator['asset_password'])
        create_order = CreateOrderRequest(ad_id=ad['ad_id'], amount=amount)
        res = order_api.order_create_post(create_order)
        if 'force' not in status:
            # 只有买家可以取消订单
            if direction == 'sell':
                set_login_status(order_api, ad_creator['user_token'])
            order_api.order_cancel_order_id_post(order_id=res.order_id)
            cancel_times = order_api.order_cancel_times_get()
            assert cancel_times.times == 1
        else:
            # 后台强制取消
            set_login_status(staff_order_api, order_creator['admin_token'])
            staff_order_api.admin_order_force_cancel_order_id_post(
                order_id=res.order_id)

        order_info = order_api.order_info_order_id_get(order_id=res.order_id)

        if 'force' not in status:
            assert int(order_info.status) == -2
        else:
            assert int(order_info.status) == -3

        # 后台查看
        set_login_status(staff_order_api, order_creator['admin_token'])
        check_info = staff_order_api.admin_order_find_page_get(
            ad_id=ad['ad_id'], order_id=res.order_id)

        if 'force' not in status:
            assert int(check_info.items[0].status) == -2
            # 后台查看
            if direction == 'sell':
                account_id = ad_creator['account_id']
            else:
                account_id = order_creator['account_id']
            check_canel_info = staff_order_api.admin_order_cancel_times_get(account_id)
            assert check_canel_info.times == 1
        else:
            assert int(check_info.items[0].status) == -3

        if direction == 'sell':
            # 后台重置取消次数
            account_id = ad_creator['account_id']
        else:
            account_id = order_creator['account_id']
        staff_order_api.admin_order_reset_cancel_times_user_id_post(account_id)
        cancel_times = order_api.order_cancel_times_get()
        assert cancel_times.times == 0

