#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: utils.py
@time: 2018/11/11
"""
import importlib
import json
import time
import pathlib
import random
import string

from faker import Faker


BACK_DOOR_VERIFY_CODE = "666666"


class PlatformManager:
    """
    封装接口中平台的差异性
    """
    def __init__(self, platform: str):
        """
        :param platform:平台名称Enum("main", "sponsor", "staff",
                                    "tenant", "venture", "otc")
        """
        self._platform = platform
        self._api_exception_template = ".{}.rest"
        self._login_request_template = ".{}.models.post_login_request"
        self._account_api_template = ".{}.api.account_api"
        self._verification_api_template = ".{}.api.verification_api"
        self._asset_api_template = ".{}.api.asset_management_api"
        self._register_request_template = ".{}.models.post_register_request"
        self._individual_request_template = (".{}.models.post_individual_"
                                             "certification_request")
        self._company_request_template = (".{}.models.post_enterprise_"
                                          "certification_request")
        self._bind_phone_request_template = (".{}.models.post_bind"
                                             "_phone_request")
        self._edit_phone_request_template = (".{}.models.post_edit"
                                             "_phone_request")
        self._bind_google_request_template = (".{}.models.post_bind_google"
                                              "_authenticator_request")
        self._open_google_request_template = (".{}.models.post_open_google"
                                              "_authenticator_request")
        self._open_phone_request_template = (".{}.models.post_open_phone"
                                             "_authenticator_request")
        self._close_google_request_template = (".{}.models.post_close_google"
                                               "_authenticator_request")
        self._close_phone_request_template = (".{}.models.post_close_phone"
                                              "_authenticator_request")
        self._init_google_request_template = (".{}.models.init_"
                                              "google_request")
        self._set_password_request_template = (".{}.models.post_set"
                                               "_password_request")
        self._rest_password_request_template = (".{}.models.post_reset"
                                                "_password_request")
        self._password_verify_request_template = (".{}.models.post_password"
                                                  "_validation_request")
        self._account_api = self.account_api_model()
        self._verify_api = self.verification_api_model()
        self._asset_api = self.asset_api_model()

    def _get_corresponding_model(self, template):
        model = importlib.import_module(template.format(self._platform),
                                        package="swagger_client")
        return model

    @property
    def register_request_model(self):
        return self._get_corresponding_model(self._register_request_template
                                             ).PostRegisterRequest

    @property
    def login_request_model(self):
        return self._get_corresponding_model(self._login_request_template
                                             ).PostLoginRequest

    @property
    def individual_request_model(self):
        return self._get_corresponding_model(
            self._individual_request_template
            ).PostIndividualCertificationRequest

    @property
    def company_request_model(self):
        return self._get_corresponding_model(
            self._company_request_template
        ).PostEnterpriseCertificationRequest

    @property
    def account_api_model(self):
        return self._get_corresponding_model(self._account_api_template
                                             ).AccountApi

    @property
    def verification_api_model(self):
        return self._get_corresponding_model(
            self._verification_api_template
        ).VerificationApi

    @property
    def asset_api_model(self):
        return self._get_corresponding_model(
            self._asset_api_template).AssetManagementApi

    @property
    def api_exception(self):
        return self._get_corresponding_model(self._api_exception_template
                                             ).ApiException

    @property
    def bind_google_request_model(self):
        return self._get_corresponding_model(
            self._bind_google_request_template
        ).PostBindGoogleAuthenticatorRequest

    @property
    def bind_phone_request_model(self):
        return self._get_corresponding_model(
            self._bind_phone_request_template).PostBindPhoneRequest

    @property
    def alter_phone_request_model(self):
        return self._get_corresponding_model(
            self._edit_phone_request_template).PostEditPhoneRequest

    @property
    def open_google_request_model(self):
        return self._get_corresponding_model(
            self._open_google_request_template
        ).PostOpenGoogleAuthenticatorRequest

    @property
    def open_phone_request_model(self):
        return self._get_corresponding_model(
            self._open_phone_request_template
        ).PostOpenPhoneAuthenticatorRequest

    @property
    def close_google_request_model(self):
        return self._get_corresponding_model(
            self._close_google_request_template
        ).PostCloseGoogleAuthenticatorRequest

    @property
    def close_phone_request_model(self):
        return self._get_corresponding_model(
            self._close_phone_request_template
        ).PostClosePhoneAuthenticatorRequest

    @property
    def set_password_request_model(self):
        return self._get_corresponding_model(
            self._set_password_request_template).PostSetPasswordRequest

    @property
    def reset_password_request_model(self):
        return self._get_corresponding_model(
            self._rest_password_request_template).PostResetPasswordRequest

    @property
    def verify_password_request_model(self):
        return self._get_corresponding_model(
            self._password_verify_request_template
        ).PostPasswordValidationRequest

    @property
    def account_api(self):
        return self._account_api

    @property
    def verify_api(self):
        return self._verify_api

    @property
    def asset_api(self):
        return self._asset_api

    @property
    def init_google_request_model(self):
        return self._get_corresponding_model(
            self._init_google_request_template).InitGoogleRequest

    def register(self, email=None, password=None, promotion_code=None,
                 verification_code="666666", nationality_code=None, challenge="",
                 sec_code="", validate="", nick_name=""):
        if nick_name:
            req_body = self.register_request_model(
                email=email, password=password,
                promotion_code=promotion_code,
                verification_code=verification_code,
                nationality_code=nationality_code,
                challenge=challenge, seccode=sec_code,
                validate=validate, nick_name=nick_name)
        else:
            req_body = self.register_request_model(
                email=email, password=password,
                promotion_code=promotion_code,
                verification_code=verification_code,
                nationality_code=nationality_code,
                challenge=challenge, seccode=sec_code,
                validate=validate)

        try:
            self.account_api.create_user(body=req_body)
        except self.api_exception as e:
            if e.status != 401:
                raise
            verify_info = {
                "account": "mailto:" + email,
                "baseToken": json.loads(e.body)["baseToken"],
                "code": BACK_DOOR_VERIFY_CODE,
                "type": "login",
                "challenge": str(),
                "gt": str(),
                "new_captcha": str()
            }
            self.verify(verify_info)

    def verify(self, verify_info):
        """
        :param verify_info: 验证信息
        例如{
              "account": "mailto:hello.world@email.com, number:18645511111 , google:XXXXXX",
              "code": "666666",
              "baseToken": "1234ABas12as12asd",
              "secondToken": "asasas12asasasa12s",
              "newPassword": "Ls1w1w1",
              "secondCode": "Ls1w1w1",
              "type": "login"
            }
        :return:
        """
        return self.verify_api.accounts_verify_post(
            verify_info=verify_info)

    def verify_login_or_password(self, verify_info):
        return self.verify_api.accounts_verify_login_or_password_post(
            verify_info=verify_info)

    def login(self, account="", password="",
              challenge="", sec_code="", validate=""):
        """
        :param account: 账户
        :param password: 密码
        :param challenge: 极验参数
        :param sec_code: 极验参数
        :param validate: 极验参数
        :return:
        """
        try:
            req_body = self.login_request_model(account="mailto:" + account,
                                                password=password,
                                                challenge=challenge,
                                                seccode=sec_code,
                                                validate=validate)

            res = self.account_api.accounts_login_post(body=req_body)
            return res.token
        except self.api_exception as ae:
            if ae.status != 401:
                raise
            verify_info = {
                "account": "mailto:" + account,
                "token": json.loads(ae.body)["baseToken"],
                "type": "login",
                "code": BACK_DOOR_VERIFY_CODE,
                "challenge": str(),
                "seccode": str(),
                "validate": str()
            }
            res = self.verify_login_or_password(verify_info)
            return res.token

    def logout(self, token, api_list=list()):
        """
        :param token: 登录后的token
        :param api_list: 所要取消token的接口列表
        """
        self.account_api.api_client.set_default_header("Authorization",
                                                       "Bearer " + token)
        self.account_api.accounts_logout_post()
        self.account_api.api_client.default_headers.pop("Authorization", "")
        for api in api_list:
            api.api_client.default_headers.pop("Authorization", "")

    def change_password(self, account, old_password, new_password):
        request = self.set_password_request_model(old_password=old_password,
                                                  new_password=new_password)
        try:
            self.account_api.accounts_set_password_post(body=request)
        except self.api_exception as e:
            if e.status != 401:
                raise
            verify_info = {
                "account":  "mailto:" + account,
                "baseToken": json.loads(e.body)["baseToken"],
                "code": BACK_DOOR_VERIFY_CODE,
                "type": "edit_login_pwd",
                "challenge": str(),
                "gt": str(),
                "new_captcha": str()
            }
            self.verify(verify_info)

    def reset_password(self, account, new_password):

        reset_password = self.reset_password_request_model(
            uri="mailto:" + account,
            challenge="",
            seccode="",
            validate="")
        try:
            self.account_api.accounts_reset_password_post(body=reset_password)
        except self.api_exception as e:
            if e.status != 401:
                raise
            verify_info = {
                "account": "mailto:" + account,
                "token": json.loads(e.body)["baseToken"],
                "type": "forget_pwd",
                "code": BACK_DOOR_VERIFY_CODE,
                "challenge": str(),
                "seccode": str(),
                "validate": str()
            }
            try:
                self.verify_login_or_password(verify_info)
            except self.api_exception as e:
                if e.status != 401:
                    raise
                sec_token = json.loads(e.body)["token"]
                verify_info.update({"token": sec_token,
                                    "password": new_password,
                                    "type": "edit_login_pwd"})
                self.verify_login_or_password(verify_info)

    def verify_password(self, password):
        verify_password_request = self.verify_password_request_model(password)
        self.account_api.accounts_password_validation_post(
            word=verify_password_request)

    def apply_individual_verify(self, number, token: str=""):
        """
        申请个人实名认证
        :param number: 证件号码
        :param token: 登录token
        """
        if token:
            self.account_api.api_client.set_default_header(
                "Authorization", "Bearer " + token)
        country = random_get_country_ob()["k"]
        individual = self.individual_request_model(
            nationality_code=country,
            name=get_random_name(2, 20),
            type="identityCard",
            number=number,
            front_photo="9382b4e1a51f4bf6b238e06e0fd02a4a",
            back_photo="9382b4e1a51f4bf6b238e06e0fd02a4a",
            handheld_photo="9382b4e1a51f4bf6b238e06e0fd02a4a")
        self.account_api.request_individual_certification(individual)
        return dict(country=individual.nationality_code, name=individual.name)

    def apply_company_verify(self, social_code, token: str="",
                             tax_code: str="tax_code",
                             organization_code: str="organization_code",
                             business_license: str="business_license"):
        """
        :param business_license: 营业执照副本
        :param organization_code: 组织机构编号
        :param tax_code: 税务登记证编号
        :param token: 登录token
        :param social_code: 社会统一编号
        :return:
        """
        if token:
            self.account_api.api_client.set_default_header("Authorization",
                                                           "Bearer " + token)
        nationality_code = "nationality_code"
        faker = Faker("zh_CN")
        company_info = self.company_request_model(
            company_name=faker.company() + str(random.randint(1, 10000)),
            nationality_code=nationality_code,
            area="公司所在区域",
            address=faker.address(),
            logo="9382b4e1a51f4bf6b238e06e0fd02a4a",
            social_code=social_code,
            name=get_random_name(2, 20),
            phone_number=faker.phone_number(),
            tax_number=tax_code,
            organization_code=organization_code,
            business_license=business_license
        )
        self.account_api.request_enterprise_certification(
            body=company_info)
        return dict(company_name=company_info.company_name,
                    name=company_info.name, phone=company_info.phone_number)

    def bind_google(self, google_code, token):
        bind_google_request = self.bind_google_request_model(
            google_code=google_code, token=token)
        # 绑定google
        self.account_api.accounts_bind_google_authenticator_post(
            bind_google_request)

    def bind_phone(self, phone, verify_code, area_code, token):
        bind_phone_request = self.bind_phone_request_model(
            phone_number=phone,
            verification_code=verify_code,
            area_code=area_code,
            token=token)
        # 绑定电话
        self.account_api.accounts_bind_phone_post(bind_phone_request)

    def alter_google(self, google_code, token):
        changed_google_request = self.bind_google_request_model(
            google_code=google_code, token=token)
        self.account_api.accounts_alter_google_authenticator_post(
            changed_google_request)

    def alter_phone(self, phone, verify_code, area_code, token):
        change_phone_request = self.alter_phone_request_model(
            phone_number=phone, verification_code=verify_code,
            area_code=area_code, token=token)
        # 修改电话
        self.account_api.accounts_alter_phone_post(change_phone_request)

    def open_google(self, google_code):
        # 开启谷歌验证
        open_google_request = self.open_google_request_model(
            google_code=google_code)
        self.account_api.accounts_open_google_authenticator_post(
            word=open_google_request)

    def open_phone(self, phone_code):
        open_phone_request = self.open_phone_request_model(
            phone_code=phone_code)
        self.account_api.accounts_open_phone_authenticator_post(
            word=open_phone_request)

    def close_google(self, account, verify_code, google_code):
        close_google_request = self.close_google_request_model(
            account=account,
            verification_code=verify_code,
            google_code=google_code)
        self.account_api.accounts_close_google_authenticator_post(
            word=close_google_request)

    def close_phone(self, account, verify_code, phone_code):
        close_phone_request = self.close_phone_request_model(
            account=account, verification_code=verify_code,
            phone_code=phone_code)
        self.account_api.accounts_close_phone_authenticator_post(
            word=close_phone_request)

    def init_google(self):
        # init_google_request = self.init_google_request_model(account=account)
        res = self.verify_api.accounts_init_googleauth_post()
        return res


def get_all_country_code():
    project_dir = pathlib.Path(__file__).parent.parent
    country_file = project_dir/pathlib.Path("resources/country.json")
    content = list()
    if country_file.exists() and country_file.is_file():
        content = country_file.read_text(encoding="utf-8")
        content = json.loads(content)
    return content


def random_get_country_code():
    country_list = get_all_country_code()
    country = random.choice(country_list)
    return country.get("n")


def random_get_country_ob():
    country_list = get_all_country_code()
    country = random.choice(country_list)
    return country


def get_random_id_number():
    arr = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    last = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    t = time.localtime()[0]
    x = '%02d%02d%02d%04d%02d%02d%03d' % (random.randint(10, 99),
                                          random.randint(1, 99),
                                          random.randint(1, 99),
                                          random.randint(t-80, t-18),
                                          random.randint(1, 12),
                                          random.randint(1, 28),
                                          random.randint(1, 999))
    y = 0
    for i in range(17):
        y += int(x[i]) * arr[i]
    return '%s%s' % (x, last[y % 11])


def get_random_name(min_num, max_num):
    all_chart = string.ascii_letters + string.digits
    string_len = random.randint(min_num, max_num)
    choice_chart = random.sample(all_chart, k=string_len)
    return "".join(choice_chart)
