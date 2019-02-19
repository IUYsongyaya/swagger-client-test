#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: venture_prepare.py
@time: 2018/12/09
"""
import json
import uuid

from faker import Faker
import requests

from common.certification_verify import individual_verify
from common.utils import (PlatformManager, get_random_id_number,
                          get_random_name)
from common.account_sign import get_admin_token, get_sponsor_token, random_user
from swagger_client.venture.api.project_api import ProjectApi
from swagger_client.venture.api.sponsors_managerment_api import SponsorsManagermentApi as SMApi
from swagger_client.staff.api.asset_management_api import AssetManagementApi
from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from swagger_client.sponsor.api.sponsors_project_api import SponsorsProjectApi


FAKE_WALLET_URL = "fakewallet:8000"
# FAKE_WALLET_URL = "http://172.19.8.52:8000"
JAVA_WALLET_API = "http://crush-wallet.c58c7e25a004943cdad05a1bf31f354b7.cn-shenzhen.alicontainer.com/wallet"


def set_login_status(api, token):
    api.api_client.set_default_header("Authorization",
                                      "Bearer " + token)


def register_wallet(coin_type):
    headers = {'content-type': 'application/json'}
    # api_url = "http://crush-wallet.crush-deploy.lan/api/wallet"
    api_url = JAVA_WALLET_API
    # url = "http://192.168.83.153:8000"
    url = FAKE_WALLET_URL
    payload = {
        "method": "addWallet",
        "params": {
            "address_ip": url,
            "withdraw_ip": url,
            "coin_type": coin_type},
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(api_url, data=json.dumps(payload),
                             headers=headers)
    return response


def recharge_notify(coin_type, confirmations, address, status=1, amount=100):
    headers = {'content-type': 'application/json'}
    # api_url = "http://crush-wallet.crush-deploy.lan/api/wallet"
    api_url = JAVA_WALLET_API
    success_status = status
    payload = {
        "method": "recharge",
        "params": {
            'address': address,
            'from_address': '{}_recharge_from_address'.format(coin_type),
            'amount': amount,
            'txid': uuid.uuid4().hex,
            'coin_type': coin_type,
            'destination_tag': "destination_tag",
            'confirmations': confirmations,
            'status': success_status
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(api_url, data=json.dumps(payload),
                             headers=headers)
    return response


def withdraw_notify(txid, status, confirmations):
    headers = {'content-type': 'application/json'}
    # api_url = "http://crush-wallet.crush-deploy.lan/api/wallet"
    api_url = JAVA_WALLET_API
    payload = {
        "method": 'confirmWithdraw',
        "params": {
            'txid': txid,
            'status': status,
            'confirmations': confirmations
        },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    return response.json()


def create_venture():
    faker = Faker()
    manager = PlatformManager("venture")
    user = random_user()
    manager.register(email=user.get("email"), password=user.get("password"),
                     promotion_code=None, verification_code="666666",
                     nationality_code=user.get("country_abbreviation"))
    token = manager.login(account=user.get("email"),
                          password=user.get("password"))
    # 个人实名认证
    individual_verify(platform="venture",
                      id_number=get_random_id_number(),
                      token=token)
    # 申请项目
    project_api = ProjectApi()
    set_login_status(project_api, token)
    project_name = get_random_name(2, 16)
    full_name = get_random_name(2, 12)
    short_name = get_random_name(2, 6)
    # project_name = "USDT"
    # short_name = "USDT"
    res = project_api.applications_post(body={
              "projectName": project_name,
              "description": "{}-project-description".format(project_name),
              "officialWebsite": "www.{}.com".format(project_name),
              "whitePaperKey": "{}-whitePaper".format(project_name),
              "areaCode": "+86",
              "projectPosterKey": faker.uri_page(),
              # "projectPosterUrl": faker.url(),
              "cellphone": "123456789",
              "telephone": "12345678910",
              "email": faker.email(),
              "fullName": "{}的全部名".format(full_name),
              "shortName": short_name,
              "issuePrice": "2.24545",
              "issuedVolume": "1000000",
              "circulationVolume": "1000000",
              "issuedDate": "2018-08-08",
              "coinLogoKey": faker.uri_page(),
              # "coinLogoUrl": faker.url(),
              "blockchainType": "public_chain",
              "dataLink": "{}-data-link".format(project_name),
              "blockBrowser": "{}-block-Browser".format(project_name)
            })
    project_apply_id = res.id
    
    # 创建保健方账号
    staff_api = SponsorsManagermentApi()
    staff_token = get_admin_token()
    set_login_status(staff_api, staff_token)
    sponsor = {"account": get_random_name(8, 20), "password": faker.password(),
               "name": get_random_name(2, 20), "email": faker.email(),
               "phone": faker.phone_number()}
    staff_api.staff_sponsors_post(post_sponsor=sponsor)
    
    # 项目方获取保健列表
    venture_api = SMApi()
    set_login_status(venture_api, token)
    res = venture_api.sponsors_get(page=1, name=sponsor.get("name"))
    item = res.items.pop()
    sponsor_id = item.id
    
    # 项目方设置保健方
    project_api.applications_id_set_sponsor_put(
        id=project_apply_id, sponsor_request={"sponsorId": sponsor_id})
    
    # 保健方登录
    # 保健项目
    sponsor_api = SponsorsProjectApi()
    get_sponsor_token(account=sponsor.get("account"),
                      password=sponsor.get("password"),
                      email=sponsor.get("email"), api_list=[sponsor_api])
    sponsor_api.projects_sponsor_put(put_project_sponsor_request={
                  "id": project_apply_id,
                  "status": 1,
                  "remark": "remark"
                }
                )
    
    # 获取币种列表
    asset_api = AssetManagementApi()
    set_login_status(asset_api, staff_token)
    res = asset_api.asset_mgmt_coins_get(coin_name=short_name)
    coin = res.items.pop()
    coin_id = coin.id
    
    # 项目初始化
    # staff_project_api = StaffProjectApi()
    # set_login_status(staff_project_api, staff_token)
    
    # staff_project_api.projects_coin_id_init_put(coin_id=coin_id,
    #                                             body={
    #                                                   "initFee": 111
    #                                                 })
    rc_confirmed_times = 2
    wc_confirmed_times = 2
    asset_api.asset_mgmt_coins_id_init_put(id=coin_id,
                                           body={"usdtPrice": "1",
                                                 "rcTimes": rc_confirmed_times,
                                                 "wcTimes": wc_confirmed_times,
                                                 "withdrawRate": "0.003",
                                                 "minWithdrawFee": "0.1",
                                                 "minWithdraw": "20",
                                                 "maxWithdraw": "1000",
                                                 "dayWithdrawTotal": "30000",
                                                 "minRecharge": "0.1",
                                                 "addressTagSwitch": True,
                                                 "addressType": short_name,
                                                 "addressUrl": "addressUrl",
                                                 "txidUrl": "fdfsfdstxidUrl"})
    
    # # 修改币种配置
    # asset_api.asset_mgmt_coins_id_put(
    #     id=coin.id, body={
    #               "rcTimes": 2,
    #               "wcTimes": 2,
    #               "withdrawRate": "0.003",
    #               "minWithdrawFee": "0.1",
    #               "minWithdraw": "20",
    #               "maxWithdraw": "1000",
    #               "dayWithdrawTotal": "30000",
    #               "minRecharge": "0.1",
    #               "addressTagSwitch": True,
    #               "addressType": short_name,
    #               "addressUrl": "addressUrl",
    #               "txidUrl": "fdfsfdstxidUrl"
    #             })
    register_wallet(short_name)
    return coin.id, coin.coin_id, short_name, rc_confirmed_times, wc_confirmed_times
    

# a = create_venture()
# print(a)
# a = register_wallet("UPCTA".upper())
# print(a.content)
# print(a, a.content)
# aa = recharge_notify("USDT", 30, "USDT_6966c1c7a8aa4e759553f01102d5c329", amount=200000)
# print(aa.content)

# admin_token = get_admin_token()
# asset_manage_api = AssetManagementApi()
# set_login_status(asset_manage_api, admin_token)
# asset_manage_api.asset_mgmt_coins_id_recharge_put(id="1", rechargeable=True)
# asset_manage_api.asset_mgmt_coins_id_withdraw_put(id="1", withdrawable=True)
