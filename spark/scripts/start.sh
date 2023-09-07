#!/bin/sh

# run jupyter server
nohup jupyter lab --port 7777 --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password='' --no-browser --allow-root &

# run spark history server
/opt/spark-3.4.1-bin-hadoop3/bin/spark-class org.apache.spark.deploy.history.HistoryServer

/usr/sbin/sshd -D