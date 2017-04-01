import threading, logging, time
from kafka import KafkaConsumer
from kafka import TopicPartition

consumer = KafkaConsumer("twitterstream",max_poll_records=10)

msg = consumer.poll(timeout_ms=2000)
print str(msg)