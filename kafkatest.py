import threading, logging, time
from kafka import KafkaConsumer
from kafka import TopicPartition

<<<<<<< Updated upstream
consumer = KafkaConsumer("twitterstream", group_id='my-group', max_poll_records=5, auto_offset_reset='earliest', enable_auto_commit=True)

msg = consumer.poll(timeout_ms=2000)
print msg
print len(msg.values()[0])
consumer.close(autocommit=True)
=======
consumer = KafkaConsumer("twitterstream",max_poll_records=10,auto_offset_reset='earliest', enable_auto_commit=True)
msg = consumer.poll(timeout_ms=2000)
print len(msg.values()[0])
print msg
>>>>>>> Stashed changes
