# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-12-17
import json
import datetime
from pprint import pprint as pprint
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


HOST = "kibana.kinmall.lan"
PORT = 9200

es = Elasticsearch(
    hosts=[dict(host=HOST, port=PORT)],
    use_ssl=False
)

INDEX = "filebeat-6.5.3-2018.12.17"
source_map = dict(
    staff="staff",
)


def filter(platform, minutes):
    return {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": "now-15m/m",
                    "lt": "now/m"
                }
            }
        }
    }
    

def main():
    print(es.info())
    # msg = es.search(index=INDEX, body=filter("tenant", 5))
    # print(msg)

    # for hit in msg["hits"]["hits"]:
    #     stamp = datetime.datetime.strptime(hit["_source"]["@timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    #     stamp.strftime("%Y-%m-%dT%H:%M:%S")
    #     print("[%s]:  %s" % (
    #     datetime.datetime.strftime(datetime.datetime.strptime(hit["_source"]["@timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"),
    #                                "%Y-%m-%d %H:%M:%S.%fZ")[:-4], hit["_source"]["message"]))
    s = Search(using=es, index=INDEX).query(source='/root/elasticsearch/logs/crush-tenant.log').filter('range', **{"@timestamp": {'gte': 'now-15m/m', 'lte': 'now/m'}})
    # s.filter('range', **{"@timestamp": {"gte": 'now-15m', "lte": 'now'}})
    rsp = s.execute()
    print(rsp)
    
    
if __name__ == '__main__':
    main()

#
# curl -H "Content-Type:application/json" "http://kibana.kinmall.lan:9200/filebeat-6.5.3-2018.12.17/doc/_search?pretty" -d '
# {
#   "query": {
#       "range": {
#             "@timestamp": {
#                 "gte": "now-15m/m",
#                 "lt": "now/m"
#             }
#       }
#   }
# }'
