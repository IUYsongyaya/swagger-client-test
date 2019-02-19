# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-20


# - 修改交易所公告
# - 获取交易所公告列表
# - 查看公告详情

import pytest
from test.tenant.id_settings import *
from test.tenant.tenant import Tenant
from test.tenant.scenario.test_exchange_announcement_create import TEST_EXCHANGE_ANNOUNCEMENT

TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED = dict(
    title="hello world",
    content="公告内容\n 回家吃饭，回家看看",
    language="zh_cn"
)


@pytest.fixture(scope="session")
def setup(request):
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    
    for ann in _tenant.list_announcements():
        _tenant.delete_announcement(ann.id)
    _tenant.post_announcement(**TEST_EXCHANGE_ANNOUNCEMENT)
    
    def finalize():
        for ann in _tenant.list_announcements():
            _tenant.delete_announcement(ann.id)
    
    request.addfinalizer(finalize)
    return _tenant


def test(setup):
    _tenant = setup
    
    # 查找公告 id by title
    ann = _tenant.query_unique_announcement(filter=dict(
        title=TEST_EXCHANGE_ANNOUNCEMENT["title"]
    ))
    assert ann
    
    # 修改公告内容
    _tenant.update_announcement(announcement_id=ann.id, **TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED)
    
    # 返读修改后公告内容对比确认修改结果是否成功
    an = _tenant.get_announcement(announcement_id=ann.id)
    
    assert an
    assert an.title == TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED['title']
    assert an.content == TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED['content']
    assert an.language == TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED['language']
