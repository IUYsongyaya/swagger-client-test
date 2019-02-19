#!/usr/bin/env python3
# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-6
import os
import sys
import time
import requests


BACK_DOOR_VERIFY_CODE = "666666"

ENV_DIST = os.environ
HOST_DEFAULT = dict(
    main="http://crush-main.c58c7e25a004943cdad05a1bf31f354b7.cn-shenzhen.alicontainer.com",
    staff="http://crush-staff.c58c7e25a004943cdad05a1bf31f354b7.cn-shenzhen.alicontainer.com",
    tenant="http://crush-tenant.c58c7e25a004943cdad05a1bf31f354b7.cn-shenzhen.alicontainer.com",
    venture="http://crush-venture.c58c7e25a004943cdad05a1bf31f354b7.cn-shenzhen.alicontainer.com"
)


def HOST(platform):
    name = f"crush_{platform}"
    return ENV_DIST.get(name, HOST_DEFAULT.get(platform))


class Account:
    def __init__(self, account, email, password):
        self.account = account
        self.email = email
        self.password = password
        self.bearer = ""


ACCOUNTS = dict(
    main=Account(account="main", email="", password="Wanshare123"),
    staff=Account(account="python", email="python", password="12345678"),
    tenant=Account(account="tenant", email="", password="Wanshare123"),
    venture=Account(account="venture", email="", password="Wanshare123")
)


verification_code = "666666"
nationalityCode = "CN"


def get_new_email(owner):
    assert owner
    now = int(time.time())
    return f"{now}{owner}@qq.com"


def register(platform, email, password):
    assert platform
    path = "/accounts/register"
    payload = {
        "nationalityCode": nationalityCode,
        "email": email,
        "password": password,
        "promotionCode": "",
        "verificationCode": verification_code,
        "challenge": "87a2661cb8458e5cee1a5741c13eb218k7",
        "seccode": "string",
        "validate": "string"
    }
    return requests.post(f"{HOST(platform)}{path}", json=payload)


def login(platform, account, password):
    assert platform
    path = "/accounts/login"
    payload = {
        "account": account,
        "password": password,
        "challenge": "",
        "seccode": "",
        "validate": ""
    }
    return requests.post(f"{HOST(platform)}{path}", json=payload)


def verify_login(platform, account, password, base):
    path = "/accounts/verifyLoginOrPassword"
    payload = {
        "challenge": str(),
        "seccode": "str()",
        "validate": "true",
        "account": account,
        "token": base,
        "password": password,
        "code": BACK_DOOR_VERIFY_CODE,
        "type": "login"
    }
    return requests.post(f"{HOST(platform)}{path}", json=payload)


def staff_login(account, password):
    platform = "staff"
    login_path = "/login"
    very_path = "/accounts/verify"
    payload = {
        "account": account,
        "password": password
    }
    lr = requests.post(f"{HOST(platform)}{login_path}", json=payload)
    
    if lr.status_code == 200:
        payload = {
            "challenge": "048ebbe51f829995db76ac4b81546403",
            "seccode": "string",
            "validate": "true",
            "account": "number:" + lr.json()["phone"],
            "code": "666666",
            "baseToken": lr.json()["token"]
        }
        vr = requests.post(f"{HOST(platform)}{very_path}", json=payload)
        if vr.status_code == 200:
            ACCOUNTS[platform].bearer = vr.json()["token"]
            print("verify bearer ==>", vr.json()["token"])
            return ACCOUNTS[platform].bearer
        else:
            print("staff verify failed")
            vr.raise_for_status()
            sys.exit(1)
    else:
        print("staff login failed")
        sys.exit(1)
        

def account_info(platform):
    path = "/accounts/account-info"
    headers = {"Authorization": f"Bearer {ACCOUNTS[platform].bearer}"}
    return requests.get(f"{HOST(platform)}{path}", headers=headers)


def staffs_info():
    platform = "staff"
    path = "/staffs/info"
    print("staffs info bearer ==>", ACCOUNTS[platform].bearer)
    headers = {"Authorization": f"Bearer {ACCOUNTS[platform].bearer}"}
    return requests.get(f"{HOST(platform)}{path}", headers=headers)


platforms_except_staff = HOST_DEFAULT.copy()
del platforms_except_staff["staff"]

for key in platforms_except_staff:
    # staff no register test
    ACCOUNTS[key].email = get_new_email(key)
    rsp = register(key, ACCOUNTS[key].email, ACCOUNTS[key].password)
    if rsp.status_code == 200:
        print(f"{key} register success")
    else:
        print(f"{key} register failed")
        rsp.raise_for_status()
        sys.exit(1)

for key in platforms_except_staff:
    lr = login(key, f"mailto:{ACCOUNTS[key].email}", ACCOUNTS[key].password)
    
    if lr.status_code == 401:
        print(f"{key} login success")
        base_token = lr.json()["baseToken"]
        print("base_token:", base_token)
        vr = verify_login(key, f"mailto:{ACCOUNTS[key].email}", ACCOUNTS[key].password, base_token)
        if vr.status_code == 200:
            print(f"{key} verify success")
            ACCOUNTS[key].bearer = vr.json()["token"]
        else:
            print(f"{key} verify failed")
            vr.raise_for_status()
            sys.exit(1)
    else:
        print(f"{key} login failed")
        lr.raise_for_status()
        sys.exit(1)


for key in platforms_except_staff:
    rsp = account_info(key)
    if rsp.status_code == 200:
        print(f"{key} get account info success")
        print(rsp.json())
    else:
        print(f"{key} account info failed")
        sys.exit(1)

staff_login(account=ACCOUNTS["staff"].account, password=ACCOUNTS["staff"].password)
rsp = staffs_info()
if rsp.status_code == 200:
    print("get staffs info success")
    print(rsp.json())
else:
    print("get staffs info failed")
    rsp.raise_for_status()
    sys.exit(1)
