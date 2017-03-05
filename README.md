# TwittMap
Shuo Wang & Jisong Liu

### Note
Check twittmap-env.vvycwdvrkk.us-west-2.elasticbeanstalk.com

Deployed on Elastic Beanstalk, built on Flask web framework. Tweets are streamed using Twitter Streaming API via Tweepy.

Select keywords from keyword list or type a word to search (Pre-defined words only, other words will show "No results found")

Pre-defined keywords: movie, commercial, car, music, food, sport, party

Display of results may take seconds (due to t2.micro hardware limitation)

Markers are shown for each tweet. They are clustered when zoomed out.

User can click on markers to see details of tweets.
