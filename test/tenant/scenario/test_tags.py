# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-20

import pytest
from test.tenant.staff import Staff
from test.tenant.tenant import Tenant
from test.tenant.id_settings import *


@pytest.fixture(scope="session")
def setup():
    return Staff(CONFIG.STAFF_INDEX), Tenant(CONFIG.TENANT_INDEX)


TEST_TAG = "reren_zxy"
TEST_TAG_MODIFIED = "renren_gogo"


class TestScenario:
    def test(self, setup):
        _staff, _tenant = setup
        
        ret = _staff.query_tags(filter=dict(name=TEST_TAG))
        if ret:
            _staff.delete_tag(tag_id=ret[0].id)
            
        ret = _staff.query_tags(filter=dict(name=TEST_TAG_MODIFIED))
        if ret:
            _staff.delete_tag(tag_id=ret[0].id)
            
        ret = _staff.query_tags(filter=dict(name=TEST_TAG))
        assert not ret, f"TAG:{TEST_TAG} 删除tag失败"

        _staff.create_tag(tag=TEST_TAG, other_language=[{"key": "英语", "value": "public_chain"}])
        
        ret = _staff.query_tags(filter=dict(name=TEST_TAG))
        assert ret, f"查询失败, <{TEST_TAG}> 不存在"
        assert len(ret) == 1, "查询结果异常, tag名字存在重复"
        
        tag = ret[0]
        _staff.update_tag(tag.id, tag_name=TEST_TAG_MODIFIED,  other_language=[{"key": "英语", "value": "public_chain"}])
        
        tag_ret = _staff.get_tag(tag_id=tag.id)
        assert tag_ret, f"获取 tag {tag.id} 失败"

        _exchange = _tenant.get_exchange()
        assert _exchange, "Need to create a exchange first"
