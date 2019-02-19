# @author: lj
import random
import time
import pytest
from common.account_sign import set_login_status
from swagger_client.otc.api import AccountApi, PaymodeApi, AdvertisementApi, OrderApi
from swagger_client.otc.models import PostPaymodeRequest, PaymodeInfo, CreateOrderRequest, UpdatePaymodeRequest
from swagger_client.otc.rest import ApiException
from swagger_client.staff.api import PaymodeApi as StaffPaymodeApi, AccountManagementApi as StaffAccountApi
from common.account_sign import set_login_status
from .util import create_ad, get_random_data, get_random_lowercase

account_api = AccountApi()
pay_mode_api = PaymodeApi()
ad_api = AdvertisementApi()
order_api = OrderApi()
staff_pay_mode_api = StaffPaymodeApi()
staff_account_api = StaffAccountApi()


class TestUserCenter:
    @pytest.mark.parametrize("way,status", [('bank', 'success'),
                                            ('ali_pay', 'success'),
                                            ('we_chat', 'success')
                                            ])
    def test_add_pay_mode(self, way, status, otc_user):
        payload = PostPaymodeRequest()
        type_map = {"bank": 3, "ali_pay": 2, "we_chat": 1}
        payload.type = type_map[way]
        payload.account = "liujun@192.com"
        payload.qrcode = 'qr_code'
        payload.status = 1
        user_info = otc_user([pay_mode_api])
        payload.asset_password = user_info['asset_password']
        print(user_info)
        if way == 'bank':
            payload.bank_name = "招商银行"
            payload.branch_name = "深圳罗湖支行"
        res = pay_mode_api.paymode_add_post(body=payload)
        active_pay_ways = pay_mode_api.paymode_my_list_get()
        pay_way_ids = [i.id for i in active_pay_ways.items]
        assert res.id in pay_way_ids
        pay_way_info = pay_mode_api.paymode_info_id_get(id=pay_way_ids[0])
        assert pay_way_info.account == 'liujun@192.com'

        time.sleep(5)
        set_login_status(staff_account_api, user_info['user_token'])
        res = staff_account_api.accounts_otc_get(account_id=user_info['account_id'])
        assert res.items[0].account_id == user_info['account_id']

    @pytest.mark.parametrize(
        "flag,way,status, test_type",
        [("has_processing", "ali_pay", "fail", "delete"),
         ("has_processing", "we_chat", "fail", "delete"),
         ("has_processing", "bank", "fail", "delete"),
         ("no_processing", "ali_pay", "success", "delete"),
         ("no_processing", "we_chat", "success", "delete"),
         ("no_processing", "bank", "success", "delete"),
         ("has_processing", "ali_pay", "fail", "update"),
         ("has_processing", "we_chat", "fail", "update"),
         ("has_processing", "bank", "fail", "update"),
         ("no_processing", "ali_pay", "success", "update"),
         ("no_processing", "we_chat", "success", "update"),
         ("no_processing", "bank", "success", "update")
         ])
    def test_change_pay_mode(self, flag, way, status, test_type, otc_user):
        """
        先创建广告，然后绑定支付方式，然后下单，设定好支付方式，然后再删除设定好的支付方式
        :return:
        """
        # 新增支付方式并启用
        payload = PostPaymodeRequest()
        type_map = {"bank": 3, "ali_pay": 2, "we_chat": 1}
        payload.type = type_map[way]
        payload.qrcode = 'qr_code'
        payload.account = "liujun@192.com"
        user_info = otc_user([pay_mode_api, ad_api])
        payload.asset_password = user_info['asset_password']
        if way == 'bank':
            payload.bank_name = "招商银行"
            payload.branch_name = "深圳罗湖支行"
        one_pay_way_res = pay_mode_api.paymode_add_post(body=payload)
        pay_mode_api.paymode_enable_paymode_id_put(paymode_id=one_pay_way_res.id)
        # 新增支付方式 并启用
        pay_way_res = pay_mode_api.paymode_add_post(body=payload)
        pay_mode_api.paymode_enable_paymode_id_put(paymode_id=pay_way_res.id)

        # 新增广告
        price, amount = get_random_data()
        ad = create_ad(ad_api, (price, amount), user_info['buyer_coin_id'], user_info['asset_password'])
        # create new user
        otc_user([order_api])
        if flag == 'has_processing':
            ad_info = ad_api.advertise_info_ad_id_get(ad_id=ad.ad_id)
            print(ad_info)
            # 创建订单
            create_order = CreateOrderRequest(ad_id=ad.ad_id, amount=amount-round(100 / price, 2))
            order_api.order_create_post(create_order)
            # 买家确认支付
            # order_api.order_buyer_paid_order_id_paymode_id_post(order_id=res.order_id, paymode_id=pay_way_res.id)

        if test_type == "delete":
            try:
                pay_mode_api.paymode_disable_paymode_id_put(paymode_id=pay_way_res.id)
                pay_mode_api.paymode_delete_paymode_id_delete(paymode_id=pay_way_res.id)
            except ApiException as e:
                if status == "fail":
                    assert e.status != 200  # 删除失败
                else:
                    raise e

        if test_type == 'success':
            my_pay_modes = pay_mode_api.paymode_my_list_get()
            my_paymode_ids = [i.id for i in my_pay_modes]
            assert pay_way_res.id not in my_paymode_ids

        if test_type == 'update':
            try:
                put_load = UpdatePaymodeRequest(id=pay_way_res.id, account="liujun@1993.com", asset_password=user_info["asset_password"])
                pay_mode_api.paymode_update_put(put_load)
            except ApiException as e:
                if status == "fail":
                    assert e.status != 200
                else:
                    raise e

    def test_add_times_limit(self, otc_user):
        payload = PostPaymodeRequest()
        type_map = {"bank": 3, "ali_pay": 2, "we_chat": 1}
        payload.status = 0
        ways = ["bank", "ali_pay", "we_chat"]
        pay_ids = []
        user_info = otc_user([pay_mode_api])
        payload.asset_password = user_info['asset_password']
        for i in range(10):
            payload.qrcode = get_random_lowercase(10)
            payload.account = f"liujun@19{i}.com"
            way = random.choice(ways)
            payload.type = type_map[way]
            if way == 'bank':
                payload.bank_name = "招商银行"
                payload.branch_name = "深圳罗湖支行"
            pay_way_res = pay_mode_api.paymode_add_post(body=payload)
            pay_ids.append(pay_way_res.id)

        # 测试最多可以三个启用
        first_three = pay_ids[:3]
        print(first_three)
        for i in first_three:
            pay_mode_api.paymode_enable_paymode_id_put(paymode_id=i)

        try:
            paymode_id = pay_ids[5]
            pay_mode_api.paymode_enable_paymode_id_put(paymode_id=paymode_id)
        except ApiException as e:
            assert e.status == 400

        # 后台获取开启的支付方式列表
        pay_mode_api.paymode_disable_paymode_id_put(paymode_id=first_three[2])
        set_login_status(staff_pay_mode_api, user_info['admin_token'])
        opend_paymodes = staff_pay_mode_api.admin_paymode_user_list_get(user_id=user_info['account_id'])
        assert set(first_three[:2]) == set([i.id for i in opend_paymodes.items])

        # 测试最多十个
        way = random.choice(ways)
        payload.type = type_map[way]
        if way == 'bank':
            payload.bank_name = "招商银行"
            payload.branch_name = "深圳罗湖支行"
        try:
            pay_mode_api.paymode_add_post(body=payload)
        except ApiException as e:
            assert e.status == 400

        # 删除支付方式
        pay_mode_api.paymode_delete_paymode_id_delete(pay_ids[9])

        # 获取自己的支付方式列表
        my_pay_modes = pay_mode_api.paymode_my_list_get(page_size=10)
        assert len(my_pay_modes.items) == 9
