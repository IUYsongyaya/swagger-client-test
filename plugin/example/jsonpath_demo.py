# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/21 17:32

# import requests
import jsonpath
import pprint

# url = "http://www.lagou.com/lbs/getAllCitySearchLabels.json"
#
# jsonobj = requests.get(url).json()
#
# citylist = jsonpath.jsonpath(jsonobj, '$..name')
#
# print(citylist)


data = {
    "store": {
        "book": [
          { "category": "reference",
            "author": "Nigel Rees",
            "title": "Sayings of the Century",
            "price": 8.95
          },
          { "category": "fiction",
            "author": "Evelyn Waugh",
            "title": "Sword of Honour",
            "price": 12.99
          },
          { "category": "fiction",
            "author": "Herman Melville",
            "title": "Moby Dick",
            "isbn": "0-553-21311-3",
            "price": 8.99
          },
          { "category": "fiction",
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

# pprint.pprint(jsonpath.jsonpath(data, '$.store.book[*].author'))
# pprint.pprint(jsonpath.jsonpath(data, '$..author'))
# # pprint.pprint(jsonpath.jsonpath(data, '$.store.*'))
# pprint.pprint(jsonpath.jsonpath(data, '$.store..price'))
# pprint.pprint(jsonpath.jsonpath(data, '$..book[2]'))
# pprint.pprint(jsonpath.jsonpath(data, '$..book[(@.length-1)]'))
# pprint.pprint(jsonpath.jsonpath(data, '$..book[-1:]'))
# pprint.pprint(jsonpath.jsonpath(data, '$..book[0,1]'))
# pprint.pprint(jsonpath.jsonpath(data, '$..book[:2]'))
# pprint.pprint(jsonpath.jsonpath(data, '$..book[?(@.isbn)]'))
# pprint.pprint(jsonpath.jsonpath(data, '$..book[?(@.price<10)]'))
# pprint.pprint(jsonpath.jsonpath(data, '$..*'))
pprint.pprint(jsonpath.jsonpath(data, '$..book[1].author'))
pprint.pprint(jsonpath.jsonpath(data, '$.store.book[0].title1'))




