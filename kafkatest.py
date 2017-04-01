import threading, logging, time
from kafka import KafkaConsumer
from kafka import TopicPartition

consumer = KafkaConsumer("twitterstream",max_poll_records=10,auto_offset_reset='earliest', enable_auto_commit=False)
msg = consumer.poll(timeout_ms=2000)
print len(msg.values()[0])