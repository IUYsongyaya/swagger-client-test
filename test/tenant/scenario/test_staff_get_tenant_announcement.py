# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-22

# - 前台交易所新建公告成功
# - (后台）获取所有交易所公告列表
# - 交易所公告详情


import pytest
from test.tenant.tenant import Tenant
from test.tenant.staff import Staff
from test.tenant.scenario.test_exchange_announcement_create import TEST_EXCHANGE_ANNOUNCEMENT
from test.tenant.id_settings import *


@pytest.fixture(scope="session")
def setup(request):
    _staff = Staff(CONFIG.STAFF_INDEX)
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    _exchange = _tenant.get_exchange()
    for ann in _tenant.list_announcements():
        _tenant.delete_announcement(ann.id)
        
    _tenant.post_announcement(**TEST_EXCHANGE_ANNOUNCEMENT)
    
    def finalize():
        for ann in _tenant.list_announcements():
            _tenant.delete_announcement(ann.id)

    request.addfinalizer(finalize)
    return _staff, _tenant, _exchange


def test(setup):
    _staff, _tenant, _exchange = setup
    assert _exchange.exchange_id, "需要先创建一个交易所"
    
    print("all exchanges ann: ", _staff.list_announcements_all_exchanges())
    ann = _staff.query_unique_announcement_all_exchanges(filter=dict(
        title=TEST_EXCHANGE_ANNOUNCEMENT["title"]
    ))
    assert ann, "Post announcement failed !"
    
    announcement = _staff.get_announcement(announcement_id=ann.id)
    assert announcement
    assert announcement.title == TEST_EXCHANGE_ANNOUNCEMENT["title"]
