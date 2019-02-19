#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-20

import sys
import os
import pprint
import swagger_client.main as Main
import swagger_client.staff as Staff
import swagger_client.tenant as Tenant
import swagger_client.venture as Venture
import swagger_client.sponsor as Sponsor
import swagger_client.otc as Otc


TEST_ROOT = os.getcwd()

OBSOLETE_FILES = ['__init__.py']
OBSOLETE_DIRS = ['interface', '.pytest_cache', 'data', 'cache', '__pycache__', 'v']
OBSOLETE_FUNC = dict(
    main=['faceid', 'faceid_result_get', 'faceid_url_get', 'get_message_list', 'messages_put', 'vps_put',
          'vps_servers_post', 'vps_servers_put'],
    staff=['accounts_id_rebates_get', 'staffs_set_password_post', 'asset_mgmt_coins_id_init_put',
           "accounts_company_audits_tasks_receive_get"],
    tenant=['faceid', 'faceid_result_get', 'faceid_url_get'],
    venture=['faceid', 'faceid_result_get', 'faceid_url_get'],
    sponsor=["sponsor_send_verification_code_post"],
    otc=['chat_msg_list_get', 'chat_new_msg_list_get', 'chat_send_post', 'order_contact_order_id_get']
)

FILES = list()

DIRS = [TEST_ROOT + '/common']

list_dirs = os.walk(TEST_ROOT + "/test/")

for root, dirs, files in list_dirs:
    for d in dirs:
        if d not in OBSOLETE_DIRS:
            print("search:", os.path.join(root, d))
            DIRS.append(os.path.join(root, d))
    

def filter_files(directory):
    src_files = list()
    files = os.listdir(directory)
    for f in files:
        if f.endswith('.py'):
            for of in OBSOLETE_FILES:
                if of == f:
                    break
            else:
                src_files.append(directory+'/'+f)
    return src_files


def search_in_dir(dir_path, search_funcs):
    missing = list(search_funcs)
    files = os.listdir(dir_path)
    for f in files:
        if not os.path.isdir(f) and f.endswith('.py'):
            # print("Search in file:", f)
            with open(dir_path+"/"+f, "r") as src:
                for line in src:
                    for func in search_funcs:
                        if func in line:
                            try:
                                missing.remove(func)
                                # print("%s found" % func)
                            except ValueError as e:
                                pass
    search_funcs = list(missing)
    return search_funcs


def api_count(swagger_client):
    apis = list()
    funcs = list()
    for api in dir(swagger_client):
        if api.endswith('Api'):
            apis.append(api)
    apis = [getattr(swagger_client, api) for api in apis]
    for api in apis:
        funcs.extend([getattr(api, f) for f in dir(api) if not (f.startswith('_') or f.endswith('_with_http_info'))])
    name = swagger_client.__name__[15:].lower()
    total = [f.__name__ for f in funcs if f.__name__ not in OBSOLETE_FUNC[name]]
    return total


STATISTICS = list()
MISSING_STATISTICS = list()


def get_author(file):
    author = ""
    with open(file, "r") as f:
        for line in f:
            if "@author" in line or "@Author" in line:
                author = line.split(":")[-1]
                if author:
                    author = author.strip()
                    break
    return author if author else "Unknown author"


OWNER_API_SET = {
    "ymy": set(),
    "ZDK": set(),
    "ljc": set(),
    "xy.zhang": set(),
    "lj": set(),
    "lh": set(),
    "lj lh": set()
}

API_OWNER_MAP = dict(
    main=dict(),
    staff=dict(),
    tenant=dict(),
    venture=dict(),
    sponsor=dict(),
    otc=dict(),
)


def parse_platform_name(path):
    platform = ""
    tail = path.split("java-crush-test2.0/test/")[-1]
    if tail:
        platform = tail.split("/")[0]
    return platform.lower() if platform else "common"


def make_empty_owner_map(funcs):
    ret = dict()
    for func in funcs:
        ret.setdefault(func, [])
    return ret
    
    
def main():
    swagger_clients = [Main, Staff, Tenant, Venture, Sponsor, Otc]
    left = list()
    for client in swagger_clients:
        apis = api_count(client)
        missing = list(apis)
        for d in DIRS:
            missing = search_in_dir(d, missing)
        STATISTICS.append(len(apis))
        MISSING_STATISTICS.append(len(missing))
        print("==================================================================================")
        print("%s total[%u] missing[%u], coverage: %.2f%%" % ( (client.__name__[15:]).upper(), len(apis), len(missing), 100 - len(missing) * 100 / len(apis)))
        print("missing:")
        print(missing)
        
        left.extend(list(missing))
        for f in missing:
            for _, val in JOB_DISPATCHED.items():
                if f in val:
                    left.remove(f)
        
    print("Total %u apis missing %u apis, coverage:%.2f%%" % (sum(STATISTICS), sum(MISSING_STATISTICS), 100 - sum(MISSING_STATISTICS)*100/sum(STATISTICS)))
    print("%u apis left :" % len(left))
    print(left)

    # src_files = list()
    # for d in DIRS:
    #     filtered = filter_files(d)
    #     src_files.extend(filtered)
    #
    # print(f"{len(src_files)} files:")
    # for f in src_files:
    #     author = get_author(f)
    #     if author == "Unknown author":
    #         print("%s => %s" % (f, author))
    #
    # for client in swagger_clients:
    #     client_name = client.__name__[15:].lower()
    #     apis = api_count(client)
    #     API_OWNER_MAP[client_name] = make_empty_owner_map(apis)
    #
    # for file in src_files:
    #     # platform = parse_platform_name(file)
    #     # print("%s ==> %s" % (file, platform))
    #     author = get_author(file)
    #     if author == "Unknown author":
    #         continue
    #     for platform_name, val in API_OWNER_MAP.items():
    #
    #         apis = [api for api in val]
    #         with open(file, "r") as f:
    #             for line in f:
    #                 for api in apis:
    #                     if api in line:
    #                         if author not in API_OWNER_MAP[platform_name][api]:
    #                             API_OWNER_MAP[platform_name][api].append(author)

    # pprint.pprint(API_OWNER_MAP)
    #
    # for platform, val in API_OWNER_MAP.items():
    #     for api, owners in val.items():
    #         for owner in owners:
    #             if owner in OWNER_API_SET:
    #                 OWNER_API_SET[owner].add(api)
    #
    # for owner in OWNER_API_SET:
    #     print("===========================================================")
    #     print("%s: got total %u apis" % (owner, len(OWNER_API_SET[owner])))
    #     for api in OWNER_API_SET[owner]:
    #         print("%s : " % api)
    #     # pprint.pprint(OWNER_API_SET[owner])
    #
    # print("===========================================================")
    # api_ng = 0
    # api_pass = 0
    # api_left = 0
    # with open("test/tenant/api_checklist.txt") as f:
    #     for l in f:
    #         if "pass" in l:
    #             api_pass += 1
    #         elif "NG" in l:
    #             api_ng += 1
    #             print(l.strip())
    #         else:
    #             api_left += 1
    #
    # print("apis pass:%u NG:%u not confirm:%u" %(api_pass, api_ng, api_left))


JOB_DISPATCHED = {
    "ZDK": ['kinmalls_get', 'kinmalls_id_get', 'kinmalls_menus_get', 'sponsor_info_post', 'sponsor_logout_post',
            'sponsor_send_verification_code_post', 'sponsor_set_password_post', 'sponsor_verify_post',
            'sponsors_ranking_get', 'sub_models_model_id_names_get', 'accounts_ventures_get',
            'accounts_ventures_id_get', 'file_key_get', 'file_key_zoom_zoom_get', 'upload'],
    "ljc": ['accounts_verify_is_valid_post', 'asset_mgmt_asset_password_has_set_account_id_get',
            'asset_mgmt_asset_password_reset_id_put', 'asset_mgmt_assets_withdraw_address_get',
            'asset_mgmt_commission_get', 'asset_mgmt_withdraw_patch_id_post', 'get_recharge_list', 'roles_list_get',
            'roles_set_staff_post', 'staffs_info_get',
            'asset_mgmt_withdraw_addresses_all_get', 'device_bind_post', 'device_unbind_post'],
    "ymy": ['system_trading_pair_update_list_put'],
    "xy.zhang": [],
    "liujun": ['admin_chat_msg_list_get', 'admin_order_cancel_times_get', 'admin_order_complete_order_count_get',
               'admin_order_reset_cancel_times_post', 'admin_paymode_user_list_get', 'admin_ad_find_page_get',
               'admin_ad_user_ad_count_get', 'accounts_otc_get'],
    "lh": ['notify_batch_send_post', 'notify_broadcast_post', 'notify_list_get', 'service_rate_get',
           'exchange_fee_history_get', 'get_message_list', 'messages_put']
    
}

if __name__ == '__main__':
    main()
