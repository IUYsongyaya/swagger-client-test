# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-20

import pytest
from test.tenant.id_settings import *
from test.tenant.staff import Staff
from test.tenant.main import Main


@pytest.fixture(scope="session")
def setup():
    banner = dict(
        title="hello world",
        banner="今晚打老虎",
        platform="pc",
        position="homepage",
        language="zh_cn",
        order=0,
        status=True,
        url="http://firer_on_fire.com"
    )

    banner_modified = dict(
        title="go go go",
        banner="夜上海, 夜上海",
        platform="pc",
        position="homepage",
        language="zh_cn",
        order=0,
        status=True,
        url="http://firer_on_fire.com"
    )
    return Staff(CONFIG.STAFF_INDEX), Main(CONFIG.MAIN_INDEX), banner, banner_modified


def test_staff_banner(setup):
    _staff, _main, test_banner, test_banner_modified = setup

    banners = list()
    banner_list = _staff.list_banners()
    # print("banner_list:", banner_list)
    if banner_list:
        banners = _staff.query_banners(filter=dict(
            title=test_banner["title"],
        ))

    if not banners:
        _staff.add_banner(**test_banner)
        banners = _staff.query_banners(filter=dict(
            title=test_banner["title"],
        ))
        assert banners, "后台创建 banner 失败"
        details = _staff.get_banner(banner_id=banners[0].id)
        assert details, "后台查询banner details 失败"

    banner_list = _staff.list_banners()
    assert banner_list, "后台查询 banner 列表失败"
    print("staff query banners num===================>", len(banners))
    assert len(banners) > 0, "后台查询 banner 错误"
    print("banner id==========>", banners[0].id)
    _staff.update_banner(banners[0].id, **test_banner_modified)

    modified = _staff.get_banner(banner_id=banners[0].id)
    assert modified.title == test_banner_modified["title"], "更改 banner 失败"

    query_res = _main.query_banners(
        language=test_banner_modified["language"],
        platform=test_banner_modified["platform"],
        position=test_banner_modified["position"]
    )

    assert query_res, " 主平台获取后台 banner 失败"

    for ban in banner_list:
        _staff.delete_banner(ban.id)

    assert not _staff.list_banners(), "后台删除 banner 失败"
