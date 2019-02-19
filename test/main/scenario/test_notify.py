# -*- coding: utf-8 -*-
# @File :  test_notify.py
# @Author : lh
import pytest
from common.account_sign import register_with_login, set_login_status
from swagger_client.main.api.notify_api import NotifyApi
from swagger_client.main.api.account_api import AccountApi
from swagger_client.venture.api.account_api import AccountApi as VentureAccountApi

notify_api = NotifyApi()
veture_ac_api = VentureAccountApi()
main_ac_api = AccountApi()


class TestNotify:
    @pytest.mark.parametrize('platform', ['main'])
    def test_notify(self, platform, with_login):
        """
        主平台向用户批量推送消息 -> 主平台向全终端推送消息 -> 获取消息列表
        """
        # 生成随机用户
        user1 = register_with_login(platform, with_login, [main_ac_api, notify_api])
        user2 = register_with_login(platform, with_login, [main_ac_api, notify_api])
        set_login_status(main_ac_api, user1['token'])
        user1_info = main_ac_api.accounts_account_info_get()
        user1_ac_id = user1_info.account_info.account_id
        set_login_status(main_ac_api, user2['token'])
        user2_info = main_ac_api.accounts_account_info_get()
        user2_ac_id = user2_info.account_info.account_id
        # 主平台向用户批量推送消息
        # content_str = '啊哈哈哈哈哈哈哈哈哈哈哈哈'
        # title_str = '哇哈哈统一康师傅冰红茶王老吉加多宝'
        # body = {
        #     'userIds': [user1_ac_id, user2_ac_id],
        #     'content': content_str,
        #     'title': title_str
        # }
        # notify_api.notify_batch_send_post(body)
        # user2查看消息列表
        # user1_message_info = notify_api.notify_list_get(page_no=0, page_size=5, order_by='IdDesc')
        # print('消息列表:', user1_message_info)
        # user1_message_list = [i for i in user1_message_info.data]
        # assert content_str == user1_message_list[0].content
        # assert title_str == user1_message_list[0].title
        # user1查看消息列表
        set_login_status(main_ac_api, user1['token'])
        user2_message_info = notify_api.notify_list_get(page_no=0, page_size=5, order_by='IdDesc')
        print('消息列表:', user2_message_info)
        # user2_message_list = [i for i in user2_message_info.data]
        # assert content_str == user2_message_list[0].content
        # assert title_str == user2_message_list[0].title

        # 向全终端发送消息
        # broadcast_content = '瓜子花生八宝粥'
        # broadcast_title = '辣条好劲道小当家'
        # notify_api.notify_broadcast_post(title=broadcast_title, content=broadcast_content)
