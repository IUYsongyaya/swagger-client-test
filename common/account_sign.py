#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: account_sign.py
@time: 2018/11/09
"""
import time
import random
import string

from faker import Faker

from swagger_client.staff.api.staff_management_api import StaffManagementApi
from swagger_client.staff.api.account_management_api import AccountManagementApi
from swagger_client.sponsor.api.sponsor_api import SponsorApi
from swagger_client.sponsor.models.post_login_request import PostLoginRequest

from common.utils import random_get_country_ob
from common.utils import PlatformManager


EMAIL_PREFIX_MIN_LEN = 4
EMAIL_PREFIX_MAX_LEN = 10
PWD_MIN_LEN = 8
PWD_MAX_LEN = 12

# 后台高级账户
# ADMIN_ACCOUNT = "python"
ADMIN_ACCOUNT = "zhangxuyi"
ADMIN_PASSWORD = "19831116zxy"
# ADMIN_PASSWORD = "12345678"


def register_with_login(platform: str, with_login, api_list: list):
    """
    :param platform: 登录所调平台平台名称Enum("main", "tenant", "venture")
    :param with_login: fixture with_login 原封不动传进来
    :param api_list: 索要登录的接口
    :return: user:dict {"email": "", "password": "", "country": "", "token": ""}
    """
    user = random_user()
    manager = PlatformManager(platform)
    if platform == 'otc':
        manager.register(email=user["email"], password=user["password"],
                         nationality_code=user["country_abbreviation"],
                         nick_name=user["nick_name"])
    else:
        manager.register(email=user["email"], password=user["password"],
                         nationality_code=user["country_abbreviation"])

    token = with_login(platform, api_list, account=user["email"],
                       password=user["password"])
    user["token"] = token
    return user


def random_user():
    """
    通过faker产生一个随机账户
    :return: dict
    """
    faker = Faker("zh_CN")
    nick_name = faker.name() + faker.name()
    country = random_get_country_ob()
    now = int(round(time.time() * 1000))
    email = str(now) + '@qq.com'
    account = dict(nick_name=nick_name, email=email, password=faker.password(),
                   country=country.get("n"),
                   country_abbreviation=country.get("k"),
                   phone=faker.phone_number())
    return account


def set_login_status(api, token):
    api.api_client.set_default_header("Authorization",
                                      "Bearer " + token)


def rand_password():
    """
    产生一个随机的密码8-12位
    :return:
    """
    length = random.SystemRandom().randint(PWD_MIN_LEN, PWD_MAX_LEN)
    digits_num = random.SystemRandom().randint(1,
                                               PWD_MAX_LEN - PWD_MIN_LEN - 2)
    upper_char_num = random.SystemRandom().randint(1, length - digits_num - 1)
    lower_char_num = length - digits_num - upper_char_num
    password = ''.join(random.SystemRandom().choice(string.digits
                                                    ) for _ in range(
        digits_num))
    password += ''.join(random.SystemRandom().choice(
        string.ascii_uppercase) for _ in range(upper_char_num))
    password += ''.join(random.SystemRandom().choice(
        string.ascii_lowercase) for _ in range(lower_char_num))
    password = list(password)
    random.shuffle(password)
    return "".join(password)


def rand_email():
    """
    产生一个随机邮件
    :return:
    """
    email_postfix = ["@qq.com", "@gmail.com", "@iclound.com",
                     "@163.com", "@126.com"]
    email = random.choice(email_postfix)
    prefix_length = random.randint(EMAIL_PREFIX_MIN_LEN, EMAIL_PREFIX_MAX_LEN)
    email = ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits
    ) for _ in range(prefix_length)) + email
    return email


def get_admin_token():
    staff_api = StaffManagementApi()
    account_api = AccountManagementApi()
    staff_res = staff_api.login_post(
        body={
              "account": ADMIN_ACCOUNT,
              "password": ADMIN_PASSWORD
            }
    )
    phone = staff_res.phone
    base_token = staff_res.token
    account_api.accounts_send_verification_code_post(body={
          "uri": "number:" + phone,
          "type": "login"
        })
    verify_resp = account_api.accounts_verify_post(
        verify_info={"challenge": "challenge",
                     "validate": "validate",
                     "seccode": "seccode",
                     "account": "number:" + phone,
                     "code": "666666",
                     "baseToken": base_token})
    return verify_resp.token


def get_sponsor_token(account="", password="",
                      challenge="", sec_code="", validate="", email="",
                      api_list=list()):
    req_body = PostLoginRequest(account=account,
                                password=password,
                                challenge=challenge,
                                seccode=sec_code,
                                validate=validate)
    sponsor_api = SponsorApi()
    res = sponsor_api.sponsor_login_post(
        sponsor_login=req_body)
    verify_info = {
        "uri": "mailto:" + email,
        "baseToken": res.base_token,
        "code": "666666",
    }
    res = sponsor_api.sponsor_login_verify_post(
        post_login_verify_request=verify_info)
    token = res.token
    for api in api_list:
        set_login_status(api, token)
    return token
