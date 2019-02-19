#!/usr/bin/env python3

# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-6

import click
import logging

from test.tenant.tenant import Tenant
from test.tenant.main import Main, Faucet
from test.tenant.sponsor import Sponsor
from test.tenant.venture import Venture
from test.tenant.staff import Staff
from test.tenant.exchange import Exchange
from test.tenant.project import Project
from test.tenant.market import Market
from test.tenant.instance import get_templated_attrs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
logger.addHandler(ch)


@click.group()
def cli():
    pass


FAUCET_ID = 99
MAIN_ID = 0
STAFF_ID = 0
TENANT_ID = 0
VENTURE_ID = 0
SPONSOR_ID = 0
EXCHANGE_ID = TENANT_ID
PROJECT_ID = 0


platforms = {"main": Main, "staff": Staff, "tenant": Tenant, "venture": Venture, "sponsor": Sponsor, "exchange": Exchange, "project": Project, "market": Market}


@cli.command()
@click.option("--project_index", "-pi", type=int, help="Need a project index to create project")
@click.option("--venture_index", "-vi", type=int, help="Need a venture index to create project")
def create_project(project_index, venture_index):
    global _project_usdt
    _project_usdt = Project(
        index=project_index,
        venture=Venture(venture_index))


@cli.command()
def create_faucet():
    Faucet(FAUCET_ID)


@cli.command()
@click.option("--tenant_index", "-ti", type=int, help="Need a tenant index to create tenant")
def create_tenant(tenant_index):
    _staff = Staff(STAFF_ID)
    _tenant = Tenant(tenant_index)
    _tenant.request_individual_cert()
    _staff.verify_individual(identity=_tenant.identity, approval="approved")
    assert _tenant.audit_accepted()
    logger.info("==  Tenant(%u) ready  ==" % TENANT_ID)

    audit = _staff.query_audits_tenant(uid=_tenant.account_id, status="audit")
    if audit:
        print("audit ============>", audit)
        _staff.audits_tenants(task_id=audit.id, approval="approved")
    else:
        logger.info("No tenants to audits")

    re_audit = _staff.query_audits_tenant(uid=_tenant.account_id, status="re_audit")
    if re_audit:
        print("re_audit ============>", re_audit)
        _staff.reaudits_tenants(task_id=re_audit.id, approval="approved")
    else:
        logger.info("No tenants to re_audits")
    logger.info("tenant %u ready!" % tenant_index)
    

@cli.command()
@click.option("--exchange_index", "-ei", type=int, help="Need a exchange index to create exchange")
def create_exchange(exchange_index):
    Exchange(exchange_index)


@cli.command()
@click.option("--sponsor_index", "-ti", type=int, help="Need a sponsor index to create sponsor")
def create_sponsor(sponsor_index):
    _staff = Staff(STAFF_ID)
    sponsor_info = get_templated_attrs(Sponsor, SPONSOR_ID)
    logger.info("template result: ", sponsor_info)
    if _staff.create_sponsor(**sponsor_info):
        _sponsor = Sponsor(sponsor_index)
        logger.info("sponsor %u ready!" % sponsor_index)
    else:
        assert 0, "staff create sponsor failed!"


@cli.command()
@click.option("--venture_index", "-vi", type=int, help="Need a venture index to create venture")
def create_venture(venture_index):
    _staff = Staff(STAFF_ID)
    _venture = Venture(venture_index)
    logger.info("venture %u ready!" % venture_index)
    _venture.request_individual_cert()
    _staff.verify_individual(identity=_venture.identity, approval="approved")
    assert _venture.audit_accepted()


@cli.command()
@click.option("--project_index", "-ei", type=int, help="Need a project index to create project")
@click.option("--venture_index", "-vi", type=int, help="Need a venture index to create venture")
def create_project(project_index, venture_index):
    Project(project_index, venture=Venture(venture_index))


@cli.command()
@click.option("--main_index", "-mi", type=int, help="Need a main index to create main")
def create_main(main_index):
    _staff = Staff(STAFF_ID)
    _main = Main(main_index)
    _main.request_individual_cert()
    _staff.verify_individual(identity=_main.identity, approval="approved")
    assert _main.audit_accepted()
    

@cli.command()
@click.option("--market_id", "-mi", type=int, help="Need a market_id to open market")
def open_market(market_id):
    _staff = Staff(STAFF_ID)
    _staff.open_market(market_id)


@cli.command()
@click.option("--index", "-i", type=int, help="Need a index")
def info(index):
    print(Main(index))
    _tenant = Tenant(index)
    print(_tenant)
    _venture = Venture(index)
    print(_venture)
    print(Sponsor(index))
    _project = _venture.get_project(index)
    print(_project)
    _exchange = Tenant(index).get_exchange()
    print(_exchange)
    usdt_id = _venture.get_usdt_coin_id()
    print(_tenant.get_market(buy=usdt_id, sell=_project.coin_id))


@cli.command()
@click.option("--platform_name", "-p", type=str, help="Need a platform name")
@click.option("--index", "-i", type=int, help="Need a index")
def check_balance(platform_name, index):
    _who = platforms[platform_name](index)
    _venture = Venture(VENTURE_ID)
    print("I am:\n", _who.account_info())
    print("tenant usdt balance:", _who.query_coin_balance(_venture.get_usdt_coin_id()))


@cli.command()
@click.option("--platform_name", "-p", type=str, help="Need a platform name")
@click.option("--index", "-i", type=int, help="Need a index")
def charge(platform_name, index):
    _faucet = Faucet(FAUCET_ID)
    _who = platforms[platform_name](index)
    _venture = Venture(VENTURE_ID)
    _faucet.free_charge(_venture.get_usdt_coin_id(), _who.account_id)
    

@cli.command()
@click.option("--exchange_index", "-ei", type=int, help="Need a exchange index")
def get_exchange_and_market_infos(exchange_index):
    _tenant = Tenant(exchange_index)
    assert _tenant.is_exchange_approved()
    print(_tenant.list_markets())


if __name__ == '__main__':
    cli()

