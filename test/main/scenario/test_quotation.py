# -*- coding: utf-8 -*-
# @File :  test_quotation.py
# @Author : lh
import pytest
import logging

import swagger_client.main
from swagger_client.main.api.entrust_api import EntrustApi  # NOQA: F401
from swagger_client.main.api.quotation_api import QuotationApi
from swagger_client.main.api.account_api import AccountApi
from swagger_client.tenant import GetDashboardHistoricalDataRequest
from swagger_client.tenant.api.quotation_api import QuotationApi as TenantQuotationApi
from swagger_client.tenant.api.account_api import AccountApi as TenantAccountApi
from swagger_client.tenant.api.exchange_entrust_api import ExchangeEntrustApi
from swagger_client.tenant.models.get_historical_data_request import GetHistoricalDataRequest \
    as TenantGetHistoricalDataRequest
from swagger_client.tenant.api.dashboard_api import DashboardApi
from swagger_client.venture.api.quotation_api import QuotationApi as VentureQuotationApi
from .profitloss_data import (quotation_data, QUOTATIONS_FIELDS)

logger = logging.getLogger('test_same_price_volume_deal_success')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

main_entrust_api = swagger_client.main.api.entrust_api.EntrustApi()
main_quota_api = QuotationApi()
main_ac_api = AccountApi()
tenant_account_api = TenantAccountApi()
tenant_quota_api = TenantQuotationApi()
tenant_dashboard_api = DashboardApi()
tenant_exchange_api = ExchangeEntrustApi()
venture_quota_api = VentureQuotationApi()


class TestSamePriceVolumeDealSuccess:
    @pytest.mark.parametrize(QUOTATIONS_FIELDS, quotation_data)
    def test_same_price_volume_success(self, market_id, price, entrust_type, trade_type, volume, trigger_price,
                                       auto_cancel_at, exchange_ids, coin_id, sell_coin_id, trading_area_id, symbol,
                                       set_tenant_login):

        set_tenant_login(
            [main_entrust_api, main_ac_api, main_quota_api, tenant_quota_api, venture_quota_api, tenant_account_api,
             tenant_dashboard_api, tenant_account_api, tenant_exchange_api])

        # 查看租户平台账户信息
        ac_info = main_ac_api.accounts_account_info_get()
        # logging.info(f'账户信息:{ac_info}')
        print('账户信息:', ac_info)
        # assert isinstance(ac_info, )

        # 获取主平台单一币种在各交易所的行情概要
        overview_res = main_quota_api.quotation_id_overview_get(id=sell_coin_id)
        overview_dict_res = overview_res.to_dict()
        print('主平台单一币种在各交易所的行情概要:', overview_res)
        assert hasattr(overview_res, 'avg_cny_price')
        assert 'avg_cny_price' in overview_dict_res
        assert 'avg_usdprice' in overview_dict_res
        assert 'change_pct' in overview_dict_res
        assert 'cny_amount' in overview_dict_res
        assert 'cny_change_extent' in overview_dict_res
        assert 'cny_market_value' in overview_dict_res
        assert 'highest_price' in overview_dict_res
        assert 'listed_exchange_count' in overview_dict_res
        assert 'lowest_price' in overview_dict_res
        assert 'project_name' in overview_dict_res
        assert 'usd_amount' in overview_dict_res
        assert 'usd_change_extent' in overview_dict_res
        assert 'usd_market_value' in overview_dict_res
        assert 'volume' in overview_dict_res

        # 查看主平台首页行情信息展示
        quota_list = main_quota_api.quotations_get()
        quota_res = [each for each in quota_list if each['marketId'] == market_id]
        print('主平台首页行情信息展示:', quota_res)
        quota_res_obj = quota_res[0]
        # assert quota_res[0]['latestPrice'] == price
        assert 'tradingAreaId' in quota_res_obj
        assert 'exchangeId' in quota_res_obj
        assert 'exchangeName' in quota_res_obj
        assert 'marketId' in quota_res_obj
        assert 'buyerCoinId' in quota_res_obj
        assert 'sellerCoin' in quota_res_obj
        assert 'sellerCoinLogoUrl' in quota_res_obj
        assert 'sellerCoinId' in quota_res_obj
        assert 'buyerCoin' in quota_res_obj
        assert 'latestPrice' in quota_res_obj
        assert 'cnyLatestPrice' in quota_res_obj
        assert 'volume' in quota_res_obj
        assert 'amount' in quota_res_obj
        assert 'changeExtent' in quota_res_obj
        assert 'changePct' in quota_res_obj

        # 查看主平台web交易所收藏，展示交易所信息
        exchange_res = main_quota_api.quotation_exchange_market_get(exchange_ids=exchange_ids)
        exchange_res_obj = exchange_res[0]['marketOverview'][0]
        print('主平台交易所信息:', exchange_res)
        assert 'tradingAreaId' in exchange_res_obj
        assert 'exchangeId' in exchange_res_obj
        assert 'exchangeName' in exchange_res_obj
        assert 'marketId' in exchange_res_obj
        assert 'buyerCoinId' in exchange_res_obj
        assert 'sellerCoin' in exchange_res_obj
        assert 'sellerCoinLogoUrl' in exchange_res_obj
        assert 'sellerCoinId' in exchange_res_obj
        assert 'buyerCoin' in exchange_res_obj
        assert 'latestPrice' in exchange_res_obj
        assert 'cnyLatestPrice' in exchange_res_obj
        assert 'volume' in exchange_res_obj
        assert 'amount' in exchange_res_obj
        assert 'changeExtent' in exchange_res_obj
        assert 'changePct' in exchange_res_obj

        # 获取主平台k线数据
        k_data_list = main_quota_api.quotations_historical_data_get(symbol=symbol, period='1d')
        k_data = k_data_list[0]
        print('主平台k线数据:', k_data_list)
        assert 'openPrice' in k_data
        assert 'closePrice' in k_data
        assert 'highestPrice' in k_data
        assert 'lowestPrice' in k_data
        assert 'volume' in k_data
        assert 'time' in k_data

        # 根据交易所id获取行情信息
        exchange_rec = main_quota_api.quotations_exchange_get(exchange_ids=exchange_ids)
        exchange_rec_data = exchange_rec[0]
        print('主平台根据交易所id获取行情信息:', exchange_rec)
        assert 'id' in exchange_rec_data
        assert 'logoUrl' in exchange_rec_data
        assert 'name' in exchange_rec_data
        assert 'usdAmount' in exchange_rec_data
        assert 'tradingPairCount' in exchange_rec_data

        # 获取项目行情信息
        project_res = main_quota_api.quotations_project_get(project_ids=sell_coin_id)
        project_res_data = project_res[0]
        print('主平台项目id行情信息:', project_res)
        assert 'id' in project_res_data
        assert 'coinId' in project_res_data
        assert 'fullName' in project_res_data
        assert 'shortName' in project_res_data
        assert 'coinLogo' in project_res_data
        assert 'volume' in project_res_data
        assert 'listedExchange' in project_res_data
        assert 'issuedVolume' in project_res_data

        # 查看项目方行情
        # 单一币种在各交易所的行情概要
        venture_id_overview_res = venture_quota_api.quotation_id_overview_get(id=sell_coin_id)
        venture_project_dict_res = venture_id_overview_res.to_dict()
        print('项目方单一币种在各交易所的行情概要:', venture_id_overview_res)
        assert 'avg_cny_price' in venture_project_dict_res
        assert 'avg_usdprice' in venture_project_dict_res
        assert 'change_pct' in venture_project_dict_res
        assert 'cny_amount' in venture_project_dict_res
        assert 'cny_change_extent' in venture_project_dict_res
        assert 'cny_market_value' in venture_project_dict_res
        assert 'highest_price' in venture_project_dict_res
        assert 'listed_exchange_count' in venture_project_dict_res
        assert 'lowest_price' in venture_project_dict_res
        assert 'project_name' in venture_project_dict_res
        assert 'usd_amount' in venture_project_dict_res
        assert 'usd_change_extent' in venture_project_dict_res
        assert 'usd_market_value' in venture_project_dict_res
        assert 'volume' in venture_project_dict_res

        # 获取市场的交易行情列表
        body = {
            'marketIds': market_id,
            'timeScope': '24d'
        }
        venture_project_res = venture_quota_api.get_project_market_trade_list(body)
        print('项目方市场交易行情列表:', venture_project_res)
        venture_project_obj = venture_project_res.items[0].to_dict()
        assert 'change_pct' in venture_project_obj
        assert 'latest_price' in venture_project_obj
        assert 'price_trend' in venture_project_obj
        assert 'volume' in venture_project_obj

        # 获取历史k线数据
        venture_kdata_payload = TenantGetHistoricalDataRequest()
        venture_kdata_payload.coin_id = sell_coin_id
        venture_kdata_payload.scope = '1w'
        venture_kdata = venture_quota_api.quotation_historical_data_post(venture_kdata_payload)
        venture_dict_kdata = venture_kdata[0]
        print('项目方历史k线数据:', venture_kdata)
        assert 'highestPrice' in venture_dict_kdata
        assert 'openPrice' in venture_dict_kdata
        assert 'lowestPrice' in venture_dict_kdata
        assert 'closePrice' in venture_dict_kdata
        assert 'volume' in venture_dict_kdata
        assert 'time' in venture_dict_kdata

        # 单一币种在单一交易所所有币对的行情统计
        venture_sell_coin_res = venture_quota_api.quotation_coins_id_get(id=sell_coin_id)
        print('项目方单一币种在单一交易所所有币对的行情统计:', venture_sell_coin_res)
        venture_sell_coin_dictres = venture_sell_coin_res[0]
        assert 'exchangeName' in venture_sell_coin_dictres
        assert 'volumePct' in venture_sell_coin_dictres

        # 查看租户平台行情
        # 查看租户平台手续费列表
        fee_history_res = tenant_exchange_api.exchange_fee_history_get()
        print('租户手续费列表', fee_history_res.items)

        # 单一币种在各交易所的行情概要
        tenant_overview_res = tenant_quota_api.quotation_id_overview_get(id=sell_coin_id)
        tenant_overview_dict_res = tenant_overview_res.to_dict()
        print('租户平台单一币种在各交易所的行情概要:', tenant_overview_res)
        assert 'avg_cny_price' in tenant_overview_dict_res
        assert 'avg_usdprice' in tenant_overview_dict_res
        assert 'change_pct' in tenant_overview_dict_res
        assert 'cny_amount' in tenant_overview_dict_res
        assert 'cny_change_extent' in tenant_overview_dict_res
        assert 'cny_market_value' in tenant_overview_dict_res
        assert 'highest_price' in tenant_overview_dict_res
        assert 'listed_exchange_count' in tenant_overview_dict_res
        assert 'lowest_price' in tenant_overview_dict_res
        assert 'project_name' in tenant_overview_dict_res
        assert 'usd_amount' in tenant_overview_dict_res
        assert 'usd_change_extent' in tenant_overview_dict_res
        assert 'usd_market_value' in tenant_overview_dict_res
        assert 'volume' in tenant_overview_dict_res

        # 获取租户平台k线数据
        tenant_kdata_payload = TenantGetHistoricalDataRequest()
        tenant_kdata_payload.coin_id = sell_coin_id
        tenant_kdata_payload.scope = '1w'
        coin_summary_list = tenant_quota_api.quotation_historical_data_post(tenant_kdata_payload)
        coin_summary_res = coin_summary_list[0]
        print('租户平台k线数据:', coin_summary_list)
        assert 'highestPrice' in coin_summary_res
        assert 'openPrice' in coin_summary_res
        assert 'lowestPrice' in coin_summary_res
        assert 'closePrice' in coin_summary_res
        assert 'volume' in coin_summary_res
        assert 'time' in coin_summary_res

        # 单一币种行情统计
        coin_count_list = tenant_quota_api.quotation_coins_id_get(sell_coin_id)
        coin_count_res = coin_count_list[0]
        print('租户平台单一币种在单一交易所所有币对的行情统计:', coin_count_list)
        assert 'exchangeName' in coin_count_res
        assert 'volumePct' in coin_count_res

        # 获取历史k线数据
        tenant_dashborad_payload = GetDashboardHistoricalDataRequest()
        tenant_dashborad_payload.trading_area_id = trading_area_id
        tenant_dashborad_payload.scope = '1w'
        tenant_dashaboard_kdata = tenant_dashboard_api.dashboard_quotation_historical_data_post(
            tenant_dashborad_payload)
        dashboard_dict_kdata = tenant_dashaboard_kdata.to_dict()['items'][0]
        print('dashboard历史K线数据:', tenant_dashaboard_kdata)
        assert 'time' in dashboard_dict_kdata
        assert 'volume' in dashboard_dict_kdata

        # 获取获取行情列表
        dashboard_summary_list = tenant_dashboard_api.dashboard_quotations_summary_get(1, 10)
        dashboard_summary_dict_res = dashboard_summary_list[0]
        dashboard_summary_pricetrend = dashboard_summary_dict_res['priceTrend']
        dashboard_summary_pricetrand_items = dashboard_summary_pricetrend['items'][0]
        print('dashborad行情列表:', dashboard_summary_list)
        assert 'tradingAreaId' in dashboard_summary_dict_res
        assert 'buyerCoin' in dashboard_summary_dict_res
        assert 'latestPrice' in dashboard_summary_dict_res
        assert 'volume' in dashboard_summary_dict_res
        assert 'priceTrend' in dashboard_summary_dict_res
        assert 'coinPair' in dashboard_summary_pricetrend
        assert 'tradingAreaId' in dashboard_summary_pricetrend
        assert 'items' in dashboard_summary_pricetrend
        assert 'volume' in dashboard_summary_pricetrand_items
        assert 'time' in dashboard_summary_pricetrand_items

        # 获取dashboard当日统计数
        dashboard_data = tenant_dashboard_api.dashboard_daily_statistics_get()
        dashboard_dict_data = dashboard_data.to_dict()
        dash_today_res = dashboard_dict_data['today']
        dash_yesterday_res = dashboard_dict_data['yesterday']
        print('dashborad当日统计数:', dashboard_data)
        assert 'day' in dashboard_dict_data
        assert 'today' in dashboard_dict_data
        assert 'yesterday' in dashboard_dict_data
        assert 'activity_users' in dash_today_res
        assert 'browse_users' in dash_today_res
        assert 'orders' in dash_today_res
        assert 'trade_number' in dash_today_res
        assert 'activity_users' in dash_today_res
        assert 'browse_users' in dash_yesterday_res
        assert 'browse_users' in dash_yesterday_res
        assert 'orders' in dash_yesterday_res
        assert 'trade_number' in dash_yesterday_res




