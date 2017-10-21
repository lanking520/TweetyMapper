# TwittMap
Qing Lan and Xiyan Liu

HW Group 18
![alt text](https://github.com/lanking520/TweetyMapper/raw/master/Demo.png)
### Note
Click [TweetyMapper](http://lanking520.github.io/TweetyMapper) to go to our Web App

Deployed on Elastic Beanstalk, built on Flask web framework. 

Using IBM-Watson API to Predict Sentiment of the Tweets.

Using Kafka/SQS with SNS to update tweets.

Tweets are streamed using Twitter Streaming API via Tweepy.

Search Pre-defined words from the drop-down menu. You can also manually type in to search.

Accept Multiple words search. Remove them by clicking tags

Pre-defined keywords: movie, commercial, car, music, food, sport, party, war, hello

Display of results may take seconds (due to t2.micro hardware limitation)

Markers are shown for each tweet. They are clustered when zoomed out.

User can click on markers to see details of tweets.
