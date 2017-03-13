from elasticsearch import Elasticsearch
import json
import time
import requests

#es = Elasticsearch([{'host': 'somehost.es.amazonaws.com', 'port': 80}])

#let's iterate over swapi people documents and index them

class ESSearch():
	def __init__(self, host = 'localhost', port=9200):
		self.es = Elasticsearch(['https://search-tweetymapper-6vgtkoygmxpi7j6zlz35qmddjy.us-east-1.es.amazonaws.com/',])

	def search(self, keyword):
		es_data = self.es.search(index="tweet", size=2000, body={"query": {"match": {'text':{'query': keyword}}}})
		es_results = es_data['hits']['hits']
		tweets = []
		for es_result in es_results:
			tweets.append(es_result["_source"])
		tweets_of_keyword = {keyword: tweets}
		return tweets_of_keyword

	def draftsearch(self, wordlist):
		tweets = []
		for key in wordlist:
			data = self.es.search(index="tweet", size=2000, body={"query": {"match": {'text':{'query': key}}}})
			data = data['hits']['hits']
			for part in data:
				tweets.append({"position":part["_source"]['coordinates'],"text":part["_source"]['text']})
		return tweets

if __name__ == "__main__":
	data = ESSearch()
	while True:
		print json.dumps(data.draftsearch(["music"]))
		print ""
		time.sleep(1)
