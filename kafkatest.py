import threading, logging, time
from kafka import KafkaConsumer
from kafka import TopicPartition

consumer = KafkaConsumer("twitterstream", group_id='my-group', max_poll_records=1, auto_offset_reset='earliest', enable_auto_commit=True)

msg = consumer.poll(timeout_ms=2000)
print msg
print len(msg.values()[0])
consumer.close(autocommit=True)