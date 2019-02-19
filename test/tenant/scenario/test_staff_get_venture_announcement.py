# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-22

# - 获取项目公告列表
# - 项目新建公告成功
# - (后台）获取项目公告列表
# - 根据 title 定位公告 id
# - 根据 id 获取项目公告详情


import pytest
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.scenario.test_project_announcement_create import TEST_PROJECT_ANNOUNCEMENT
from test.tenant.id_settings import *


@pytest.fixture(scope="session")
def setup(request):
    _staff = Staff(CONFIG.STAFF_INDEX)
    _venture = Venture(CONFIG.VENTURE_INDEX)
    _project = _venture.get_project(CONFIG.PROJECT_INDEX)
    assert _project.project_id, "需要先创建一个项目"
    for ann in _venture.list_announcements(project_id=_project.project_id):
        _venture.delete_announcement(ann.id)

    _venture.post_announcement(**TEST_PROJECT_ANNOUNCEMENT, project_id=_project.project_id)

    def finalize():
        for ann in _venture.list_announcements(project_id=_project.project_id):
            _venture.delete_announcement(ann.id)

    request.addfinalizer(finalize)
    return _staff, _venture, _project


def test(setup):
    _staff, _venture, _project = setup
    # - (后台）获取项目公告列表
    announcements = _staff.list_announcements_project(project_id=_project.project_id)
    assert announcements
    
    # - 根据 title 定位公告 id
    announcement_id = None
    for an in announcements:
        if an.title == TEST_PROJECT_ANNOUNCEMENT["title"]:
            announcement_id = an.id
    else:
        assert "无法找到项目方创建的公告"

    # - 获取项目公告详情
    announcement = _staff.get_announcement(announcement_id=announcement_id)
    assert announcement
    assert announcement.title == TEST_PROJECT_ANNOUNCEMENT["title"]
