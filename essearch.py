from elasticsearch import Elasticsearch
import json
import requests

es = Elasticsearch([{'host': 'somehost.es.amazonaws.com', 'port': 80}])

#let's iterate over swapi people documents and index them

class ESSearch():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    def search(self, keyword):
        es_data = es.search(index="tweet", size=2000, body={"query": {"match": {'text':{'query': keyword}}}})
        es_results = es_data['hits']['hits']
        tweets = []
        for es_result in es_results:
            tweets.append(es_result["_source"])
        tweets_of_keyword = {keyword: tweets}
        return tweets_of_keyword
