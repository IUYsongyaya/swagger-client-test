# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-22
import os
import json

CUR_DIR=os.path.dirname(os.path.abspath(__file__))

exchange_items = [
    dict(name="sBitMan", nationality="SC", tags="挖矿返利"),
    dict(name="sEax", nationality="MT", tags="挖矿返利"),
    dict(name="sBsuper", nationality="TW", tags="交易手续费低"),
    dict(name="sCoinMate", nationality="KY", tags="交易手续费低"),
    dict(name="sHighTop", nationality="KR", tags="优选币种"),
    dict(name="sGemini", nationality="US", tags="交易返利"),
    dict(name="sHotcoin", nationality="SG", tags="挖矿返利"),
    dict(name="sDcoin", nationality="US", tags="公开透明"),
    dict(name="sKucoin", nationality="SG", tags="挖矿返利"),
    dict(name="sBiger", nationality="HK", tags="优选币种"),
    dict(name="sKoinex", nationality="IN", tags="交易手续费低"),
    dict(name="sBBX", nationality="MT", tags="挖矿返利"),
    dict(name="s币链网", nationality="CA", tags="挖矿返利"),
    dict(name="s蚁币", nationality="AU", tags="优选币种"),
    dict(name="s趣币网", nationality="SC", tags="公开透明"),
    dict(name="sGAEA", nationality="SC", tags="挖矿返利"),
    dict(name="sSimex", nationality="RU", tags="挖矿返利"),
    dict(name="s币管家", nationality="SC", tags="优选币种"),
    dict(name="s币贝交易", nationality="SG", tags="挖矿返利"),
    dict(name="sUEX", nationality="HK", tags="优选币种")
]

countries = ["塞舌尔", "马耳他", "台湾", "开曼群岛", "韩国", "美国", "新加坡", "美国", "新加坡", "香港", "印度", "马耳他", "加拿大", "澳大利亚", "塞舌尔", "塞舌尔",
             "俄罗斯", "塞舌尔", "新加坡", "香港"]


def get_nationality_code(name):
    with open(CUR_DIR + "/../../../resources/country.json", "r") as f:
        cm = json.loads(f.read())
        for c in cm:
            if c["c"] == name:
                return c["k"]


def get_phone_num(name):
    with open(CUR_DIR + "/../../../resources/country.json", "r") as f:
        cm = json.loads(f.read())
        for c in cm:
            if c["c"] == name:
                return "+"+c["n"]


if __name__ == '__main__':
    for c in countries:
        print(get_nationality_code(c))
        print(get_phone_num(c))
