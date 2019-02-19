# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-8
import json
import logging
from test.tenant.token_manager import TokenManager
from common.photo import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)

BACK_DOOR_VERIFY_CODE = "666666"


class Account:
    attrs_template = dict(email="", password="", name="", logo="", account="", phone="", identity="", nationality_code="",
                          account_id="")
    
    def __init__(self):
        super().__init__()
        self.token_mgr = None
        self._inited = False
    
    def request_individual_cert(self):
        req = self.PostIndividualCertificationRequest(
            nationality_code="cn",
            name=self.name,
            type="identityCard",
            number=self.identity,
            front_photo=PHOTO_KEY,
            back_photo=PHOTO_KEY,
            handheld_photo=PHOTO_KEY)
        try:
            self.api_account.request_individual_certification(body=req)
        except self.ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "This information has been submitted, please be patient":
                logger.warning("[ignore] Repeat individual certification request ignore")
            elif e.status == 400 and json.loads(e.body)["message"] == "ID card has been registered":
                logger.warning("[ignore] Repeat individual certification request ignore")
            elif e.status == 400 and json.loads((e.body))["message"] == "This user is already a real name user":
                logger.warning("[ignore] This user is already a real name user")
            elif e.status == 400 and (json.loads((e.body))["message"] == "该证件号已被认证" or json.loads((e.body))[
                "message"] == "该资料已经提交，请耐心等待审核"):
                logger.warning("%s" % json.loads((e.body))["message"])
            else:
                raise
        else:
            logger.info("Individual certificate success")

    def verify(self, info):
        return self.api_verification.accounts_verify_post(
            verify_info=info)

    def register(self, promotion_code="", challenge="", sec_code="", validate=True):
        req_body = self.PostRegisterRequest(
            email=self.email,
            password=self.password,
            # promotion_code=promotion_code,
            verification_code=BACK_DOOR_VERIFY_CODE,
            nationality_code=self.nationality_code,
            challenge=challenge,
            seccode=sec_code,
            validate=validate)
        try:
            self.api_account.create_user(body=req_body)
        except self.ApiException as e:
            if e.status == 400 and (
                    json.loads(e.body)["message"] == "Mailbox exists" or json.loads(e.body)["message"] == "邮箱已经存在了"):
                logger.warning("Mailbox exists")
                return True
            if e.status != 401:
                raise
            verify_info = {
                "account": "mailto:" + self.email,
                "baseToken": json.loads(e.body)["baseToken"],
                "code": BACK_DOOR_VERIFY_CODE,
                "type": "login",
                "challenge": str(),
                "gt": str(),
                "new_captcha": str()
            }
            self.verify(verify_info)

    def verify_login_or_password(self, info):
        return self.api_verification.accounts_verify_login_or_password_post(
            verify_info=info)

    def login(self, challenge="", sec_code="", validate=""):
        try:
            req_body = self.PostLoginRequest(
                account="mailto:" + self.email,
                password=self.password,
                challenge=challenge,
                seccode=sec_code,
                validate=validate)

            rsp = self.api_account.accounts_login_post(body=req_body)
        except self.ApiException as ae:
            if ae.status != 401:
                raise
            verify_info = {
                "account": "mailto:" + self.email,
                "token": json.loads(ae.body)["baseToken"],
                "type": "login",
                "code": BACK_DOOR_VERIFY_CODE,
                "challenge": str(),
                "seccode": str(),
                "validate": str()
            }
            rsp = self.verify_login_or_password(verify_info)
            return rsp.token
        else:
            return rsp.token
    
    def verify_payment_token(self):
        req = {"challenge": "",
               "seccode": "",
               "validate": "true",
               "account": "mailto:" + self.email,
               "code": BACK_DOOR_VERIFY_CODE,
               "type": "pay"}
        try:
            rsp = self.verify(info=req)
        except self.ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "phone has bind":
                pass
                # logger.warning("Phone has bind")
        else:
            return rsp.token
    
    def verify_close_market_token(self):
        req = {"challenge": "",
               "seccode": "",
               "validate": "true",
               "account": "mailto:" + self.email,
               "code": BACK_DOOR_VERIFY_CODE,
               "type": "close_market"}
        try:
            rsp = self.verify(info=req)
        except self.ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "phone has bind":
                pass
                # logger.warning("Phone has bind")
        else:
            return rsp.token
    
    def bind_phone(self):
        req = {"challenge": "",
               "seccode": "",
               "validate": "true",
               "account": "mailto:" + self.email,
               "code": BACK_DOOR_VERIFY_CODE,
               "type": "bind_phone"}
        try:
            rsp = self.verify(info=req)
        except self.ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "phone has bind":
                pass
                # logger.warning("Phone has bind")
        else:
            print("verify token", rsp.token)
            req = self.PostBindPhoneRequest(
                phone_number=self.phone,
                verification_code=BACK_DOOR_VERIFY_CODE,
                area_code="+86",
                token=rsp.token)
            # 绑定电话
            self.api_account.accounts_bind_phone_post(req)

    def init_instance(self):
    
        # logger.info("<<<<<   %s   >>>>>", type(self))
        # logger.info("account %s:", self.account)
        # logger.info("password %s:", self.password)
        # logger.info("email : %s", self.email)
        # logger.info("identity : %s", self.identity)
        # logger.info("<<<<<<<<<<<<<>>>>>>>>>>>")
        
        try:
            self.register(promotion_code="90909999")
        except self.ApiException as e:
            if e.status == 400 and json.loads(e.body)["message"] == "Email exits":
                pass
                # print("Existed account, try login in, body:", json.loads(e.body))
            else:
                raise
    
        token = self.login(challenge="", sec_code="", validate="true")
        self.token_mgr = TokenManager(token)
        self.token_mgr.auth_headers(self)
        self.bind_phone()
        self.account_id = self.account_info().account_id
        self._inited = True
        
    def account_info(self):
        return self.api_account.accounts_account_info_get().account_info
    
    def audit_accepted(self):
        return self.api_account.accounts_account_info_get().certification_audit.certification_status == "accepted"
    
    @property
    def inited(self):
        return self._inited

    def __repr__(self):
        cls_name = f"< {type(self).__name__}"
        attrs_info = ""
        for key, val in self.__dict__.items():
            if not callable(val) and not key.startswith("api_") and not key.startswith("_"):
                attrs_info += f"  {key}: {val}  "
        else:
            attrs_info += " >"
        return cls_name+attrs_info