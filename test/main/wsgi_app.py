#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:ljc
@file: wsgi_app.py
@time: 2018/12/10
"""
import uuid

from flask import Flask
from flask_jsonrpc import JSONRPC


app = Flask(__name__)
json_rpc = JSONRPC(app, "/")


@json_rpc.method("get_address(coin_type=String)")
def get_address(coin_type):
    return dict(pub_address="{}_{}".format(coin_type, uuid.uuid4().hex),
                tag="{}_tag".format(coin_type))


@json_rpc.method("withdraw")
def withdraw(address, amount, coin_type, **kwargs):
    return "{}_{}_{}".format(coin_type, address, int(amount))


if __name__ == "__main__":
    app.run("0.0.0.0", 8000)
