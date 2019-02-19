# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-22

# - 获取所有交易所公告列表
# - 根据公告 title 和exchange_id 定位 announcement_id
# - 根据 id 获取公告详情
# - 禁用公告
# - 获取公告详情，确认状态修改成功
# - 启用公告
# - 获取公告详情，确认状态修改成功

import pytest
from test.tenant.tenant import Tenant
from test.tenant.staff import Staff
from test.tenant.main import Main
from test.tenant.scenario.test_exchange_announcement_create import TEST_EXCHANGE_ANNOUNCEMENT
from test.tenant.id_settings import *


@pytest.fixture(scope="session")
def setup(request):
    _staff = Staff(CONFIG.STAFF_INDEX)
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    _exchange = _tenant.get_exchange()
    _main = Main(CONFIG.MAIN_INDEX)
    for ann in _tenant.list_announcements():
        _tenant.delete_announcement(ann.id)

    _tenant.post_announcement(**TEST_EXCHANGE_ANNOUNCEMENT)

    def finalize():
        for ann in _tenant.list_announcements():
            _tenant.delete_announcement(ann.id)

    request.addfinalizer(finalize)
    return _staff, _tenant, _exchange, _main


class TestScenario:
    def test(self, setup):
        _staff, _tenant, _exchange, _main = setup
        
        assert _exchange.exchange_id, "需要先创建一个交易所"
        
        # 获取指定交易所公告列表
        announcements = _staff.list_announcements_all_exchanges()
        assert announcements, "所有交易所公告为空"
        
        # 根据公告 title 定位 announcement_id
        announcements = _staff.query_announcements_by_exchange_id(_exchange.exchange_id)
        assert announcements, "特定交易所的公告为空"
        
        annoucement = _staff.query_unique_announcement_by_exchange_id(_exchange.exchange_id)
        assert annoucement, "特定交易所公告为空"
        
        # 禁用公告
        _staff.enable_announcement(announcement_id=annoucement.id, status=False)
        
        # 获取公告详情，确认状态修改成功
        details = _staff.get_announcement(announcement_id=annoucement.id)
        assert details, "公告详情获取失败"
        assert not details.status, "公告禁用失败"

        # 启用公告
        _staff.enable_announcement(announcement_id=annoucement.id, status=True)

        # 获取公告详情，确认状态修改成功
        details = _staff.get_announcement(announcement_id=annoucement.id)
        assert details, "公告详情获取失败"
        assert details.status, "公告启用失败"
        
        anns_list = _main.list_announcements_by_exchange_id(exchange_id=_exchange.exchange_id)
        assert anns_list

        assert _main.get_exchange_announcement(announcemen_id=annoucement.id), "Get exchange announcement failed"
