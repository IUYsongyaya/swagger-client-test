# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-19
import requests


class Faucet:
    def __init__(self, token, host):
        self._token = token
        self._host = host
    
    def free_charge(self, coin_id, amount):
        print("host: %s token: %s" % (self._host, self._token))
        rsp = requests.post(
            f"{self._host }/asset-test/asset-initialize/{coin_id}/{amount}",
            headers={"Authorization": f"Bearer {self._token}"}
        )
        if rsp.status_code != 200:
            rsp.raise_for_status()
