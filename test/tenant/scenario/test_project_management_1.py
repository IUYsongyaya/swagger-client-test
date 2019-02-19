# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-12


#
# 创建新项目 - 项目方获取项目申请列表 - 获取项目列表和 project_id - 根据 project_id 获取项目详情
#

import pytest
from unittest.mock import patch
from swagger_client.tenant.api.contacts_api import ContactsApi  # noqa: E501
from swagger_client.tenant.api.exchange_management_api import ExchangeManagementApi
from swagger_client.venture.api.project_api import ProjectApi
from swagger_client.venture.api.project_management_api import ProjectManagementApi

from swagger_client.venture.models.application_request import ApplicationRequest
from test.tenant.scenario.data.exchange_application_data import TEST_EXCHANGE
from test.tenant.scenario.data.project_application_data import TEST_PROJECT

api_contacts = ContactsApi()
api_projects = ProjectApi()
api_exchange_management = ExchangeManagementApi()
api_project_management = ProjectManagementApi()


class Empty:
    def __init__(self):
        self.empty = None


class DictObject:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


empty_obj = Empty()


def pytest_namespace():
    return dict(
        project_id="",
        exchange_id="",
        application_id="",
        contact_id="",
        applying_projects_list=[])


application_result = dict.copy(TEST_EXCHANGE)
application_result.update(dict(status="done", id="test_application_id"))
application_result = DictObject(**application_result)

project_info = dict.copy(TEST_PROJECT)
project_info.update(dict(project_id="test_project_id"))
project_info = DictObject(**project_info)


project_detail = dict(project_info={})
project_detail = DictObject(**project_detail)

info = dict.copy(TEST_PROJECT)
info.update(id="test_project_id")
info = DictObject(**info)
project_detail.project_info = info


class TestScenario:

    # 创建项目
    # @patch.object(empty_obj, "empty")
    @patch.object(
        api_projects,
        "applications_post",
        return_value=DictObject(id="test_application_id"))
    @pytest.mark.dependency()
    def test_applications_post(self, mocking):
        project_application = ApplicationRequest(**TEST_PROJECT)
        result = api_projects.applications_post(body=project_application)
        assert result.id
        pytest.application_id = result.id

    # 项目方获取项目申请列表
    # @patch.object(empty_obj, "empty")
    @patch.object(
        api_projects,
        "applications_get",
        return_value=DictObject(items=[application_result]))
    @pytest.mark.dependency("test_applications_post")
    def test_applications_get(self, mocking):
        rsp = api_projects.applications_get(page=1)
        assert len(rsp.items)
        applying_list = rsp.items
        for applying in applying_list:
            if applying.id == pytest.application_id:
                assert applying.status == "done"

    # 获取项目列表
    # @patch.object(empty_obj, "empty")
    @patch.object(
        api_projects,
        "projects_get",
        return_value=DictObject(items=[project_info]))
    @pytest.mark.dependency("test_applications_get")
    def test_projects_get(self, mocking):
        rsp = api_projects.projects_get(page=1)
        assert len(rsp.items)
        project_list = rsp.items
        for project in project_list:
            if project.project_name == project_info.project_name:
                pytest.project_id = project.project_id

    # 获取项目详情
    # @patch.object(empty_obj, "empty")
    @patch.object(
        api_projects,
        "projects_id_get",
        return_value=project_detail)
    @pytest.mark.dependency("test_projects_get")
    def test_projects_id_get(self, mocking):
        detail = api_projects.projects_id_get(id=pytest.project_id)
        assert detail
        assert detail.project_info.id == pytest.project_id
