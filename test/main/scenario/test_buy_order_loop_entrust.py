# -*- coding: utf-8 -*-
# @File :  test_stoploss_buy.py
# @Author : lh
# @time : 19-1-24 下午5:06
import time

import pytest
import logging

from common.account_sign import set_login_status
from swagger_client.main.models.post_entrusts_request import PostEntrustsRequest
from swagger_client.main.api.account_api import AccountApi
from swagger_client.main.api.entrust_api import EntrustApi
from swagger_client.main.api.asset_management_api import AssetManagementApi

from test.main.scenario.profitloss_data import quotation_data, QUOTATIONS_FIELDS, get_random_price_and_volume

main_ac_api = AccountApi()
main_entrust_api = EntrustApi()
main_asset_api = AssetManagementApi()
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler)


class TestBuyOrderLoopEntrust:
    @pytest.mark.parametrize(QUOTATIONS_FIELDS, quotation_data)
    def testbuyorderloopentrust(self, market_id, price, entrust_type, trade_type, volume, trigger_price, auto_cancel_at,
                                exchange_ids, coin_id, sell_coin_id, trading_area_id, symbol, quotation_special_login):
        # login
        quotation_special_login([main_entrust_api, main_ac_api])
        payload = PostEntrustsRequest()
        payload.price = 1000_00
        payload.entrust_type = 'market'
        payload.trade_type = 'sell'
        # payload.trigger_price = trigger_price
        payload.volume = 100000_00
        # payload.auto_cancel_at = auto_cancel_at
        # login
        payload.market_id = market_id

        # 清空
        main_entrust_api.entrusts_post(body=payload)
        payload.trade_type = 'buy'
        main_entrust_api.entrusts_post(body=payload)

        # seller_user_login
        buyer_special_info = quotation_special_login([main_ac_api, main_entrust_api, main_asset_api])

        # sellser_user login
        seller_special_info = quotation_special_login([main_ac_api, main_entrust_api, main_asset_api])

        buyer_order_list = []
        seller_order_list = []
        buy_order_deal_time = []
        sell_order_deal_time = []
        for i in range(100):
            price, volume = get_random_price_and_volume(buyer_special_info['precision'])
            payload = PostEntrustsRequest()
            payload.market_id = market_id
            logger.info(f'下单价格:{price}')
            payload.price = price
            payload.entrust_type = entrust_type
            payload.trade_type = 'buy'
            payload.trigger_price = trigger_price
            payload.volume = volume
            payload.auto_cancel_at = auto_cancel_at

            # 买方登陆
            set_login_status(main_entrust_api, buyer_special_info['token'])
            set_login_status(main_asset_api, buyer_special_info['token'])
            # 查询买方下单前资产余额
            before_buyer_usdt_info = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
            logger.info(f'买方usdt余额信息:{before_buyer_usdt_info}')
            before_buyer_usdt_bal = before_buyer_usdt_info.balance
            before_buyer_coin_info = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=sell_coin_id)
            logger.info(f'买方xlm余额信息:{before_buyer_coin_info}')
            before_buyer_coin_bal = before_buyer_coin_info.balance
            # 下买单
            payload.price = price + 0.05
            buy_order_res = main_entrust_api.entrusts_post(body=payload)
            buy_order_id = buy_order_res.order_id

            # 卖方登陆
            set_login_status(main_entrust_api, seller_special_info['token'])
            set_login_status(main_asset_api, seller_special_info['token'])

            # 查询卖方下单前资产余额
            before_seller_usdt_info = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
            logger.info(f'卖方下单前usdt余额信息:{before_seller_usdt_info}')
            before_seller_usdt_bal = before_seller_usdt_info.balance
            before_seller_coin_info = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=sell_coin_id)
            logger.info(f'卖方下单前xlm余额信息:{before_seller_coin_info}')
            before_seller_coin_bal = before_seller_coin_info.balance

            # 下卖单
            payload.trade_type = 'sell'
            sell_order_res = main_entrust_api.entrusts_post(body=payload)
            sell_order_id = sell_order_res.order_id
            time.sleep(5)

            # 查询卖方下单后的资产余额
            set_login_status(main_asset_api, seller_special_info['token'])
            set_login_status(main_entrust_api, seller_special_info['token'])
            after_seller_usdt_info = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
            logger.info(f'卖方下单后usdt余额信息:{after_seller_usdt_info}')
            after_serller_usdt_bal = after_seller_usdt_info.balance
            after_serller_coin_info = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
            logger.info(f'卖方下单后coin余额信息:{after_serller_coin_info}')
            after_serller_coin_bal = after_serller_coin_info.balance

            # 查询买方下单后的资产余额
            set_login_status(main_ac_api, buyer_special_info['token'])
            set_login_status(main_entrust_api, buyer_special_info['token'])
            set_login_status(main_asset_api, buyer_special_info['token'])
            after_buyer_usdt_info = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=coin_id)
            logger.info(f'买方下单后usdt余额信息:{after_buyer_usdt_info}')
            after_buyer_usdt_bal = after_buyer_usdt_info.balance
            after_buyer_coin_info = main_asset_api.asset_mgmt_assets_coin_id_get(coin_id=sell_coin_id)
            logger.info(f'买方下单后xlm余额:{after_buyer_coin_info}')
            after_buyer_coin_bal = after_buyer_coin_info.balance

            # 查询买方委托成交记录
            success_deal_history = main_entrust_api.trades_get(order_id=buy_order_id)
            buy_order_deal_list = success_deal_history.items
            buyer_entrust_res = main_entrust_api.entrusts_get()
            buyer_entrust_list = [i for i in buyer_entrust_res.items if i.order_id == buy_order_id]
            buy_order_create_time = buy_order_deal_list[0].create_at
            buy_order_deal_time = buyer_entrust_list[0].created_at
            logger.info(f'委托成交记录:{buy_order_deal_list}')
            if buy_order_deal_list:
                buyer_order_list.append(buy_order_deal_list[0].order_id)

            # 查询卖方委托成交记录
            set_login_status(main_entrust_api, seller_special_info['token'])
            success_deal_history = main_entrust_api.trades_get(order_id=buy_order_id)
            seller_order_deal_list = success_deal_history.items
            seller_entrust_res = main_entrust_api.entrusts_get()
            seller_entrust_list = [i for i in seller_entrust_res.items if i.order_id == sell_order_id]
            sell_order_create_time = seller_entrust_list[0].create_at
            sell_order_deal_time = seller_order_deal_list[0].created_at
            logger.info(f'委托成交记录:{seller_order_deal_list}')
            if seller_order_deal_list:
                seller_order_list.append(seller_order_deal_list[0].order_id)

            # 计算成交单的时间
            buy_order_deal_sec = buy_order_deal_time - buy_order_create_time
            buy_order_deal_time.append(buy_order_deal_sec)
            logger.info(f'买单成交时间:{buy_order_deal_sec}')
            sell_order_deal_sec = sell_order_deal_time - sell_order_create_time
            buy_order_deal_time.append(sell_order_deal_sec)
            logger.info(f'卖单成交时间:{sell_order_deal_sec}')

            # 获取费率
            total_rate = seller_special_info['total_rate']

            assert round(float(before_buyer_coin_bal), 8) + round((price * volume)(1 - total_rate),
                                                                  8) == after_buyer_coin_bal
            assert round(float(before_seller_usdt_bal), 8) + round((price * volume)(1 - total_rate),
                                                                   8) == after_buyer_usdt_bal
        # 计算撮合平均时间
        buy_deal_avg_time = sum(buy_order_deal_time)
        sell_deal_avg_time = sum(buy_order_deal_time)
        deal_avg_time = (buy_deal_avg_time + sell_deal_avg_time) / 200
        logger.info(f'平均撮合一单的时间:{deal_avg_time}')
