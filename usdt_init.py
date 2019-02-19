# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-19


import logging
from test.tenant.main import Main
from test.tenant.sponsor import Sponsor
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.instance import get_templated_attrs
from test.tenant.id_settings import *
from common.photo import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


def main():
    logger.info("========== Init USDT Start ==========")

    _staff = Staff(CONFIG.STAFF_INDEX)
    logger.info("==========  Staff(%u) ready  ==========" % CONFIG.STAFF_INDEX)

    _main = Main(CONFIG.MAIN_INDEX)
    _main.request_individual_cert()
    _staff.verify_individual(identity=_main.identity, approval="ACCEPTED")
    logger.info("==========  Main(%u) ready  ==========" % CONFIG.MAIN_INDEX)

    sponsor_info = get_templated_attrs(Sponsor, CONFIG.SPONSOR_INDEX)
    logger.info("template result: ", sponsor_info)
    if _staff.create_sponsor(**sponsor_info):
        _sponsor = Sponsor(CONFIG.SPONSOR_INDEX)
    else:
        assert 0, "staff create sponsor failed!"
    logger.info("==========  Sponsor(%u) Done  ==========" % CONFIG.SPONSOR_INDEX)

    _venture = Venture(1)
    _venture.request_individual_cert()
    _staff.verify_individual(identity=_venture.identity, approval="ACCEPTED")
    assert _venture.audit_accepted()
    logger.info("==========  Venture(%u) Done  ==========" % CONFIG.VENTURE_INDEX)
    project_name = "泰达币"
    full_name="Tether"
    short_name = "USDT"
    USDT_PRJ = {
            'project_name': project_name,
            'description': f'USDT almost is USD',
            'official_website': 'https://tether.to/',
            'white_paper_key': f'1234555',
            'area_code': '+86',
            'project_poster_key': "1234555",
            'cellphone': '13510022445',
            'telephone': '12874846',
            'email': '1234832456@qq.com',
            'full_name': full_name,
            'short_name': short_name,
            'issue_price': '2.24545',
            'issued_volume': '1000000',
            'circulation_volume': '1000000',
            'issued_date': '2018-08-08',
            "coin_logo_key": PHOTO_KEY,
            'blockchain_type': 'public_chain',
            'data_link': 'https://tether.to/',
            'block_browser': 'https://omniexplorer.info'
        }
    _project = _venture.create_project(attrs=USDT_PRJ)

    logger.info("==========  Project(%u) %s: %s(%s) Done ==========", CONFIG.PROJECT_INDEX, _project.project_name,
                _project.full_name,
                _project.short_name)

    sponsor_id = _venture.query_sponsor_id(_sponsor.name)
    logger.info("sponsor id:%s ============>" % sponsor_id)

    for app in _venture.list_applications():
        _venture.set_sponsor(sponsor_id, app.id)

    app_id = _sponsor.query_project_application_id(_project.project_name)
    if app_id:
        _sponsor.sponsor_project(app_id)

    _project = _venture.update_project_info(CONFIG.PROJECT_INDEX)

    logger.info("==========  Sponsor(%u) $$$ Project(%u) %s: %s(%s) Done =========="
                % (CONFIG.SPONSOR_INDEX, CONFIG.PROJECT_INDEX, _project.project_name, _project.full_name, _project.short_name))

    for config in _staff.get_coins_config_list():
        if config.coin_id == _project.coin_id:
            print("%s config id:%s" % (_project.coin_id, config.id))
            _staff.init_coin(usdt_price=1, config_id=config.id)
            _staff.config_coin_rechargable(config.id, rechargeable=True)
            _staff.config_coin_withdrawable(config.id, withdrawable=True)
    logger.info("==========  Init Project(%u) %s: %s(%s) Done  ==========" % (CONFIG.PROJECT_INDEX, _project.project_name,
                                                                              _project.full_name, _project.short_name))
    logger.info("========== Init USDT End ==========")


if __name__ == '__main__':
    main()
