
from common.utils import PlatformManager

class TestAccountInfo:
    def test_sample_get_account_info(self, special_login):
        manager = PlatformManager("main")
        account_api = manager.account_api
        special_login([account_api])
        res = account_api.accounts_account_info_get()
        print(res)
