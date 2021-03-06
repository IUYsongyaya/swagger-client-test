# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 19-1-14
import pytest
import logging
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


@pytest.fixture(scope="session")
def setup():
    logger.info("++  Multi Market  ++")
    
    _staff = Staff(CONFIG.STAFF_INDEX)
    logger.info("==========  Staff(%u) ready  ==========" % CONFIG.STAFF_INDEX)
    
    for item in _staff.list_tags():
        if item.name == CONFIG.MY_TAG:
            break
    else:
        _staff.create_tag(tag=CONFIG.MY_TAG, other_language=[{"key": "英语", "value": "public_chain"}])
    logger.info("==========  tag < %s > ready  ==========" % CONFIG.MY_TAG)
    
    _main = Main(CONFIG.MAIN_INDEX)
    _main.request_individual_cert()
    _staff.verify_individual(identity=_main.identity, approval="approved")
    logger.info("==========  Main(%u) ready  ==========" % CONFIG.MAIN_INDEX)
    
    sponsor_info = get_templated_attrs(Sponsor, CONFIG.SPONSOR_INDEX)
    logger.info("template result: ", sponsor_info)
    if _staff.create_sponsor(**sponsor_info):
        _sponsor = Sponsor(CONFIG.SPONSOR_INDEX)
    else:
        assert 0, "staff create sponsor failed!"
    logger.info("==========  Sponsor(%u) Done  ==========" % CONFIG.SPONSOR_INDEX)
    
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    _tenant.request_individual_cert()
    _staff.verify_individual(identity=_tenant.identity, approval="approved")
    assert _tenant.audit_accepted()
    logger.info("==========  Tenant(%u) Create Done  ==========" % CONFIG.TENANT_INDEX)
    
    _exchange = _tenant.get_exchange()
    if not _exchange:
        _exchange = _tenant.create_exchange()
    
    audits = _staff.query_audits_tenant(uid=_tenant.account_id, status="audit")
    
    for audit in audits:
        _staff.audits_tenants(task_id=audit.id, approval="approved")
        
        result = _staff.get_tenant_indiv_audits_result(audit_id=audit.id)
        assert result.audit_status == "approved"
    
    re_audits = _staff.query_audits_tenant(uid=_tenant.account_id, status="re_audit")
    for re_audit in re_audits:
        _staff.reaudits_tenants(task_id=re_audit.id, approval="approved")
        
        result = _staff.get_tenant_indiv_re_audits_result(audit_id=re_audit.id)
        assert result.re_status == "approved"
    
    if _tenant.is_exchange_approved():
        _exchange = _tenant.update_exchange_info()
    else:
        assert 0, "exchange should be approved here"
    
    logger.info("==========  exchange_id:%s ready ==========" % (_exchange.exchange_id))
    
    _venture = Venture(CONFIG.VENTURE_INDEX)
    _venture.request_individual_cert()
    _staff.verify_individual(identity=_venture.identity, approval="approved")
    assert _venture.audit_accepted()
    logger.info("==========  Venture(%u) Done  ==========" % CONFIG.VENTURE_INDEX)
    
    _project = _venture.get_project(CONFIG.PROJECT_INDEX)
    if not _project:
        _project = _venture.create_project(CONFIG.PROJECT_INDEX)
    
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
                % (CONFIG.SPONSOR_INDEX, CONFIG.PROJECT_INDEX, _project.project_name, _project.full_name,
                   _project.short_name))
    
    for config in _staff.get_coins_config_list():
        if config.coin_id == _project.coin_id:
            print("%s config id:%s" % (_project.coin_id, config.id))
            _staff.init_coin(usdt_price=1, config_id=config.id)
            _staff.config_coin_rechargable(config.id, rechargeable=True)
            _staff.config_coin_withdrawable(config.id, withdrawable=True)
    logger.info(
        "==========  Init Project(%u) %s: %s(%s) Done  ==========" % (CONFIG.PROJECT_INDEX, _project.project_name,
                                                                      _project.full_name, _project.short_name))
    
    _venture.contacts(project_id=_project.project_id, exchange_id=_exchange.exchange_id, sponsor="venture")
    
    for contact in _tenant.list_contacts(_exchange.exchange_id, status="pending"):
        print("contact_id ====================>", contact.id)
        _tenant.contact_accept(contact_id=contact.id, status="accepted")
    logger.info(
        "==========  Venture(%u) contact Tenant(%u) Done  ==========" % (CONFIG.VENTURE_INDEX, CONFIG.TENANT_INDEX))
    
    usdt_id = _venture.get_usdt_coin_id()
    _market = _tenant.get_market(buy=usdt_id, sell=_project.coin_id)
    _faucet = Faucet(_tenant.token_mgr.token, _tenant.api_account.api_client.configuration.host)
    if not _market:
        _faucet.free_charge(coin_id=_venture.get_usdt_coin_id(), amount=10000000000)
        logger.info(
            "==========  Faucet(%s) charge Tenant(%u) Done ==========" % (CONFIG.FAUCET_INDEX, CONFIG.TENANT_INDEX))
        _market, order_id = _tenant.create_market(usdt_id, _project.coin_id, "6", "0")
    logger.info("==========  Tenant(%u) create Market(%s) Done ==========" % (CONFIG.TENANT_INDEX, _market.market_id))
    
    logger.info("========== Multi Market End ==========")
    return _staff, _tenant, _venture, _sponsor, _faucet, _exchange


def test(setup):
    _staff, _tenant, _venture, _sponsor, _faucet, _exchange = setup
    
    _project = _venture.create_project(attrs=dict(
        project_name="prj2_zxy_001",
        full_name = "coin2_zxy_001",
        short_name = "2XY001"
    ))

    logger.info("==========  Project %s: %s(%s) Done ==========", _project.project_name,
                _project.full_name,
                _project.short_name)

    sponsor_id = _venture.query_sponsor_id(_sponsor.name)
    logger.info("sponsor id:%s ============>" % sponsor_id)

    for app in _venture.list_applications():
        _venture.set_sponsor(sponsor_id, app.id)

    app_id = _sponsor.query_project_application_id(_project.project_name)
    if app_id:
        _sponsor.sponsor_project(app_id)

    _project = _venture.get_project(project_name=_project.project_name)

    logger.info("==========  Sponsor(%u) $$$ Project %s: %s(%s) Done =========="
                % (CONFIG.SPONSOR_INDEX, _project.project_name, _project.full_name,
                   _project.short_name))

    for config in _staff.get_coins_config_list():
        if config.coin_id == _project.coin_id:
            print("%s config id:%s" % (_project.coin_id, config.id))
            _staff.init_coin(usdt_price=1, config_id=config.id)
            _staff.config_coin_rechargable(config.id, rechargeable=True)
            _staff.config_coin_withdrawable(config.id, withdrawable=True)
    logger.info(
        "==========  Init Project %s: %s(%s) Done  ==========" % (_project.project_name, _project.full_name, _project.short_name))

    _venture.contacts(project_id=_project.project_id, exchange_id=_exchange.exchange_id, sponsor="venture")

    for contact in _tenant.list_contacts(_exchange.exchange_id, status="pending"):
        print("contact_id ====================>", contact.id)
        _tenant.contact_accept(contact_id=contact.id, status="accepted")
    logger.info(
        "==========  Venture(%u) contact Tenant(%u) Done  ==========" % (CONFIG.VENTURE_INDEX, CONFIG.TENANT_INDEX))

    usdt_id = _venture.get_usdt_coin_id()
    _market = _tenant.get_market(buy=usdt_id, sell=_project.coin_id)
    if not _market:
        _faucet.free_charge(coin_id=_venture.get_usdt_coin_id(), amount=10000000000)
        logger.info(
            "==========  Faucet(%s) charge Tenant(%u) Done ==========" % (CONFIG.FAUCET_INDEX, CONFIG.TENANT_INDEX))
        _market, order_id = _tenant.create_market(usdt_id, _project.coin_id, "6", "0")
    logger.info("==========  Tenant(%u) create Market(%s) Done ==========" % (CONFIG.TENANT_INDEX, _market.market_id))

    logger.info("========== Multi Market End ==========")