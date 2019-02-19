#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/16 16:03
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 随机生成邮箱账号
import random


def random_email(email_type=None, rang=None):
    __email_type = ["@qq.com", "@163.com", "@126.com", "@189.com"]
    # 如果没有指定邮箱类型，默认在 __email_type中随机一个
    if email_type is None:
        __randomEmail = random.choice(__email_type)
    else:
        __randomEmail = email_type
    # 如果没有指定邮箱长度，默认在4-10之间随机
    if rang is None:
        __rang = random.randint(4, 10)
    else:
        __rang = int(rang)
    __Number = "0123456789qbcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"
    __randomNumber = "".join(random.choice(__Number) for i in range(__rang))
    _email = __randomNumber + __randomEmail
    return _email
