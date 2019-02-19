# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-22


import json
import logging
import datetime
from pprint import pprint
from test.tenant.tenant import Tenant
from test.tenant.main import Main
from test.tenant.faucet import Faucet
from test.tenant.sponsor import Sponsor
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.instance import get_templated_attrs
from test.data_simulator.data.data_sponsors import sponsor_items
from test.data_simulator.data.data_projects import project_items
from test.tenant.id_settings import *
from test.data_simulator.data.data_files import WHITE_PAPER_KEY, WHITE_PAPER_URL


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    _staff = Staff(CONFIG.STAFF_INDEX)
    logger.info("==========  Staff(%u) ready  ==========" % CONFIG.STAFF_INDEX)
    projects = project_items
    with open(CUR_DIR + "/data/project_logos/photo.json", "r") as f:
        logos = json.loads(f.read())
        pprint(logos)

    assert len(logos) >= len(projects), "Not enough logo photos"
    for i, prj in enumerate(projects[:1]):
        _venture = Venture(i)
        _venture.request_individual_cert()
        _staff.verify_individual(identity=_venture.identity, approval="ACCEPTED")
        assert _venture.audit_accepted()
        _project = _venture.get_project(project_name=prj["project_name"])
        if not _project:
            # _project = _venture.create_project(0, attrs={
            #     'project_name': prj["project_name"],
            #     'description': prj["description"] if len(prj["description"]) < 1024 else prj["description"][:1024],
            #     'official_website': prj["official_website"] if len(prj["official_website"]) < 32 else prj["official_website"][:32],
            #     'white_paper_key': WHITE_PAPER_KEY,
            #     'cellphone': _venture.phone,
            #     'telephone': prj["telephone"] or '12874846',
            #     'email': _venture.email or '1234832456@qq.com',
            #     'full_name': prj["full_name"] if len(prj["full_name"]) < 16 else prj["full_name"][:16],
            #     'short_name': prj["short_name"],
            #     'issue_price': str(prj["issue_price"]),
            #     'issued_volume': str(prj["issued_volume"]),
            #     'issued_date': datetime.datetime.strptime(prj["issued_date"], "%Y-%m-%d %H:%M:%S"),
            #     "coin_logo_key": logos[i]["key"],
            #     'blockchain_type': prj["blockchain_type"],
            #     'data_link': prj["data_link"][:32],
            #     'block_browser': prj["block_browser"] if len(prj["block_browser"]) < 64 else prj["block_browser"][:64]
            # })
            _project = _venture.create_project(0, attrs={
                'project_name': prj["project_name"],
                'description': prj["description"] ,
                'official_website': prj["official_website"] ,
                'white_paper_key': WHITE_PAPER_KEY,
                'cellphone': _venture.phone,
                'telephone': prj["telephone"] or '12874846',
                'email': _venture.email or '1234832456@qq.com',
                'full_name': prj["full_name"] ,
                'short_name': prj["short_name"],
                'issue_price': str(prj["issue_price"]),
                'issued_volume': str(prj["issued_volume"]),
                'issued_date': prj["issued_date"],
                "coin_logo_key": logos[i]["key"],
                'blockchain_type': prj["blockchain_type"],
                'data_link': prj["data_link"],
                'block_browser': prj["block_browser"]
            })
            sponsor_index = i % 5
            sponsor_names = sponsor_items[sponsor_index]["name"]
            _sponsor = Sponsor(sponsor_index)
            sponsor_id = _venture.query_sponsor_id(sponsor_names)
            print("%s id:%s" % (_sponsor.email, sponsor_id))
            for app in _venture.list_applications():
                _venture.set_sponsor(sponsor_id, app.id)

            print("%s sponsor %s" %(_sponsor.email, _project.project_name))
            app_id = _sponsor.query_project_application_id(_project.project_name)
            if app_id:
                _sponsor.sponsor_project(app_id)
            _project = _venture.update_project_info(_project.project_name)
            assert _project, "Update project info failed"

            for config in _staff.get_coins_config_list():
                if config.coin_id == _project.coin_id:
                    print("%s config id:%s" % (_project.coin_id, config.id))
                    _staff.init_coin(usdt_price=prj["issue_price"], config_id=config.id)
                    _staff.config_coin_rechargable(config.id, rechargeable=True)
                    _staff.config_coin_withdrawable(config.id, withdrawable=True)

            _venture.update_project_setting(_project.project_id, open=True, access_method="accept")


if __name__ == '__main__':
    main()