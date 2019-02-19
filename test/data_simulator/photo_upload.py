# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-22

import os
import logging
import json
from test.tenant.tenant import Tenant
from test.tenant.main import Main
from test.tenant.faucet import Faucet
from test.tenant.sponsor import Sponsor
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.instance import get_templated_attrs
from test.tenant.id_settings import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)

CUR_DIR=os.path.dirname(os.path.abspath(__file__))


def list_all_photos(directory):
    paths = list()
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.jpg') or f.endswith('.png'):
                path = os.path.join(root, f)
                paths.append(path)
    return paths


def retrieve_logo_data(path):
    try:
        with open(path, "rb") as j:
            return json.loads(j.read())
    except FileNotFoundError as e:
        # logger.exception(e)
        return []
    

def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    for root, dirs, files in os.walk(CUR_DIR+"/data/"):
        for dirct in dirs:
            abs_path = root + f"{dirct}"
            photos = sorted(list_all_photos(abs_path), key=lambda path: int(os.path.basename(path)[:-4]))
            photo_json = retrieve_logo_data(abs_path+"/photo.json")
            if len(photos) > len(photo_json):
                photo_json = []
                for photo in photos:
                    key, url = _staff.upload(photo)
                    # key, url = "key", "url"
                    logger.info("upload %s with key:%s url:%s" % (photo, key, url))
                    photo_json.append(dict(key=key, url=url))
                with open(abs_path+"/photo.json", "w") as f:
                    f.write(json.dumps(photo_json))
            logger.info("==========  Upload %u photo done  ==========" % len(photo_json))


if __name__ == '__main__':
    main()
