import tweepy
import json
import boto3
import time

consumer_key="INPUT_KEY_HERE"
consumer_secret="INPUT_KEY_HERE"
access_token="INPUT_KEY_HERE"
access_token_secret="INPUT_KEY_HERE"
AWS_ACCESS_KEY = "INPUT_KEY_HERE"
AWS_SECRET_KEY = "INPUT_KEY_HERE"

class DataUploadStreamListener(tweepy.StreamListener):

    def __init__(self):
        super(DataUploadStreamListener, self).__init__()
        self.sqs = boto3.client('sqs', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        self.queueUrl = self.sqs.create_queue(QueueName='tweetstream')['QueueUrl']
        time.sleep(1)

    def on_status(self, status):
        try:
            self.process(status._json)
        except KeyError as e:
            print ("KeyError: ", e)

    def on_error(self, status_code, data):
        print ("Error: ", status_code, ": ", data)

        if status_code == 420: # Rate limited!
            return False

    def process(self, data):
        keywords = ["music", "food", "sport", "show", "movie", "car", "commercial", "party", "war", "hello"]
        content = data['text'].lower()
        #print("+++++")
        if any(x in content for x in keywords):
            if (data['coordinates'] is not None) and (('lang' not in data) or (data['lang']=='en')): # data[coordinates] may be null, want to filter it out
                # print("------")
                # print(data['text'])
                # print(data['coordinates'])
                # print(data['created_at'])
                # print(data['timestamp_ms'])
                # print(data['created_at'])
                # print(data['user']['name'])
                # print(data['user']['screen_name'])
                # print("------")
                print "Find a match " + data['timestamp_ms']
                tweet_dict = {'text': data['text'],
                             'coordinates': data['coordinates']['coordinates'],
                             'created_at': data['created_at'],
                             'timestamp_ms': data['timestamp_ms'],
                             'user_name': data['user']['name'],
                             'user_screen_name': data['user']['screen_name']}
                response = self.sqs.send_message(QueueUrl=self.queueUrl,MessageBody=json.dumps(tweet_dict))


if __name__ == '__main__':
    duStreamListener = DataUploadStreamListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    keywords = ["music", "food", "sport", "show", "movie", "car", "commercial", "party", "war", "hello"]
    locations = [-180,-90,180,90]
    while True:
        try:
            duStream = tweepy.Stream(auth, duStreamListener)
            duStream.filter(track=keywords, locations=locations)
        except Exception as e:
            print "Failed with " + str(e)
            continue




