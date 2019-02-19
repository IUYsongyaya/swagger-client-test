from swagger_client.otc.models import CreateAdRequest
from swagger_client.otc.models import PostPaymodeRequest, PaymodeInfo, CreateOrderRequest, UpdatePaymodeRequest
from test.otc.scenario.data.data import get_random_data, CURRENCYID, get_random_lowercase


# 默认卖币
def create_ad(ad_api, data, coind_id, assetpwd, *, direction=2):
    price, amount = data
    payload = CreateAdRequest(
        price=price,
        amount=amount,
        type=direction,
        asset_password=assetpwd,
        max_limit=500_000,
        min_limit=100,
        currency_id=coind_id)
    ad = ad_api.advertise_create_advertise_post(payload)
    return ad


def create_paymode(pay_mode_api, asset_password, *,  way='we_chat'):
    payload = PostPaymodeRequest()
    type_map = {"bank": 3, "ali_pay": 2, "we_chat": 1}
    payload.type = type_map[way]
    payload.qrcode = 'qr_code'
    payload.account = "liujun@192.com"
    payload.asset_password = asset_password
    if way == 'bank':
        payload.bank_name = "招商银行"
        payload.branch_name = "深圳罗湖支行"
    one_pay_way_res = pay_mode_api.paymode_add_post(body=payload)
    pay_mode_api.paymode_enable_paymode_id_put(paymode_id=one_pay_way_res.id)
    return one_pay_way_res.id
