# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-20

# - 获取交易所公告列表
# - 发送交易所公告
# - 获取交易所公告列表
# - 查找公告 id by title
# - 查看公告详情

import pytest
from test.tenant.tenant import Tenant
from test.tenant.id_settings import *


TEST_EXCHANGE_ANNOUNCEMENT = dict(
    title="exchange title",
    content="公告内容\n 今晚不回家，今晚打老虎",
    language="zh_cn"
)


@pytest.fixture(scope="session")
def setup(request):
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    
    for ann in _tenant.list_announcements():
        _tenant.delete_announcement(ann.id)
        
    def finalize():
        for ann in _tenant.list_announcements():
            _tenant.delete_announcement(ann.id)
            
    request.addfinalizer(finalize)
    return _tenant


def test(setup):
    _tenant = setup
    
    # 发送交易所公告
    _tenant.post_announcement(**TEST_EXCHANGE_ANNOUNCEMENT)

    # 查找公告 id by title
    ann = _tenant.query_unique_announcement(filter=dict(
        title= TEST_EXCHANGE_ANNOUNCEMENT["title"]
    ))
    assert ann

    # 查看公告详情
    an = _tenant.get_announcement(announcement_id=ann.id)
    assert an, "查看公告详情失败"



