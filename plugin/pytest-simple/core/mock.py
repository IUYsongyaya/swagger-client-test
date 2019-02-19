# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/19 17:10

import random
from faker import Faker
fake = Faker()

from faker.providers import BaseProvider


class MyProvider(BaseProvider):
    def foo(self):
        return random.choice(['bar1', 'bar2', 'bar3', 'bar4', 'bar5'])


fake.add_provider(MyProvider)

print(fake.foo())



####################


from faker import Factory

fake = Factory.create('zh_CN')
for _ in range(10):
    # print(fake.address())
    # print(fake.city())
    print(fake.company())


####################

dict_data = {
    'name': fake.name(),
    'id': random.choice(range(1, 11)),
    'market': random.choice(["ETH/USDT", "BTC/USDT"]),
    'page': random.choice(range(1, 5)),

    'string': random.choice('dfsdfdsfd'),
    'integer': random.choice(range(0, 100))
}

print(dict_data['name'])
print(dict_data['id'])
print(dict_data['market'])
print(dict_data)



####################

import requests


class Mock:
    def __init__(self):
        pass

    def get_data(self, name, type):
        if name in dict_data:
            return dict_data.get(name)
        return dict_data.get(type)

    def get_api(self):
        params = [
            ('name', 'string'),
            ('grade', 'integer')
        ]
        aa = [(name, self.get_data(name, type)) for name, type in params]
        print(dict(aa))

        # print(dict(params))
        # json = {
        #     'name': self.get_data('name', 'string'),
        #     'grade': self.get_data('grade', 'integer')
        # }
        # print(json)
        # return requests.get('http://www.baidu.com', json=json)

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
            result = requests.get(p['url']).json().get('result')
            assert p['asset']


if __name__ == '__main__':
    mock = Mock()
    mock.group_test()
