from watson_developer_cloud import AlchemyLanguageV1
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import boto3
import json
import time
from kafka import KafkaConsumer

alchemy_api_key = "INPUT_KEY_HERE"
AWS_ACCESS_KEY = "INPUT_KEY_HERE"
AWS_SECRET_KEY = "INPUT_KEY_HERE"

class KafkaSNSWorkerPool:
    def __init__(self, num_threads=2):
    	self.consumer = KafkaConsumer("twitterstream", group_id='my-group', max_poll_records=5, auto_offset_reset='earliest', enable_auto_commit=True, bootstrap_servers=['localhost:9092'])
        self.alchemy_language = AlchemyLanguageV1(api_key=alchemy_api_key)
        # sns_client = boto3.client('sns')
        # topic_arn = sns_client.create_topic( Name='tweet')

        # sns service 
        self.sns = boto3.client('sns', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        self.topic_arn = self.sns.create_topic(Name='tweet')['TopicArn']

        self.pool = ThreadPool(num_threads)

    def start(self):
        while True:
            messages = self.consumer.poll(timeout_ms=2000)
            try:
                messages = messages.values()[0]
                print "Retrieved " + str(len(messages)) + " messages from Kafka"
                self.pool.map(self.work, messages)
            except:
                print "No Messages..."
                time.sleep(1)
            # Sleep for 1 second if the message body is empty

    def work(self, message):
        try:
            print "Worker: " + str(multiprocessing.dummy.current_process())
            data = json.loads(message.value)
            tweet_text = data['text']
            sentiment = self.alchemy_language.sentiment(text=tweet_text)
            data['sentiment'] = sentiment['docSentiment']['type']
            print data['sentiment']
            self.sns.publish(TopicArn=self.topic_arn,Message=json.dumps(data))
        except Exception as e:
            print e


if __name__ == '__main__':
    workerPool = KafkaSNSWorkerPool()
    workerPool.start()

