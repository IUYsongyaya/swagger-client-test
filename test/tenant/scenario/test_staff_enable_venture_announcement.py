# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-22


# - 获取指定公告列表
# - 根据公告 title 定位 announcement_id
# - 根据 id 获取公告详情
# - 禁用公告
# - 获取公告详情，确认状态修改成功
# - 启用公告
# - 获取公告详情，确认状态修改成功

import pytest
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.main import Main
from test.tenant.scenario.test_project_announcement_create import TEST_PROJECT_ANNOUNCEMENT
from test.tenant.id_settings import *


@pytest.fixture(scope="session")
def setup(request):
    _staff = Staff(CONFIG.STAFF_INDEX)
    _venture = Venture(CONFIG.VENTURE_INDEX)
    _project = _venture.get_project(CONFIG.PROJECT_INDEX)
    _main = Main(CONFIG.MAIN_INDEX)
    assert _project.project_id, "需要先创建一个项目"
    for ann in _venture.list_announcements(project_id=_project.project_id):
        _venture.delete_announcement(ann.id)

    _venture.post_announcement(**TEST_PROJECT_ANNOUNCEMENT, project_id=_project.project_id)
    
    def finalize():
        for ann in _venture.list_announcements(project_id=_project.project_id):
            _venture.delete_announcement(ann.id)

    request.addfinalizer(finalize)
    return _staff, _venture, _project, _main


def test(setup):
    _staff, _venture, _project, _main = setup
    
    # 根据 project_id 公告 title 定位 announcement_id
    anns = _staff.query_announcements_project(project_id=_project.project_id, filter=dict(
        title=TEST_PROJECT_ANNOUNCEMENT["title"]
    ))
    assert anns, "无法找到此项目的公告"
    announcement_id = anns[0].id
    
    # 禁用公告
    _staff.enable_announcement(announcement_id=announcement_id, status=False)
    
    # 获取公告详情，确认状态修改成功
    annoucement = _staff.get_announcement(announcement_id=announcement_id)
    assert annoucement, "公告详情获取失败"
    assert not annoucement.status, "公告禁用失败"
    
    # 启用公告
    _staff.enable_announcement(announcement_id=announcement_id, status=True)
    
    # 获取公告详情，确认状态修改成功
    annoucement = _staff.get_announcement(announcement_id=announcement_id)
    assert annoucement, "公告详情获取失败"
    assert annoucement.status, "公告启用失败"

    anns_list = _main.list_announcements_by_project_id(project_id=_project.project_id)
    assert anns_list
    
    assert _main.get_project_announcement(announcemen_id=announcement_id), "获取项目公告详情失败"

