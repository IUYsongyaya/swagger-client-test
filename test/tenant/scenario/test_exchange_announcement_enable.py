# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-20

# - 获取交易所公告列表
# - 查找公告 id by title
# - 禁用公告
# - 查看公告列表, 确认为已禁用
# - 启用公告
# - 查看公告列表, 确认为已启动

import pytest
from test.tenant.tenant import Tenant
from test.tenant.main import Main
from test.tenant.id_settings import *
from test.tenant.scenario.test_exchange_announcement_modify import TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED


@pytest.fixture(scope="session")
def setup(request):
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    _exchange = Tenant(CONFIG.TENANT_INDEX).get_exchange()
    _main = Main(CONFIG.MAIN_INDEX)

    for ann in _tenant.list_announcements():
        _tenant.delete_announcement(ann.id)

    _tenant.post_announcement(**TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED)

    def finalize():
        for ann in _tenant.list_announcements():
            _tenant.delete_announcement(ann.id)

    request.addfinalizer(finalize)
    return _tenant, _exchange, _main


def test(setup):
    _tenant, _exchange, _main = setup
    
    # 查找公告 id by title
    ann = _tenant.query_unique_announcement(filter=dict(
        title=TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED["title"]
    ))
    assert ann, "查找公告by title失败, 无此公告在列表中"

    _tenant.enable_announcement(announcement_id=ann.id, status=False)
    
    ann = _tenant.query_unique_announcement(filter=dict(
        title=TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED["title"]
    ))
    assert not ann.status, "disable announcement failed!"

    _tenant.enable_announcement(announcement_id=ann.id, status=True)

    ann = _tenant.query_unique_announcement(filter=dict(
        title=TEST_EXCHANGE_ANNOUNCEMENT_MODIFIED["title"]
    ))
    
    assert ann.status, "enable announcement failed!"
    
    newest_ann = _main.get_newest_announcement(str(_exchange.exchange_id), "exchange")
    assert newest_ann, "main get newest announcement failed"

