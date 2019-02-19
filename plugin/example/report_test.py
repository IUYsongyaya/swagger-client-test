# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/22 9:07

from jinja2 import Environment, FileSystemLoader
import os

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('report.html')
filename = os.path.join(root, 'html', 'report.html')

data = {
    'title': 'crush测试报告',
    'name': 'crush 平台接口(用户管理后台端) -- 测试报告',
    'project': {
        'modules': [
            {
                'name': 'verification 验证相关-李欣',
                'api': [
                    {
                        'method': 'GET',
                        'url': '/init-captcha',
                        'description': '极验初始化',
                        'result': True,
                        'reason': ''
                    },
                    {
                        'method': 'POST',
                        'url': '/init-googleauth',
                        'description': '谷歌验证初始化',
                        'result': False,
                        'reason': 'name字段不能为空'
                    },
                    {
                        'method': 'POST',
                        'url': '/get-verification-code',
                        'description': '获取验证码',
                        'result': False,
                        'reason': '验证码不能为空'
                    }
                ]
            }
        ],
        'scenarios': [
            {
                'name': '用户解锁场景测试',
                'steps': [
                    {
                        'step': '第1步',
                        'description': '获取用户信息',
                        'result': True,
                        'reason': ''
                    },
                    {
                        'step': '第2步',
                        'description': '用户解锁',
                        'result': True,
                        'reason': ''
                    },
                    {
                        'step': '第3步',
                        'description': '对比用户信息',
                        'result': False,
                        'reason': '两次获取的信息不一致'
                    }
                ]
            },
            {
                'name': '资金管理测试',
                'steps': [
                    {
                        'step': '第1步',
                        'description': '获取用户币数量',
                        'result': True,
                        'reason': ''
                    },
                    {
                        'step': '第2步',
                        'description': '提币操作',
                        'result': True,
                        'reason': ''
                    },
                    {
                        'step': '第3步',
                        'description': '获取用户币数量',
                        'result': False,
                        'reason': '提币后数量一样'
                    }
                ]
            }
        ]
    }
}

html = template.render(**data)
with open(filename, 'w', encoding='utf-8') as fh:
    fh.write(html)
