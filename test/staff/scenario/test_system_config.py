#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: test_system_config.py
@time: 2018/12/17
"""
from datetime import datetime

from pytest import fixture

from common.account_sign import get_admin_token, set_login_status
from swagger_client.staff.api.system_management_api import SystemManagementApi


class TestSystemConfig:
    @fixture
    def admin_token(self):
        return get_admin_token()
    
    def test_normal_commission_config(self, admin_token):
        api = SystemManagementApi()
        set_login_status(api, admin_token)
        # 提交佣金设置
        # api.system_commission_post(body={
        #                                   "commissionRate": "string",
        #                                   "startAt": datetime.utcnow(),
        #                                   "endAt": datetime.utcnow(),
        #                                   "ageDays": 100
        #                                 })
        #
        
        # res = api.system_commission_get(page=1)
        # print(res)
        
        # # 获取系统配置
        # api.system_system_config_get()
        # # 修改系统配置
        # api.system_system_config_id_put(
        #     id="1", body={
        #                   "configValue": 123.123
        #                 })
        # # 获取系统配置
        # res = api.system_system_config_get()
        # print(res)

        # 获取审核失败原因
        api.system_failure_reasons_get()
        # 新增审核失败原因
        api.system_failure_reasons_post(
            body={
                  "failureReason": "_failure_reason",
                  "type": "PERSONAL_AUTHENTICATE"
                  })
        # 获取审核失败原因
        res = api.system_failure_reasons_get()
        print(res)
        
        # 获取提币审核失败原因
        res = api.system_failure_reasons_withdraw_get()
        # 根据类型获取失败原因
        res = api.system_failure_reasons_type_get(type="PERSONAL_AUTHENTICATE")
        print(res)
        
        # # 获取区分列表
        # res = api.system_partition_get()
        # # 获取交易币对配置列表
        # res = api.system_trading_pair_get(partition_id=1)
        # print(res)
