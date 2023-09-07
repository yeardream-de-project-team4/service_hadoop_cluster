import os
import json
from kafka import KafkaConsumer
from minio import Minio
from hdfs import InsecureClient

# MinIO
minio_client = Minio(
    os.getenv("MINIO_HOST"),
    os.getenv("MINIO_USER"),
    os.getenv("MINIO_PASSWORD"),
    secure=False,
)

# HDFS
hdfs_client = InsecureClient("http://namenode:9870", user="root")

# Consumer
consumer = KafkaConsumer(
    bootstrap_servers=os.getenv("KAFKA_BROKERS").split(","),
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    group_id="consumer-load-hadoop",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)
consumer.subscribe(["topic-load-hadoop"])

for message in consumer:
    try:
        if "data_from_flask" not in hdfs_client.list("/"):
            hdfs_client.makedirs("/data_from_flask")
        data = message.value
        bucket, filename = data["bucket"], data["filename"]
        hdfs_path = f"/data_from_flask/{filename}"
        response = minio_client.get_object(bucket, filename)

        with hdfs_client.write(hdfs_path) as writer:
            for d in response.stream(32 * 1024):
                writer.write(d)
    except Exception:
        continue
