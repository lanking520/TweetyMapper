from elasticsearch import Elasticsearch
import json
import time
import math
import requests


class ESSearch():
	def __init__(self):
		self.es = Elasticsearch(['https://search-tweetymapper-6vgtkoygmxpi7j6zlz35qmddjy.us-east-1.es.amazonaws.com',])

	def search(self, keyword):
		es_data = self.es.search(index="tweet", size=2000, body={"query": {"match": {'text':{'query': keyword}}}})
		es_results = es_data['hits']['hits']
		tweets = []
		for es_result in es_results:
			tweets.append(es_result["_source"])
		tweets_of_keyword = {keyword: tweets}
		return tweets_of_keyword

	def draftsearch(self, wordlist,filters=None):
		tweets = []
		for key in wordlist:
			data = self.es.search(index="tweet", size=2000, body={"query": {"match": {'text':{'query': key}}}})
			data = data['hits']['hits']
			for part in data:
				if filters:
					Latlgn = part["_source"]['coordinates']
					if math.pow(filters[0]-Latlgn[0],2)+math.pow(filters[1]-Latlgn[1],2) < 0.5:
						tweets.append({"position":part["_source"]['coordinates'],"text":part["_source"]['text'],"sentiment":part["_source"]['sentiment']})
				else:
					tweets.append({"position":part["_source"]['coordinates'],"text":part["_source"]['text'],"sentiment":part["_source"]['sentiment']})
		return {"result":tweets}

	def upload(self, data):
		self.es.index(index='tweet', doc_type='tweet_data', body=json.loads(json.dumps(data)))

