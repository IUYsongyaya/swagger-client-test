# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/19 16:22

import sys
import pytest

PY3 = sys.version_info[0] == 3
pytest_plugins = "pytester",


def run(testdir, path='a.yaml', *args):
    path = testdir.tmpdir.join(path)
    result = testdir.runpytest('--simple', path, *args)
    with open(str(path)) as f:
        text = f.read()
    return result, text