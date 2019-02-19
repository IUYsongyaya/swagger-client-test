# @author: lj
import pytest
import time

from swagger_client.otc import CreateOrderRequest
from swagger_client.otc.api import AdvertisementApi, OrderApi, PaymodeApi
from swagger_client.otc.api import BalanceApi, AssetManagementApi
from swagger_client.staff.api import AdvertisementApi as StaffAdApi
from swagger_client.otc.models import UpdateAdvertisementRequest
from swagger_client.otc.rest import ApiException
from test.otc.scenario.data.data import (
    get_random_data, test_up_ad_data, test_edit_ad_data, test_limit_ad,
    test_down_ad_data, test_delete_ad_data)
from common.account_sign import set_login_status
from .util import create_ad, create_paymode

otc_bal_api = BalanceApi()
otc_asset_api = AssetManagementApi()
ad_api = AdvertisementApi()
order_api = OrderApi()
pay_mode_api = PaymodeApi()
staff_ad_api = StaffAdApi()


class TestAdvert:
    # 未设置实名认证，点击发布广告-》发布广告失败，提示未进行实名认证
    # 未绑定手机号，点击发布广告-〉发布广告失败，提示未绑定手机号
    #
    # 未设置昵称，点击发布广告-》发布广告失败，提示未设置昵称
    # 未设置资金密码，点击发布广告-》发布广告失败，提示未设置资金密码
    # 未设置收款方式，点击发布广告-》发布广告失败，提示未设置收款方式
    # 未申请为商家，点击发布广告-》发布广告失败，跳转到申请商家页面
    # 企业实名认证通过，其它限制条件已满足，点击发布广告 -》 发布广告失败，提示企业用户无法发布
    @pytest.mark.parametrize('fail_type,code', [pytest.param("not_individual", 1),
                                                # ("is_company", 2),
                                                # ("not_bind_phone", 3),
                                                # ("not_nick_name", 4),
                                                # ("not_assert_pwd", 5),
                                                pytest.param("not_biz", 6)])
    def test_auth(self, fail_type, code, limit_user):
        price, amount = get_random_data()
        ad_creator = limit_user([ad_api], fail_type)
        try:
            res = create_ad(
                ad_api, (price, amount),
                ad_creator['seller_coin_id'],
                ad_creator['asset_password'],
                direction=1)
            assert str(res.code) == str(code)
        except ApiException as e:
            pass

    @pytest.mark.parametrize('action,test_type,fail_type', test_limit_ad)
    def test_limit_ad(self, action, test_type, fail_type, otc_user):
        ad_creator = otc_user([ad_api, order_api, pay_mode_api])
        create_paymode(pay_mode_api, ad_creator['asset_password'])
        price, amount = get_random_data()
        if fail_type == 'lt':
            amount = 100 / price - 1

        if fail_type == 'gt':
            amount = 1000_000 / price + 100

        if action == 'sell':
            create_ad(ad_api, (price, amount), ad_creator['buyer_coin_id'],
                      ad_creator['asset_password'])
        else:
            create_ad(
                ad_api, (price, amount),
                ad_creator['buyer_coin_id'],
                ad_creator['asset_password'],
                direction=1)

    @pytest.mark.parametrize('action,test_type, fail_type', test_up_ad_data)
    def test_up_ad(self, action, test_type, fail_type, otc_user):
        ad_creator = otc_user([ad_api, order_api, pay_mode_api])
        create_paymode(pay_mode_api, ad_creator['asset_password'])
        price, amount = get_random_data()
        # 卖币, 创建卖币广告，使用卖方币种
        response = create_ad(ad_api, (price, amount),
                             ad_creator['buyer_coin_id'],
                             ad_creator['asset_password'])
        ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        assert ad_info.status == 1
        ad_api.advertise_put_off_ad_id_post(ad_id=response.ad_id)
        if test_type == 'up_normal':
            up_amount = (100 / price) + 1
        if test_type == 'up_mini':
            up_amount = (100 / price) - 0.1
        if test_type == 'up_large':
            up_amount = (1000_000 / price) + 100
        if fail_type == 'fail':
            try:
                ad_api.advertise_put_on_ad_id_amount_post(
                    ad_id=response.ad_id, amount=up_amount)
            except ApiException as e:
                assert 400 <= e.status < 500
            ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
            assert ad_info.status == 2  # 广告上线,不成功
        else:
            ad_api.advertise_put_on_ad_id_amount_post(
                ad_id=response.ad_id, amount=up_amount)
            ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
            assert ad_info.status == 1  # 广告上线

    # 编辑已上架且有成交订单的广告，点击编辑按钮-》编辑失败，提示该广告无法进行编辑
    @pytest.mark.parametrize('action,test_type, fail_type', test_edit_ad_data)
    def test_edit_ad(self, action, test_type, fail_type, otc_user):
        ad_creator = otc_user([ad_api, order_api, pay_mode_api])
        create_paymode(pay_mode_api, ad_creator['asset_password'])
        price, amount = get_random_data()
        # 卖币, 创建卖币广告，使用卖方币种
        response = create_ad(ad_api, (price, amount),
                             ad_creator['buyer_coin_id'],
                             ad_creator['asset_password'])
        ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        assert ad_info.status == 1
        all_ad = ad_api.advertise_my_list_get()
        before_ad_count = len([i for i in all_ad.items])

        if fail_type == 'fail':
            try:
                payload = UpdateAdvertisementRequest(
                    ad_id=response.ad_id,
                    price=price + 10,
                    asset_password=ad_creator['asset_password'])
                ad_api.advertise_update_put(payload)
            except ApiException as e:
                assert 400 <= e.status < 500
        else:
            ad_api.advertise_put_off_ad_id_post(ad_id=response.ad_id)
            payload = UpdateAdvertisementRequest(
                ad_id=response.ad_id,
                price=price + 10,
                asset_password=ad_creator['asset_password'])
            ad_api.advertise_update_put(payload)

        all_ad = ad_api.advertise_my_list_get()
        after_ad_count = len([i for i in all_ad.items])
        assert before_ad_count == after_ad_count

    @pytest.mark.parametrize('status,action,test_type', test_down_ad_data)
    def test_down_ad(self, status, action, test_type, otc_user):
        ad_creator = otc_user([ad_api, pay_mode_api])
        pay_way_id = create_paymode(pay_mode_api,
                                    ad_creator['asset_password'])
        price, amount = get_random_data()
        # 卖币
        response = create_ad(ad_api, (price, amount),
                             ad_creator['buyer_coin_id'],
                             ad_creator['asset_password'])

        # 创建用户
        order_creator = otc_user([order_api])

        if status == 'up_no_transaction':
            ad_api.advertise_put_off_ad_id_post(ad_id=response.ad_id)
            ad_on_lines = ad_api.advertise_online_list_get(
                currency_id=ad_creator['buyer_coin_id'],
                type='2',
                page_size=10)
            ids = [i.ad_id for i in ad_on_lines.items]
            assert response.ad_id not in ids
            return
        # 创建买币订单
        set_login_status(pay_mode_api, order_creator['user_token'])
        create_paymode(pay_mode_api, order_creator['asset_password'])
        create_order = CreateOrderRequest(ad_id=response.ad_id, amount=amount)
        res = order_api.order_create_post(create_order)
        ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        assert ad_info.status == 1  # 交易未成功，广告不下线

        # 买家确认
        order_api.order_buyer_paid_order_id_paymode_id_post(
            order_id=res.order_id, paymode_id=pay_way_id)
        # 卖家确认放行
        set_login_status(order_api, ad_creator['user_token'])
        order_api.order_seller_confirm_order_id_post(order_id=res.order_id)

        # 不在上线广告内
        time.sleep(1)
        ad_on_lines = ad_api.advertise_online_list_get(
            currency_id=ad_creator['buyer_coin_id'],
            type='2',
            page_size=10)
        ids = [i.ad_id for i in ad_on_lines.items]
        assert response.ad_id not in ids

        order_info = order_api.order_info_order_id_get(order_id=res.order_id)
        assert order_info.status == 30

        ad_info = ad_api.advertise_info_ad_id_get(ad_id=response.ad_id)
        assert ad_info.status == 2  # 交易成功

    @pytest.mark.parametrize('action,test_type, fail_type',
                             test_delete_ad_data)
    def test_delete_ad(self, action, test_type, fail_type, otc_user):
        price, amount = get_random_data()

        # 创建用户
        ad_creator = otc_user([ad_api, pay_mode_api])
        create_paymode(pay_mode_api, ad_creator['asset_password'])
        ad_res = create_ad(ad_api, (price, amount),
                           ad_creator['buyer_coin_id'],
                           ad_creator['asset_password'])

        set_login_status(staff_ad_api, ad_creator['admin_token'])
        # 删除下架广告
        if action == 'down_ad':
            ad_api.advertise_put_off_ad_id_post(ad_id=ad_res.ad_id)
            ad_count = staff_ad_api.admin_ad_user_ad_count_get(
                ad_creator['account_id'])
            assert ad_count.count == 1

            ad_info = staff_ad_api.admin_ad_find_page_get(ad_id=ad_res.ad_id)
            target_ad_ids = [i.ad_id for i in ad_info.items]
            assert ad_res.ad_id in target_ad_ids

            ad_api.advertise_delete_ad_id_delete(ad_id=ad_res.ad_id)
            ad_on_lines = ad_api.advertise_online_list_get(
                currency_id=ad_creator['buyer_coin_id'],
                type='2',
                page_size=10)
            ids = [i.ad_id for i in ad_on_lines.items]
            assert ad_res.ad_id not in ids
            # admin_ad_find_page_get', 'admin_ad_user_ad_count_get
            ad_count = staff_ad_api.admin_ad_user_ad_count_get(
                ad_creator['account_id'])
            assert ad_count.count == 0

            return
        # 删除上架广告
        try:
            ad_api.advertise_delete_ad_id_delete(ad_id=ad_res.ad_id)
        except ApiException as e:
            assert 400 <= e.status < 500
