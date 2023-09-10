def callback_file(message, minio, hdfs):
    if "data_from_flask" not in hdfs.list("/"):
        hdfs.makedirs("/data_from_flask")
    data = message.value
    bucket, filename = data["bucket"], data["filename"]
    hdfs_path = f"/data_from_flask/{filename}"
    response = minio.get_object(bucket, filename)

    with hdfs.write(hdfs_path) as writer:
        for d in response.stream(32 * 1024):
            writer.write(d)
