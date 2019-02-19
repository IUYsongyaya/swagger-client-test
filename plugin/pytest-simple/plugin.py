# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/19 15:36


import pytest


def pytest_addhooks(pluginmanager):
    from . import hooks
    pluginmanager.add_hookspecs(hooks)


def pytest_runtest_setup():
    pass


class SimpleTestDev(object):

    def __init__(self):
        pass

    class TestResult:
        def __init__(self):
            pass

    def pytest_addoption(self, parser):
        parser.addoption("--gen_api_code", dest="simple pytest",
                         help="generate api code by swagger yaml file")
        parser.addoption("--gen_test_code", dest="simple pytest",
                         help="generate test code")
        parser.addoption("--gen_test_report", dest="simple pytest",
                         help="run test code and generate test report")
        parser.addoption("--simple", dest="simple pytest",
                         help="simple pytest development by one key")

    def pytest_configure(self, config):
        eventlog = config.getvalue('simple_test')
        if eventlog:
            self.eventlogfile = open(eventlog).open('w')

    def pytest_unconfigure(self, config):
        if hasattr(self, 'simple_test'):
            self.eventlogfile.close()
            del self.eventlogfile

    def pyevent(self, eventname, *args, **kwargs):
        if hasattr(self, 'simple_test'):
            print(self.eventlogfile, eventname, args, kwargs,
            self.eventlogfile.flush())

