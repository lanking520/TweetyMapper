import tweepy
import json
from elasticsearch import Elasticsearch

#Variables that contains the user credentials to access Twitter API
consumer_key="ElLAEYVqoWEQ62CThiph88Q01"
consumer_secret="Zbh6Z9hK9wEIExaRXzFoJENaQy5bPm5TLnoVkavKcDdDgGKiOv"
access_token="887932914-U1gobak10He0VbMIVTcRUkQeLudpBybyuRx3zbAf"
access_token_secret="ZV7Iy5E4cMyzKN1SbWiFqKaeGOIkYDZmAH9oXAN3dnX4B"

class DataUploadStreamListener(tweepy.StreamListener):
    es = Elasticsearch(['https://search-tweetymapper-6vgtkoygmxpi7j6zlz35qmddjy.us-east-1.es.amazonaws.com/',])

    def on_status(self, status):
        try:
            self.process(status._json)
        except KeyError as e:
            print ("KeyError: ", e)

    def on_error(self, status_code, data):
        print ("Error: ", status_code, ": ", data)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
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
                self.es.index(index='tweet', doc_type='tweet_data', body=json.loads(json.dumps(tweet_dict)))
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
        except:
            continue
