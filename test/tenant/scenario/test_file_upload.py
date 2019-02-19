# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-8

import pytest
from test.tenant.id_settings import *
from test.tenant.tenant import Tenant


@pytest.fixture(scope="session")
def setup():
    return Tenant(CONFIG.TENANT_INDEX)


class TestScenario:
    
    def test_photo_upload(self, setup):
        _tenant = setup
        key, url = _tenant.upload(red=255, width=1920, height=1080)
        assert key, "upload response key is null"
        assert url, "upload response url is null"
        
        url_ret = _tenant.get_file(key=key)
        assert url == url_ret

        url_ret = _tenant.get_zoom_file(key=key, zoom="1")
        assert url != url_ret
