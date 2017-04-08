from watson_developer_cloud import AlchemyLanguageV1
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import boto3
import json

alchemy_api_key = "f2a40969214d57623993c2f998ef7bdf12d8062f"
AWS_ACCESS_KEY = "AKIAI3AUPHHLWCOUUKMA"
AWS_SECRET_KEY = "m0dj6LYIlPM1HJUm3dVCuwIZYnGiuO1I1ibFvhCy"

class SQSSNSWorkerPool:
    def __init__(self, num_threads=2):
    	self.sqs = boto3.client('sqs', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        self.queueUrl = self.sqs.get_queue_url(QueueName='tweetstream')['QueueUrl']

        self.alchemy_language = AlchemyLanguageV1(api_key=alchemy_api_key)

        self.sns = boto3.client('sns', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        self.topic_arn = self.sns.create_topic( Name='tweet')
        self.pool = ThreadPool(num_threads)

    def start(self):
        while True:
            messages = self.sqs.receive_message(QueueUrl=self.queueUrl, MaxNumberOfMessages=5, WaitTimeSeconds=20)
            # Add Handler for Empty Message Body
            print "Retrieved " + str(len(messages)) + " messages from sqs"
            self.pool.map(self.work, messages['Messages'])
            # Sleep for 1 second if the message body is empty

    def work(self, message):
        try:
            print "Worker: " + str(multiprocessing.dummy.current_process())
            data = json.loads(message.Body)
            tweet_text = data['text']
            sentiment = self.alchemy_language.sentiment(text=tweet_text)
            data['sentiment'] = sentiment['docSentiment']['type']
            print data['sentiment']
            self.sns.publish(TopicArn=self.topic_arn,Message=json.dumps(data))
        except Exception as e:
            print e
        finally:
            self.sqs.delete_message(QueueUrl=self.queueUrl, ReceiptHandle= message['ReceiptHandle'])

if __name__ == '__main__':
    workerPool = SQSSNSWorkerPool()
    workerPool.start()

