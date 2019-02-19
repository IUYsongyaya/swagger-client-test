
from common.utils import PlatformManager


class TestAccountInfo:
    def test_sample_get_account_info(self, otc_user):
        manager = PlatformManager("otc")
        account_api = manager.account_api
        otc_user([account_api])
        res = account_api.accounts_profile_get()
        print(res)
