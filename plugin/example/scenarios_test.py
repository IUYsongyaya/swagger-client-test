# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/21 14:51


import os
from collections import namedtuple

from jinja2 import Environment, FileSystemLoader
from jsonpath import jsonpath
from ruamel import yaml

from plugin.example.entire_flow import Swagger


class Scenarios:
    def __init__(self):
        self.scenarios_report = []
        self.swagger = Swagger()
        self.swagger.hosts = ['http://192.168.56.1:7777/v1', 'http://192.168.56.1:8888/v1']
        self.swagger.parse_files(['crush-staff.yaml', 'otc.yaml'])

    def get_result(self):
        result = dict()
        result['name'] = self.report_name
        result['project'] = dict(scenarios=self.scenarios_report)
        return result

    def load_template(self, file):
        data = yaml.safe_load(open(file, encoding='utf-8'))
        self.scenarios = data['scenarios']
        self.report_name = data['name']
        self.scenarios_names = list(data['scenarios'].keys())
        print(self.scenarios)
        print(self.scenarios_names)

    def check_data(self, obj):
        valid = True
        reason = ''
        for asset in obj.assets:
            actual = obj.response.get(asset['field'])
            if asset['field'][0] == '$':
                tmp = asset['field'][1:].split('.')
                actual = getattr(obj, tmp[0]).response.get(tmp[1])

            type = asset['type']
            if type == 'equal':
                valid = valid and actual == asset['expected']
            elif type == 'not None':
                valid = valid and actual is not None
            else:
                raise Exception(f'Not have this compare type: {type}')

            if not valid:
                break

        # output check result
        if not valid:
            reason = f'地址：{obj.url} </br>' \
                     f'状态码：{obj.response["status"]} </br>' \
                     f'期望值：<span style="color:red">{asset["expected"]}</span> </br>'\
                     f'实际值：{actual}'
        return dict(result=valid, reason=reason)

    def parse_cal_value(self, dict, obj):
        dict_copy = dict.copy()
        for key, value in dict.items():
            if value[0] == '$':
                tmp = value[1:].split('.')
                dict_copy[key] = getattr(obj, tmp[0]).response.get(tmp[1])
        return dict_copy

    def parse_json_data(self, json_obj, path):
        result = jsonpath(json_obj, path)
        if not result:
            return ''
        return result[0] if len(result) == 1 else result

    def gen_report(self):
        result = self.get_result()
        print(result)

        root = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(root, 'templates')
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template('report.html')
        filename = os.path.join(root, 'html', 'report.html')

        html = template.render(**result)
        with open(filename, 'w', encoding='utf-8') as fh:
            fh.write(html)

    def mock_data(self):
        self.swagger.get_api()

    def invoke_api(self, url, step):
        obj = self.swagger.get_obj(step['url'])

        method = step.get('method', obj.method)
        params = step.get('params', {})
        body = step.get('body', {})
        auth = step.get('auth', {})

        # merge params
        if url.startswith('/'):
            url = obj.host + url
        params = dict(obj.query, **params)
        body = dict(obj.body, **body)

        # { 'api_key': token, 'Content-Type': 'application/json' }
        headers = dict({'Content-Type': 'application/json'}, **auth)

        print('url:', url)
        print('method:', method)
        print('params:', params)
        print('body:', body)
        print('headers', headers)
        print('*' * 100)

        # response = requests.request(method, url, json=body, params=params, headers=headers)
        # return response.json()

    def parse_scenarios(self, name):
        setup = self.scenarios[name].get('setup', [])
        for s in setup:
            all = self.parse_scenarios(s)
            for a in all:
                yield a

        steps = self.scenarios[name]['steps']
        scence_report = []
        objs = {}
        for step in steps:
            name = step['name']
            obj = namedtuple(name, ['asserts'])
            obj.assets = step['asserts']
            obj.url = step['url']

            for req in step.get('require', []):
                setattr(obj, req, objs[req])

            if step.get('path'):
                obj.url = step['url'].format(**self.parse_cal_value(step['path'], obj))
                # print(obj.url)

            obj.response = {}
            # todo invoke api to get response data
            out = self.invoke_api(obj.url, step)
            # print(out)
            # out = dict(id=1, name='robin', createTime='2018')
            out = {
                "store": {
                    "book": [
                        {"id": 1,
                         "category": "reference",
                         "author": "Nigel Rees",
                         "title": "Sayings of the Century",
                         "price": 8.95
                         },
                        {"id": 2,
                         "category": "fiction",
                         "author": "Evelyn Waugh",
                         "title": "Sword of Honour",
                         "price": 12.99
                         },
                        {"id": 3,
                         "category": "fiction",
                         "author": "Herman Melville",
                         "title": "Moby Dick",
                         "isbn": "0-553-21311-3",
                         "price": 8.99
                         },
                        {
                            "id": 4,
                            "category": "fiction",
                            "author": "J. R. R. Tolkien",
                            "title": "The Lord of the Rings",
                            "isbn": "0-395-19395-8",
                            "price": 22.99
                        }
                    ],
                    "bicycle": {
                        "color": "red",
                        "price": 19.95
                    }
                }
            }

            obj.response['status'] = 200
            for field, path in step.get('output', []).items():
                obj.response[field] = self.parse_json_data(out, path)

            objs[name] = obj
            check_result = self.check_data(obj)
            scence_report.append(dict(description=step['comment'], **check_result))
        yield scence_report


if __name__ == '__main__':

    scenarios = Scenarios()
    scenarios.load_template('scenarios.yml')
    for name in scenarios.scenarios_names:
        # todo 初始化数据
        all_step = scenarios.parse_scenarios(name)
        scence_report = dict(name=scenarios.scenarios[name]['description'], steps=[])
        for step in all_step:
            scence_report['steps'] += step

        scenarios.scenarios_report.append(scence_report)
        print('*' * 100)
    scenarios.gen_report()

