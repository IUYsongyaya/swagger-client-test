#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 15:19
# @Author  : ZDK
# @Email    : zhengdengke@wanshare.com

# 新建保荐方——获取保荐方列表——获取保荐方详情——修改保荐方状态——获取保荐方列表
from faker import Faker
import pytest

from common.utils import (get_random_name)
from common.account_sign import set_login_status
from swagger_client.staff.api.sponsors_managerment_api import SponsorsManagermentApi
from common.account_sign import get_admin_token
from swagger_client.staff.models.put_sponsor_status_request import PutSponsorStatusRequest


class TestProjectCase16(object):

    @pytest.mark.order1
    def test_applications16(self):
        faker = Faker()
        staff_api = SponsorsManagermentApi()
        staff_token = get_admin_token()
        set_login_status(staff_api, staff_token)
        sponsor = {"account": get_random_name(6, 25), "password": faker.password(),
                   "name": faker.user_name(), "email": faker.email(),
                   "phone": faker.phone_number()}
        staff_api.staff_sponsors_post(post_sponsor=sponsor)
        # 管理后台获取保健列表
        res = staff_api.staff_sponsors_get(page=1, name=sponsor.get("name"))
        id_ = ''
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.account == sponsor.get("account")
            assert item.email == sponsor.get("email")
            assert item.name == sponsor.get("name")
            assert item.status is True
            id_ = item.id
        # 管理后台获取保荐方详情
        res = staff_api.staff_sponsors_id_get(id=id_)
        assert res.email == sponsor.get("email")
        assert res.real_name == sponsor.get("name")
        assert res.id
        # 修改保荐方状态
        payload = {
                      "id": id_,
                      "status": False
                    }
        req = PutSponsorStatusRequest(**payload)
        staff_api.staff_sponsor_status_put(put_sponsor_status=req)
        # 管理后台获取保健列表
        res = staff_api.staff_sponsors_get(page=1, name=sponsor.get("name"))
        assert res.meta.total_count == 1
        for item in res.items:
            assert item.account == sponsor.get("account")
            assert item.email == sponsor.get("email")
            assert item.name == sponsor.get("name")
            assert not item.status
