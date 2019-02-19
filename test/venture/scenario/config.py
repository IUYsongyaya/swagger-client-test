#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/01/07 17:28
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com
from faker import Faker
import random

from common.utils import get_random_name
from common.photo import PHOTO_KEY

faker = Faker()
project_name = get_random_name(2, 16)
short_name = "BTC" + str(random.randint(100, 999))
full_name = get_random_name(2, 16)
payload = {
    "project_name": project_name,
    "description": "{}-description".format(project_name),
    "official_website": "www.{}.com".format(project_name),
    "white_paper_key": PHOTO_KEY,
    "area_code": "+86",
    "project_poster_key": PHOTO_KEY,
    "cellphone": "123456789",
    "telephone": "12345678910",
    "email": faker.email(),
    "full_name": full_name,
    "short_name": short_name,
    "issue_price": "2.24545",
    "issued_volume": "1000000",
    "circulation_volume": "1000000",
    "issued_date": "2018-08-08",
    "coin_logo_key": PHOTO_KEY,
    "blockchain_type": "public_chain",
    "data_link": "{}-data-link".format(project_name),
    "block_browser": "{}-block-Browser".format(project_name)
}
