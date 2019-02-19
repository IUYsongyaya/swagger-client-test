# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-20

#
# 校验项目名是否已存在 - 创建需审批项目 - 查看申请列表 - 获取项目列表 - 获取项目状态
#
import pytest
import logging
from test.tenant.staff import Staff
from test.tenant.tenant import Tenant
from test.tenant.venture import Venture
from test.tenant.sponsor import Sponsor
from test.tenant.main import Faucet
from test.tenant.main import Main
from test.tenant.id_settings import Config
from test.tenant.instance import get_templated_attrs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


@pytest.fixture(scope="session")
def setup():
    CONFIG = Config()
    
    _staff = Staff(CONFIG.STAFF_INDEX)
    
    _tenant = Tenant(CONFIG.TENANT_INDEX)
    _venture = Venture(CONFIG.VENTURE_INDEX)
    _main = Main(CONFIG.MAIN_INDEX)
    
    _tenant.request_individual_cert()
    _venture.request_individual_cert()
    _main.request_individual_cert()
    
    _staff.verify_individual(identity=_tenant.identity, approval="approved")
    rsp = _staff.get_indiv_audits_result(account_id=_tenant.account_id)
    assert rsp.certification_status == "ACCEPTED"
    _staff.verify_individual(identity=_venture.identity, approval="approved")
    rsp = _staff.get_indiv_audits_result(account_id=_venture.account_id)
    assert rsp.certification_status == "ACCEPTED"
    # rsp = _staff.verify_individual(identity=_faucet.identity, approval="approved")
    # assert rsp.certification_status == "ACCEPTED"
    # rsp = _staff.verify_individual(identity=_main.identity, approval="approved")
    # assert rsp.certification_status == "ACCEPTED"
    
    sponsor_info = get_templated_attrs(Sponsor, CONFIG.SPONSOR_INDEX)
    if _staff.create_sponsor(**sponsor_info):
        _sponsor = Sponsor(CONFIG.SPONSOR_INDEX)
    else:
        assert 0, "staff create sponsor failed!"
    _sponsor = Sponsor(CONFIG.SPONSOR_INDEX)

    # =================== 创建 tags ========================
    for item in _staff.list_tags():
        if item.name == CONFIG.MY_TAG:
            break
    else:
        _staff.create_tag(tag=CONFIG.MY_TAG, other_language=[{"key": "英语", "value": "public_chain"}])
    logger.info("==========  tag < %s > ready  ==========" % CONFIG.MY_TAG)

    # =================== 创建 交易所 ========================
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

    logger.info(
        "==========  exchange_id:%s ready ==========" % _exchange.exchange_id)

    # ================ 创建项目 =============================
    _project = _venture.get_project(CONFIG.PROJECT_INDEX)

    if not _project:
        _project = _venture.create_project(CONFIG.PROJECT_INDEX)
    assert _project
    
    logger.info("==========  Project(%u) %s: %s(%s) Done ==========", CONFIG.PROJECT_INDEX, _project.project_name,
                _project.full_name,
                _project.short_name)
    
    # ======================= sponsor 保荐项目 ========================
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

    # ========================= staff 初始化项目 ============================
    for config in _staff.get_coins_config_list():
        if config.coin_id == _project.coin_id:
            print("%s config id:%s" % (_project.coin_id, config.id))
            _staff.init_coin(usdt_price=1, config_id=config.id)
            _staff.config_coin_rechargable(config.id, rechargeable=True)
            _staff.config_coin_withdrawable(config.id, withdrawable=True)
    logger.info(
        "==========  Init Project(%u) %s: %s(%s) Done  ==========" % (CONFIG.PROJECT_INDEX, _project.project_name,
                                                                      _project.full_name, _project.short_name))

    return _staff, _tenant, _venture, _project, _exchange, CONFIG


def test(setup):
    _staff, _tenant, _venture, _project, _exchange, CONFIG = setup
    
    _venture.contacts(project_id=_project.project_id, exchange_id=_exchange.exchange_id, sponsor="venture")
    
    for contact in _tenant.list_contacts(_exchange.exchange_id, status="pending"):
        print("contact_id ====================>", contact.id)
        _tenant.contact_accept(contact_id=contact.id, status="accepted")
    print("project_id =============================>", _project.project_id)
    rsp = _tenant.get_contacts_status_by_project_id(_project.project_id)
    assert rsp.status == "accepted"