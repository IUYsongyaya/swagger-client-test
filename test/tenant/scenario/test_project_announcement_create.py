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
from test.tenant.main import Main
from test.tenant.id_settings import *

TEST_PROJECT_ANNOUNCEMENT = dict(
    title="上海不咋的",
    content="公告内容\n 夜上海，夜上海，你是一个不夜城!",
    language="zh_cn"
)


@pytest.fixture(scope="session")
def setup():
    _venture = Venture(CONFIG.TENANT_INDEX)
    _project = _venture.get_project(CONFIG.PROJECT_INDEX)
    _main = Main(CONFIG.MAIN_INDEX)
    return _venture, _project, _main


class TestScenario:
    
    def test(self, setup):
        _venture, _project, _main = setup
        assert _project.project_id, "project id 不能为空"
        # 获取项目方公告列表
        
        for ann in _venture.list_announcements(project_id=_project.project_id):
            _venture.delete_announcement(announcement_id=ann.id)
        
        announcement_list = _venture.list_announcements(project_id=_project.project_id)
        assert not announcement_list, "公告列表不为空"
        
        # 发送项目方公告
        _venture.post_announcement(project_id=_project.project_id, **TEST_PROJECT_ANNOUNCEMENT)
        
        print("project ann list", _venture.list_announcements(project_id=_project.project_id))
        # 查找公告 id by title
        ann = _venture.query_unique_announcement(project_id=_project.project_id, filter=dict(
            title=TEST_PROJECT_ANNOUNCEMENT["title"],
            language=TEST_PROJECT_ANNOUNCEMENT["language"]
        ))
        assert ann, "query unique announcement failed!"
        
        # 查看公告详情
        an = _venture.get_announcement(announcement_id=ann.id)
        
        assert an, "查看公告详情失败"
        assert an.title == TEST_PROJECT_ANNOUNCEMENT["title"]
        assert an.content == TEST_PROJECT_ANNOUNCEMENT['content']
        assert an.language == TEST_PROJECT_ANNOUNCEMENT['language']
        assert ann.id, "announcement id is null"
        newest_ann = _main.get_newest_announcement(str(_project.project_id), "project")
        assert newest_ann, "main get newest announcement failed"
