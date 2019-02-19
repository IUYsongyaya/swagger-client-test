# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-18

# - 获取项目方公告列表
# - 发送项目方公告
# - 发送项目方公告
# - 查找公告 id by title
# - 查看公告详情

import pytest
from test.tenant.venture import Venture
from test.tenant.id_settings import *

from test.tenant.scenario.test_project_announcement_create import TEST_PROJECT_ANNOUNCEMENT


@pytest.fixture(scope="session")
def setup():
    _venture = Venture(CONFIG.TENANT_INDEX)
    _project = _venture.get_project(CONFIG.PROJECT_INDEX)
    for ann in _venture.list_announcements(project_id=_project.project_id):
        _venture.delete_announcement(announcement_id=ann.id)
    _venture.post_announcement(project_id=_project.project_id, **TEST_PROJECT_ANNOUNCEMENT)
    return _venture, _project


class TestScenario:
    
    def test(self, setup):
        _venture, _project = setup
        assert _project.project_id, "project id 不能为空"
        
        ann = _venture.query_unique_announcement(project_id=_project.project_id, filter=dict(
            title=TEST_PROJECT_ANNOUNCEMENT["title"]
        ))
        assert ann, "Announce is not exists"
        
        _venture.delete_announcement(announcement_id=ann.id)
        
        # 获取项目方公告列表
        announcement_list = _venture.list_announcements(project_id=_project.project_id)
        assert not announcement_list, "公告列表不为空"
