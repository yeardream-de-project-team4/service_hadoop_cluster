import os
import json

from kafka import KafkaConsumer
from minio import Minio
from hdfs import InsecureClient

from consumer_file import callback_file


class MessageConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=os.getenv("KAFKA_BROKERS").split(","),
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            group_id=os.getenv("KAFKA_CONSUMER_GROUP"),
            enable_auto_commit=True,
        )
        self.events = {}
        self.minio = Minio(
            os.getenv("MINIO_HOST"),
            os.getenv("MINIO_USER"),
            os.getenv("MINIO_PASSWORD"),
            secure=False,
        )
        self.hdfs = InsecureClient("http://namenode:9870", user="root")

    def regist_event(self, topic, callback):
        self.events[topic] = callback

    def start(self):
        self.consumer.subscribe(list(self.events.keys()))
        for message in self.consumer:
            try:
                self.events[message.topic](message, self.minio, self.hdfs)
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    consumer = MessageConsumer()
    consumer.regist_event("flask-hadoop-file", callback_file)
    consumer.start()
