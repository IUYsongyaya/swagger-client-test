# -*- coding: utf-8 -*-
# @File :  test_asset.py
# @Author : lh
import decimal
import pytest
import requests
import logging
from common.account_sign import get_admin_token, set_login_status
from swagger_client.otc import TransferFromRequest, TransferToRequest
from swagger_client.otc.api import AssetManagementApi as Otcasset, BalanceApi
from swagger_client.otc.api import AccountApi
from swagger_client.otc.rest import ApiException
from swagger_client.main.api import AssetManagementApi

from swagger_client.staff.api import AssetManagementApi as StaffAsset
from swagger_client.staff.api import BalanceApi as StaffBal
from swagger_client.staff.rest import ApiException as StaffApiException
from test.otc.scenario.data.data1 import test_asset_Data, FIELDS, test_trans_coin_legals, test_trans_legals_coin, \
    test_trans_coin_legals_fail, test_trans_legals_coin_fail

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

main_asset_api = AssetManagementApi()
otc_ac_api = AccountApi()
otc_asset_api = Otcasset()
otc_balance_api = BalanceApi()
staff_asset_api = StaffAsset()
staff_balance_api = StaffBal()


class TestAsset:
    # 获取资产信息，资产信息显示正确，币币余额与主平台用户资产数据一致
    # 币币划转到法币-> 选择某一币种，点击立即划转-》在资金划转页面中，选择需要划转的币种与数量、划转平台为币币，点击确定 -> 资产划转成功，币币余额减少，法币余额增加，主平台资产余额余币币余额资产数量一致
    # 币币划转到法币-> 选择某一币种，划转数量超出币币余额点击立即划转-> 失败，提示余额不足

    # 法币到币币 -> 选择某一币种，点击立即划转-> 在资金划转页面中，选择需要划转的币种与数量、划转平台为法币，点击确定 -> 资产划转成功，法币余额减少，币币余额增加，主平台资产余额余币币余额资产数量一致
    # 法币到币币 -> 选择某一币种，划转数量超出币币余额点击立即划转-> 失败，提示余额不足

    # 进行一笔币币划转到法币平台，划转成功，在资产明细列表中显示一笔类型为转入的记录，记录信息显示正确
    # 进行一笔法币划转到币币平台，划转成功，在资产明细列表中显示一笔类型为转出的记录，记录信息显示正确

    # 币币划转到法币 -> 选择某一币种
    @pytest.mark.parametrize('amount, coin_name', test_asset_Data)
    def test_asset(self, amount, coin_name, otc_user):
        """
        资产信息正确,币币余额与主平台用户资产数据一致
        """
        # 后台登录验证
        staff_token = get_admin_token()
        set_login_status(staff_balance_api, staff_token)
        set_login_status(staff_asset_api, staff_token)
        user_res_info = otc_user([otc_balance_api, otc_asset_api, main_asset_api, otc_ac_api])
        # 获取otc平台account_id
        coin_id = user_res_info['buyer_coin_id']
        account_res = otc_ac_api.accounts_account_info_get()
        account_id = account_res.account_info.account_id
        # 获取主平台币币余额
        main_bb_res = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        # logger.info('主平台某一币种bb余额:', main_bb_res)
        assert main_bb_res
        # 获取后台币币余额
        bb_bal_list = staff_asset_api.asset_mgmt_assets_id_get(id=account_id)
        assert bb_bal_list.items
        bb_bal_assetinfo = bb_bal_list.items
        staff_bb_bal = [i for i in bb_bal_assetinfo if i.coin_name == coin_name]
        # logger.info('币币余额列表信息:', staff_bb_bal)
        # 获取后台法币余额
        rec = staff_balance_api.admin_balance_user_balance_list_get(user_id=account_id)
        assert rec.items
        staff_fb_bal = [i for i in rec.items if i.currency_id == str(coin_id)]
        # 获取otc平台资产币币余额
        otc_asset_info = otc_asset_api.asset_mgmt_assets_get()
        otc_coin_info = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        logger.info(f'otc币币余额:{otc_asset_info}')
        logger.info(f'amount:{amount}')
        target_bb_assert_info = [i for i in otc_asset_info if i['coinName'] == coin_name]
        assert main_bb_res.balance == target_bb_assert_info[0]['balance']
        assert main_bb_res.frozen == target_bb_assert_info[0]['frozen']

        assert float(staff_bb_bal[0].balance) == float(target_bb_assert_info[0]['balance'])
        assert float(staff_bb_bal[0].frozen) == float(target_bb_assert_info[0]['frozen'])
        assert float(staff_bb_bal[0].balance) == float(otc_coin_info.balance)
        assert float(staff_bb_bal[0].frozen) == float(otc_coin_info.frozen)
        # 获取otc平台资产法币余额
        otc_fb_list = otc_balance_api.balance_list_get()
        otc_coin_fb_info = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        assert otc_fb_list.items
        otc_fb_rec = [i for i in otc_fb_list.items if i.currency_id == str(coin_id)]
        # logger.info(f'otcfb余额:{otc_fb_rec}')
        assert otc_fb_rec[0].available == staff_fb_bal[0].available
        assert otc_fb_rec[0].frozen == staff_fb_bal[0].frozen
        assert otc_coin_fb_info.available == staff_fb_bal[0].available
        assert otc_coin_fb_info.frozen == staff_fb_bal[0].frozen

    @pytest.mark.parametrize(FIELDS, test_trans_legals_coin)
    def test_legals_trans_coin_success(self, amount, coin_name, otc_user):
        """
        法币划转到币币成功
        """
        # otc平台,后台登录验证
        user_res_info = otc_user([otc_balance_api, otc_asset_api, otc_ac_api, main_asset_api])
        coin_id = user_res_info['buyer_coin_id']
        staff_token = get_admin_token()
        set_login_status(staff_balance_api, staff_token)
        set_login_status(staff_asset_api, staff_token)
        # 获取otc平台account_id
        account_res = otc_ac_api.accounts_account_info_get()
        account_id = account_res.account_info.account_id
        # 获取otc法币余额，币币余额
        before_coin_fb_res1 = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        logger.info(f'法币余额:{before_coin_fb_res1}')
        before_fb_list = otc_balance_api.balance_list_get()
        assert before_coin_fb_res1
        assert before_fb_list
        before_fb_rec = [i for i in before_fb_list.items if i.currency_id == str(coin_id)]
        before_fb_bal = before_fb_rec[0].available
        before_coin_fb_bal = before_coin_fb_res1.available

        before_coin_bb_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        before_bb_list_res2 = otc_asset_api.asset_mgmt_assets_get()
        before_bb_list_rec = [i for i in before_bb_list_res2 if i['coinName'] == coin_name]
        before_bb_bal = before_bb_list_rec[0]['balance']
        before_coin_bb_bal = before_coin_bb_res2.balance
        assert before_coin_bb_res2
        assert before_bb_list_res2
        # 获取主平台币币余额
        main_before_res1 = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        main_before_bb_bal = main_before_res1.balance
        # 获取后台币币余额，法币余额
        staff_before_fb_res = staff_balance_api.admin_balance_user_balance_list_get(user_id=account_id)
        assert staff_before_fb_res.items
        staff_before_fb_list1 = [i for i in staff_before_fb_res.items if i.currency_id == coin_id]
        staff_before_fb_bal = staff_before_fb_list1[0].available
        staff_before_bb_res2 = staff_asset_api.asset_mgmt_assets_id_get(id=account_id)
        assert staff_before_bb_res2.items
        staff_before_bb_list2 = [i for i in staff_before_bb_res2.items if i.coin_name == coin_name]
        staff_before_bb_bal = staff_before_bb_list2[0].balance
        # 法币划转到币币成功
        transload = TransferToRequest(currency_id=coin_id, amount=amount)
        otc_balance_api.balance_transfer_to_post(transload)
        # 获取otc法币余额，币币余额
        after_coin_fb_res1 = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        after_fb_list = otc_balance_api.balance_list_get()
        after_fb_rec = [i for i in after_fb_list.items if i.currency_id == str(coin_id)]
        after_fb_bal = after_fb_rec[0].available
        after_coin_fb_bal = after_coin_fb_res1.available
        assert after_coin_fb_res1
        assert after_fb_list

        after_bb_coin_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        after_bb_list_res2 = otc_asset_api.asset_mgmt_assets_get()
        after_bb_list_rec = [i for i in after_bb_list_res2 if i['coinName'] == coin_name]
        after_bb_bal = after_bb_list_rec[0]['balance']
        after_coin_bb_bal = after_bb_coin_res2.balance
        logger.info(f'amount:{amount}')
        logger.info(f'before_asset:{before_fb_bal, after_fb_bal, amount}')
        assert round(float(before_fb_bal) - amount, 8) == round(float(after_fb_bal), 8)
        logger.info(f'before_coin_fb_bal:{before_coin_fb_bal, after_coin_fb_bal, amount}')
        assert round(float(before_coin_fb_bal) - amount, 8) == round(float(after_coin_fb_bal), 8)
        logger.info(f'before_bb_bal:{before_bb_bal, after_bb_bal, amount}')
        assert round(float(before_bb_bal) + amount, 8) == round(float(after_bb_bal), 8)
        logger.info(f'before_coin_bb_bal:{before_coin_bb_bal, after_coin_bb_bal, amount}')
        assert round(float(before_coin_bb_bal) + amount, 8) == round(float(after_coin_bb_bal), 8)
        # 获取主平台币币余额
        main_after_res1 = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        main_after_bal = main_after_res1.balance
        assert round(float(main_after_bal), 8) == round(float(main_before_bb_bal) + amount, 8)
        # 获取后台法币,币币余额
        staff_after_res1 = staff_balance_api.admin_balance_user_balance_list_get(user_id=account_id)
        assert staff_after_res1.items
        staff_after_list1 = [i for i in staff_after_res1.items if i.currency_id == coin_id]
        logger.info(f'staff_after_list1:{staff_after_list1}')
        staff_after_fb_bal = staff_after_list1[0].available
        staff_after_res2 = staff_asset_api.asset_mgmt_assets_id_get(id=account_id)
        assert staff_after_res2.items
        staff_after_list2 = [i for i in staff_after_res2.items if i.coin_name == coin_name]
        staff_after_bb_bal = staff_after_list2[0].balance
        assert round(float(staff_after_bb_bal), 8) == round(float(staff_before_bb_bal) + amount, 8)
        assert round(float(staff_after_bb_bal), 8) == round(float(before_bb_bal) + amount, 8)
        assert round(float(staff_after_bb_bal), 8) == round(float(before_coin_bb_bal) + amount, 8)
        assert round(float(staff_after_fb_bal), 8) == round(float(staff_before_fb_bal) - amount, 8)
        assert round(float(staff_after_fb_bal), 8) == round(float(before_fb_bal) - amount, 8)
        assert round(float(staff_after_fb_bal), 8) == round(float(before_coin_fb_bal) - amount, 8)

        # otc查询流水转出的记录
        otc_transto_list = otc_balance_api.balance_get_flow_get()
        logger.info(f'流水记录:{otc_transto_list}')
        otc_transto_info = [i.amount for i in otc_transto_list.items]
        logger.info(f'流水列表:{otc_transto_info}')
        amount = decimal.Decimal(str(amount)).quantize(decimal.Decimal('0.00000000'))
        assert str(amount) in otc_transto_info

        # 后台查询流水转出记录
        staff_transto_list = staff_balance_api.admin_balance_user_balance_flow_get(user_id=account_id)
        staff_transto_info = [i.amount for i in staff_transto_list.items]
        assert str(amount) in staff_transto_info

    @pytest.mark.parametrize(FIELDS, test_trans_coin_legals)
    def test_coin_trans_legals_success(self, amount, coin_name, otc_user):
        """
        币币划转法币成功
        """
        # otc平台,后台登录验证
        user_res_info = otc_user([otc_balance_api, otc_asset_api, otc_ac_api, main_asset_api])
        coin_id = user_res_info['buyer_coin_id']
        staff_token = get_admin_token()
        set_login_status(staff_balance_api, staff_token)
        set_login_status(staff_asset_api, staff_token)
        # 获取otc平台account_id
        account_res = otc_ac_api.accounts_account_info_get()
        account_id = account_res.account_info.account_id
        # 获取otc法币余额，币币余额
        before_coin_fb_res1 = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        before_fb_list = otc_balance_api.balance_list_get()
        assert before_coin_fb_res1
        assert before_fb_list
        before_fb_rec = [i for i in before_fb_list.items if i.currency_id == str(coin_id)]
        before_fb_bal = before_fb_rec[0].available
        before_coin_fb_bal = before_coin_fb_res1.available

        before_coin_bb_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        logger.info(f'otc币币余额：{before_coin_bb_res2}')
        before_bb_list_res2 = otc_asset_api.asset_mgmt_assets_get()
        before_bb_list_rec = [i for i in before_bb_list_res2 if i['coinName'] == coin_name]
        before_bb_bal = before_bb_list_rec[0]['balance']
        before_coin_bb_bal = before_coin_bb_res2.balance
        assert before_coin_bb_res2
        assert before_bb_list_res2
        # 获取主平台币币余额
        main_before_res1 = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        main_before_bb_bal = main_before_res1.balance
        # 获取后台币币余额，法币余额
        staff_before_fb_res = staff_balance_api.admin_balance_user_balance_list_get(user_id=account_id)
        assert staff_before_fb_res.items
        staff_before_fb_list1 = [i for i in staff_before_fb_res.items if i.currency_id == coin_id]
        staff_before_fb_bal = staff_before_fb_list1[0].available
        staff_before_bb_res2 = staff_asset_api.asset_mgmt_assets_id_get(id=account_id)
        assert staff_before_bb_res2.items
        staff_before_bb_list2 = [i for i in staff_before_bb_res2.items if i.coin_name == coin_name]
        staff_before_bb_bal = staff_before_bb_list2[0].balance
        # 币币划转法币成功
        transload = TransferFromRequest(currency_id=coin_id, amount=amount)
        otc_balance_api.balance_transfer_from_post(transload)
        # 获取otc法币余额，币币余额
        after_coin_fb_res1 = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        after_fb_list = otc_balance_api.balance_list_get()
        after_fb_rec = [i for i in after_fb_list.items if i.currency_id == str(coin_id)]
        after_fb_bal = after_fb_rec[0].available
        after_coin_fb_bal = after_coin_fb_res1.available
        assert after_coin_fb_res1
        assert after_fb_list

        after_bb_coin_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        after_bb_list_res2 = otc_asset_api.asset_mgmt_assets_get()
        after_bb_list_rec = [i for i in after_bb_list_res2 if i['coinName'] == coin_name]
        after_bb_bal = after_bb_list_rec[0]['balance']
        after_coin_bb_bal = after_bb_coin_res2.balance

        assert round(float(before_fb_bal) + amount, 8) == round(float(after_fb_bal), 8)
        assert round(float(before_coin_fb_bal) + amount, 8) == round(float(after_coin_fb_bal), 8)
        assert round(float(before_bb_bal) - amount, 8) == round(float(after_bb_bal), 8)
        assert round(float(before_coin_bb_bal) - amount, 8) == round(float(after_coin_bb_bal), 8)
        # 获取主平台币币余额
        main_after_res1 = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        main_after_bal = main_after_res1.balance
        assert round(float(main_after_bal), 8) == round(float(main_before_bb_bal) - amount, 8)
        # 获取后台法币,币币余额
        staff_after_res1 = staff_balance_api.admin_balance_user_balance_list_get(user_id=account_id)
        assert staff_after_res1.items
        staff_after_list1 = [i for i in staff_after_res1.items if i.currency_id == coin_id]
        logger.info(f'staff_after_list1:{staff_after_list1}')
        staff_after_fb_bal = staff_after_list1[0].available
        staff_after_res2 = staff_asset_api.asset_mgmt_assets_id_get(id=account_id)
        assert staff_after_res2.items
        staff_after_list2 = [i for i in staff_after_res2.items if i.coin_name == coin_name]
        staff_after_bb_bal = staff_after_list2[0].balance
        assert round(float(staff_after_bb_bal), 8) == round(float(staff_before_bb_bal) - amount, 8)
        assert round(float(staff_after_bb_bal), 8) == round(float(before_bb_bal) - amount, 8)
        assert round(float(staff_after_bb_bal), 8) == round(float(before_coin_bb_bal) - amount, 8)
        assert round(float(staff_after_fb_bal), 8) == round(float(staff_before_fb_bal) + amount, 8)
        assert round(float(staff_after_fb_bal), 8) == round(float(before_fb_bal) + amount, 8)
        assert round(float(staff_after_fb_bal), 8) == round(float(before_coin_fb_bal) + amount, 8)

        # otc查询流水转出的记录
        otc_transfrom_list = otc_balance_api.balance_get_flow_get()
        otc_transfrom_info = [i.amount for i in otc_transfrom_list.items]
        amount = decimal.Decimal(str(amount)).quantize(decimal.Decimal('0.00000000'))
        assert str(amount) in otc_transfrom_info

        # 后台查询流水转出记录
        staff_transto_list = staff_balance_api.admin_balance_user_balance_flow_get(user_id=account_id)
        staff_transfrom_info = [i.amount for i in staff_transto_list.items]
        assert str(amount) in staff_transfrom_info

    @pytest.mark.parametrize(FIELDS, test_trans_coin_legals_fail)
    def test_coin_trans_legals_fail(self, amount, coin_name, otc_user):
        """
        币币化转到法币失败
        """
        # 后台登录验证
        staff_token = get_admin_token()
        set_login_status(staff_balance_api, staff_token)
        set_login_status(staff_asset_api, staff_token)
        user_res_info = otc_user([otc_balance_api, otc_asset_api])
        coin_id = user_res_info['buyer_coin_id']
        # 获取otc法币余额，币币余额
        before_res1 = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        assert before_res1
        before_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        assert before_res2
        # 币币划转到法币失败
        transload = TransferFromRequest(currency_id=coin_id, amount=amount)
        try:
            otc_balance_api.balance_transfer_from_post(transload)
        except ApiException as e:
            assert e.status == 400
        # 获取otc法币余额，币币余额
        after_res1 = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        assert round(float(after_res1.available), 8) == round(float(before_res1.available), 8)
        after_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        assert round(float(after_res2.balance), 8) == round(float(before_res2.balance), 8)

    @pytest.mark.parametrize(FIELDS, test_trans_legals_coin_fail)
    def test_legals_trans_coin_fail(self, amount, coin_name, otc_user):
        """
        法币化转到币币失败
        """
        # 后台登录验证
        staff_token = get_admin_token()
        set_login_status(staff_balance_api, staff_token)
        set_login_status(staff_asset_api, staff_token)
        user_res_info = otc_user([otc_balance_api, otc_asset_api])
        coin_id = user_res_info['buyer_coin_id']
        # 获取otc法币余额，币币余额
        before_res1 = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        assert before_res1
        before_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        assert before_res2
        # 币币划转到法币失败
        transload = TransferToRequest(currency_id=coin_id, amount=amount)
        try:
            otc_balance_api.balance_transfer_to_post(transload)
        except ApiException as e:
            assert e.status == 400
        # 获取otc法币余额，币币余额
        after_res1 = otc_balance_api.balance_info_currency_id_get(currency_id=coin_id)
        assert round(float(after_res1.available), 8) == round(float(before_res1.available), 8)
        after_res2 = otc_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
        assert round(float(after_res2.balance), 8) == round(float(before_res2.balance), 8)
