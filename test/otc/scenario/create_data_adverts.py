# @author: lj
import pytest

from swagger_client.otc.api import AdvertisementApi, OrderApi, PaymodeApi
from swagger_client.otc.api import BalanceApi, AssetManagementApi
from test.otc.scenario.data.data import (get_random_data, test_up_ad_data, test_edit_ad_data,
                                         test_down_ad_data, test_delete_ad_data, test_create_ad_data)
from .util import create_ad, create_paymode

otc_bal_api = BalanceApi()
otc_asset_api = AssetManagementApi()
ad_api = AdvertisementApi()
order_api = OrderApi()
pay_mode_api = PaymodeApi()


class TestAdvert:
    @pytest.mark.parametrize('action,test_type, fail_type', test_up_ad_data)
    def test_up_ad(self, action, test_type, fail_type, otc_user):
        one_user_info = otc_user([ad_api, order_api, pay_mode_api])
        pay_way_id = create_paymode(pay_mode_api, one_user_info['asset_password'])
        price, amount = get_random_data()
        # 卖币
        for i in range(10):
            response = create_ad(ad_api, (price, amount), one_user_info['seller_coin_id'], one_user_info['asset_password'])
            response = create_ad(ad_api, (price, amount), one_user_info['seller_coin_id'], one_user_info['asset_password'], direction=1)
        return
