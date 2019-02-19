# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-20

# - 获取交易所公告列表
# - 查找公告 id by title
# - 删除公告
# - 查看公告列表, 确认已经删除

import pytest
from test.tenant.tenant import Tenant
from test.tenant.id_settings import *
from test.tenant.scenario.test_exchange_announcement_modify import TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED


@pytest.fixture(scope="session")
def setup(request):
    _tenant = Tenant(CONFIG.TENANT_INDEX)

    for ann in _tenant.list_announcements():
        _tenant.delete_announcement(ann.id)

    _tenant.post_announcement(**TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED)

    def finalize():
        for ann in _tenant.list_announcements():
            _tenant.delete_announcement(ann.id)

    request.addfinalizer(finalize)
    return _tenant


def test(setup):
    _tenant = setup
    
    # - 查找公告 id by title
    ann = _tenant.query_unique_announcement(filter=dict(
        title=TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED["title"]
    ))
    
    # - 删除公告
    _tenant.delete_announcement(announcement_id=ann.id)

    # - 查看公告列表, 确认已经删除
    ann = _tenant.query_unique_announcement(filter=dict(
        title=TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED["title"]
    ))
    assert not ann
