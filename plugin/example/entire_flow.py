# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/19 17:10

import random

from faker import Faker

fake = Faker()

from faker.providers import BaseProvider
from collections import defaultdict


class MyProvider(BaseProvider):
    def foo(self):
        return random.choice(['bar1', 'bar2', 'bar3', 'bar4', 'bar5'])


fake.add_provider(MyProvider)

# print(fake.foo())


####################


from faker import Factory

fake = Factory.create('zh_CN')
# for _ in range(10):
#     # print(fake.address())
#     # print(fake.city())
#     print(fake.company())


####################

def get_random_char(num):
    str = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join([random.choice(str) for _ in range(num)])

dict_data = {
    'name': fake.name(),
    'id': random.choice(range(1, 11)),
    'market': random.choice(["ETH/USDT", "BTC/USDT"]),
    'page': random.choice(range(1, 5)),
    'email': random.choice(['liguobin@wanshare.com', 'hello@qq.com']),
    'startTime': '2018-12-12 12:13:09',
    'endTime': '2018-12-21 15:17:20',
    'createdStartAt': '2018-12-12 12:13:09',
    'createdEndAt': '2018-12-21 15:17:20',
    'ids': '1,2,3',
    'description': 'here is description information',
    'coinName': random.choice(['ETH', 'BTC', 'XRP']),
    'code': '231',

    'string': get_random_char(5),
    'integer': random.choice(range(0, 100)),
    'number': random.choice([12.3, 50.1]),
    'boolean': random.choice([True, False]),
    'body': 'obj'
}

# print(dict_data['name'])
# print(dict_data['id'])
# print(dict_data['market'])
# print(dict_data)


####################

from collections import namedtuple
from ruamel import yaml


class Swagger:
    def __init__(self):
        self.base_url = 'http://192.168.56.1:7777/v1'
        self.mock = Mock()
        self.urls = []
        self.paths = {}
        self.definitions = []
        self.hosts = []

    def parse_file(self, file):
        data = yaml.safe_load(open(file, encoding='utf-8'))
        self.urls = list(data['paths'].keys())
        self.paths = data['paths']
        self.definitions = data['definitions']

    def parse_files(self, files):
        files = zip(files, self.hosts)
        for file, host in files:
            data = yaml.safe_load(open(file, encoding='utf-8'))
            self.urls = self.urls + list(data['paths'].keys())
            for key, value in data['paths'].items():
                data['paths'][key]['host'] = host
            self.paths = dict(self.paths, **data['paths'])
            self.definitions = dict(self.definitions, **data['definitions'])

    def get_params(self):
        pass

    def get_data(self, url):
        pass

    def get_api(self, url):
        obj = self.get_obj(url)
        print('host:', obj.host)
        print('url:', obj.url)
        print('method:', obj.method)
        print('query:', obj.query)
        print('path:', obj.path)
        print('body:', obj.body)
        # print('response', obj.response)

        # response = requests.request(obj.method, obj.url, json=obj.body, params=obj.query, auth=self.get_auth())
        # return response.json() if response else response
        return obj

    def get_all_api(self):
        for url in self.urls:
            self.get_api(url)
            print('*' * 100)

    def get_auth(self):
        return dict(api_key='xxxx')

    def parse_ref(self, str):
        # str = '#/definitions/GetStaffListResponse'
        return str[str.rindex('/') + 1:]

    def asset_data(self, keyword, actual, expected):
        pass

    def check_data_flow(self):
        pass

    def parse_params(self, params):
        data = defaultdict(list)
        for p in params:
            data[p['in']].append((p['name'], p))
        return dict(data)

    def parse_properties(self, properties):
        # print('properties', properties)
        return dict([(name, self.mock.get_data(name, obj['type'])) for name, obj in properties.items()])

    def parse_body(self, params):
        schema = params['schema']
        if schema.get('$ref'):
            ref = self.parse_ref(schema['$ref'])
            return self.parse_properties(self.definitions[ref]['properties'])

        if schema.get('properties'):
            return self.parse_properties(schema['properties'])

        return {}

    def filled_data(self, obj):

        if obj.params.get('path'):
            url_path = [(p, self.mock.get_data(p, params['type'])) for p, params in obj.params['path']]
            obj.url = obj.url.format(**dict(url_path))

        if obj.params.get('body'):
            obj.body = self.parse_body(obj.params['body'][0][1])

        if obj.params.get('query'):
            obj.query = dict([(q, self.mock.get_data(q, params['type'])) for q, params in obj.params['query']])

    def get_obj(self, url):
        api = namedtuple('api', ['url', 'host', 'method', 'params', 'body', 'path', 'query', 'response'])

        try:
            data = self.paths[url]
        except KeyError:
            return api('', '', 'get', {}, {}, {}, {}, {})

        api.url = url
        api.host = data['host']
        api.method = next(iter(data.keys()))
        values = data.values()
        dict_value = next(iter(values))
        api.params = self.parse_params(dict_value['parameters']) if dict_value.get('parameters') else {}
        api.path = {}
        api.body = {}
        api.query = {}
        api.responses = dict_value['responses']
        self.filled_data(api)
        return api


class Mock:
    def __init__(self):
        pass

    def get_data(self, name, type='string'):
        if name in dict_data:
            return dict_data.get(name)
        return dict_data.get(type)

    def group_test(self):
        group_params = [
            {
                'url': '/init-captcha',
                'result': 'success',
                'asset': True
            },
            {
                'url': '/init-googleauth',
                'result': 'account',
                'asset': True
            }
        ]

        result = {}
        for p in group_params:
            # result = requests.get(p['url']).json().get('result')
            # assert p['asset']
            pass


if __name__ == '__main__':
    swagger = Swagger()
    # swagger.parse_file('crush-staff.yaml')
    swagger.hosts = ['http://192.168.56.1:7777/v1', 'http://192.168.56.1:8888/v1']
    swagger.parse_files(['crush-staff.yaml', 'otc.yaml'])

    for url in swagger.urls:
        swagger.get_api(url)

        print('*' * 100)

