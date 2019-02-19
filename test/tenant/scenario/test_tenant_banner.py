# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-20

import pytest
from test.tenant.id_settings import *
from test.tenant.tenant import Tenant
from test.tenant.main import Main


@pytest.fixture(scope="session")
def setup():
    banner = dict(
        title="hello world",
        banner="今晚打老虎",
        url="http://helloworld_rule_the_world/banner.jpg"
    )
    
    banner_modified = dict(
        title="go go go",
        banner="夜上海, 夜上海",
        url="http://go_go_go_never_stop/banner.jpg"
    )
    return Tenant(CONFIG.TENANT_INDEX), Main(CONFIG.MAIN_INDEX), banner, banner_modified


def test_tenant_banner(setup):
    _tenant, _main, test_banner, test_banner_modified = setup
    
    _exchange = _tenant.get_exchange()
    assert _exchange, "租户需要先创建一个交易所"
    banners = list()
    banner_list = _tenant.list_banners()
    print("banner_list:", banner_list)
    if banner_list:
        banners = _tenant.query_banners(filter=dict(
            title=test_banner["title"],
        ))
        
    if not banners:
        print("Go adding banner====================>")
        _tenant.add_banner(title=test_banner["title"], banner=test_banner["banner"], url=test_banner["url"])
        banners = _tenant.query_banners(filter=dict(
            title=test_banner["title"],
        ))
        assert banners, "租户创建 banner 失败"
        details = _tenant.get_banner(banner_id=banners[0].id)
        print("Adding result: ", details)
        assert details, "租户查询banner details 失败"

    banner_list = _tenant.list_banners()
    assert banner_list, "租户查询 banner 列表失败"
    print("banners ===================>", banners)
    assert len(banners) > 0, "租户查询 banner 错误"

    for banner in banner_list:
        _tenant.update_banner_status(banner.id, status=True)

        _tenant.update_banner(banner.id, **test_banner_modified)

        modified = _tenant.get_banner(banner_id=banner.id)
        assert modified.title == test_banner_modified["title"], "更改 banner 失败"

    print("==============>exchange_id:", _exchange.exchange_id)
    # query_res = _main.query_banners_by_exchange_id(exchange_id=_exchange.exchange_id, filter=test_banner_modified)
    query_res = _main.get_banners_by_exchagne_id(exchange_id=_exchange.exchange_id)
    assert query_res, " 主平台获取交易所 exchange_id:%s banner 失败" % _exchange.exchange_id

    for banner in _tenant.list_banners():
        print("banners before reset:", banner)
        _tenant.update_banner_status(banner.id, status=True)
        
    for banner in _tenant.list_banners():
        print("banners after reset:", banner)
        _tenant.reset_banner(banner_id=banner.id)
        
    banners = _tenant.query_banners(filter=dict(
        title=test_banner_modified["title"],
    ))

    for banner in banners:
        assert banner.status, "租户修改 banner 状态失败"
    
    for ban in _tenant.list_banners():
        _tenant.delete_banner(ban.id)

    assert not _tenant.list_banners(), "租户删除 banner 失败"
