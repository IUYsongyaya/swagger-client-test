# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-12


#
# 获取交易所卖买方币种列表 - 获取单一币种在单一交易所币对的行情统计
#

import pytest
import json
import swagger_client.tenant
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch
from swagger_client.tenant.api.contacts_api import ContactsApi  # noqa: E501
from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
from swagger_client.venture.api.project_api import ProjectApi
from swagger_client.venture.api.project_management_api import ProjectManagementApi
from swagger_client.tenant.rest import ApiException

from swagger_client.tenant.models.get_exchange_request import GetExchangeRequest
from swagger_client.venture.models.application_request import ApplicationRequest
# from conftest import verify, login, logout, register, BACK_DOOR_VERIFY_CODE, rand_password, rand_email, rand_phone, rand_indiv_cert
from test.tenant.scenario.data.exchange_application_data import TEST_EXCHANGE
from test.tenant.scenario.data.project_application_data import TEST_PROJECT


class DictObject:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


api_contacts = ContactsApi()
api_projects = ProjectApi()
api_exchange_management = ExchangeManagementApi()
api_project_management = ProjectManagementApi()


APPLICATION_GET_RESULT = dict.copy(TEST_EXCHANGE)
APPLICATION_GET_RESULT.update(dict(status="done", id="test_application_id"))


PROJECT_GET_RESULT = dict.copy(TEST_PROJECT)
PROJECT_GET_RESULT.update(dict(project_id="test_project_id"))


PROJECT_INFO_GET_RESULT = dict.copy(TEST_PROJECT)
PROJECT_INFO_GET_RESULT.update(dict(id="test_project_id"))
PROJECT_INFO_GET_RESULT = DictObject(**PROJECT_INFO_GET_RESULT)


class TestScenario:

    @patch.object(api_exchange_management, "exchange_post", return_value=None)
    def test_mock_usage(self, mock_exchange_post):
        api_exchange_management.exchange_post(body=None)
        mock_exchange_post.assert_called_with(body=None)
