# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-8


class TokenManager:
    
    def __init__(self, token):
        assert token, "Token must not be null"
        self._token = token
        super().__init__()
        
    def auth_headers(self, apis):
        # print("[ %s ]  token:" % type(self).__name__, self._token)
        for key, api in vars(apis).items():
            if key.startswith("api_"):
                # print("%s set token:%s" % (api.__class__, self._token))
                api.api_client.set_default_header("Authorization", "Bearer " + self._token)

    def __call__(self, *args, **kwargs):
        return self._token

    @property
    def token(self):
        return self._token