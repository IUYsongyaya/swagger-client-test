#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-6
import logging
from test.tenant.instance import get_templated_attrs
from test.tenant.id_settings import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


class Project:
    
    attrs_template = dict(
        project_name=lambda name, index: f"prj_{CONFIG.TESTER}_%s%s%s" % (num_2_ascii(index)),
        full_name=lambda name, index: f"coin_{CONFIG.TESTER}_%s%s%s" % (num_2_ascii(index)),
        short_name=lambda name, index: f"{CONFIG.TESTER.upper()}%s%s%s" % (num_2_ascii(index)),
        project_id="",
        coin_id="",
        sponsor_id="",
        application_id=-1)

    def __init__(self, index=None, attrs=None):
        if attrs:
            for key, val in attrs.items():
                setattr(self, key, val)
        else:
            assert isinstance(index, int), "Index must be a int if attrs is None for auto attrs gen"
            for key, val in get_templated_attrs(type(self), index).items():
                setattr(self, key, val)

    def __repr__(self):
        cls_name = f"< {type(self).__name__}"
        attrs_info = ""
        for key, val in self.__dict__.items():
            if not callable(val):
                attrs_info += f"  {key}: {val}  "
        else:
            attrs_info += " >"
        return cls_name+attrs_info
    

def main():
    
    _staff = Staff(CONFIG.STAFF_INDEX)
    _venture = Venture(CONFIG.VENTURE_INDEX)
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    
    _tenant.request_individual_cert()
    _staff.verify_individual(identity=_tenant.identity, approval="ACCEPTED")
    _exchange = _tenant.get_exchange()
    assert _exchange, "Must have a exchange first"
    
    _sponsor = Sponsor(CONFIG.SPONSOR_INDEX)
    
    _exchange = _tenant.get_exchange()
    assert _tenant.is_exchange_approved(), "exchange must be approved first"
    
    _project = _venture.get_project(CONFIG.PROJECT_INDEX)
    if not _project:
        _project = _venture.create_project(CONFIG.PROJECT_INDEX)
    assert _project, "create project return must not null"
    logger.info("==========  Project(%u) %s: %s(%s) Done ==========", CONFIG.PROJECT_INDEX, _project.project_name, _project.full_name,
                _project.short_name)

    sponsor_id = _venture.query_sponsor_id(_sponsor.name)
    print("sponsor id ============>", sponsor_id)

    for app in _venture.list_applications():
        _venture.set_sponsor(sponsor_id, app.id)

    app_id = _sponsor.query_project_application_id(_project.project_name)
    if app_id:
        _sponsor.sponsor_project(app_id)
    _project = _venture.update_project_info(CONFIG.PROJECT_INDEX)
    assert _project
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
    
    _venture.contacts(project_id=_project.project_id, exchange_id=_exchange.exchange_id, sponsor="venture")
    
    for contact in _tenant.list_contacts(_exchange.exchange_id, status="pending"):
        _tenant.contact_accept(contact_id=contact.id, status="accepted")
    logger.info("==========  Venture(%u) contact Tenant(%u) Done  ==========" % (CONFIG.VENTURE_INDEX, CONFIG.TENANT_INDEX))
    
    
if __name__ == '__main__':
    from test.tenant.staff import Staff
    from test.tenant.venture import Venture
    from test.tenant.tenant import Tenant
    from test.tenant.sponsor import Sponsor
    main()
