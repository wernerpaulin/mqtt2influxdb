#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
import influxdb_client
#from influxdb_client.client.write_api import SYNCHRONOUS
#from influxdb_client import InfluxDBClient, Point, WritePrecision
#pip install influxdb-client

from helper.env_support import initializeENV
from helper.mqtt_scanner import mqttScanner



"""
Connects to Influx on port, etc. unless specified with ENV

Creates DB if not exists


"""

#check for environmental variables in case this app is started in a docker container
MQTT_BROKER_IP = initializeENV("MQTT_BROKER_IP", "localhost")
MQTT_BROKER_PORT = initializeENV("MQTT_BROKER_PORT", 1883)
MQTT_BROKER_KEEPALIVE = initializeENV("MQTT_BROKER_KEEPALIVE", 60)

INFLUXDB_HOST = initializeENV("INFLUXDB_HOST", "localhost")
INFLUXDB_PORT = initializeENV("INFLUXDB_PORT", 8086)
INFLUXDB_USERNAME = initializeENV("INFLUXDB_USERNAME", "mqtt2influx_app")
INFLUXDB_PASSWORD = initializeENV("INFLUXDB_PASSWORD", "X!rA69c6BqnnMDat")
INFLUXDB_BUCKET = initializeENV("INFLUXDB_BUCKETNAME", "mqtt_data")
INFLUXDB_TOKEN = initializeENV("INFLUXDB_TOKEN", "UnNoUKqtepQSg5ipNQNEGHTMnDFw1UlnDKeJMIQTm5hF7mOgokgBVWxygnbkLQTn6mtLN6g_uFMHOHG-Uv88-g==")

#connect to InfluxDB time series database
#influxdb_client = InfluxDBClient(INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_USERNAME, INFLUXDB_PASSWORD, None)
#influxdb_client = InfluxDBClient(url="http://localhost:8086", token=INFLUXDB_TOKEN)
#write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "KhCvDVWND4uVc7Qb0MrCLIdggL-fIjMdEik7pc9yChaq9HZIPYJTzK2tL1r6HCExaCynaWi_JKIJoiXFAu2RGg=="
org = "Lenze"
bucket = "mqtt_data"

client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)

def OnMessageReceivedMQTT(topic, payload):
    #print("OnMessageMQTT: Topic <{0}> received with payload {1}".format(topic, payload))
    #https://github.com/Nilhcem/home-monitoring-grafana/blob/master/02-bridge/main.py

    write_api = client.write_api(write_options=SYNCHRONOUS)
    #assume data is sent as JSON string: "{"actVelocity":"0.0"}"
    try:
        jsonObj = json.loads(payload)
        #map json key values directly to class instance
        for key in jsonObj:
            #print( "JSON Object: key: {0}, value: {1}".format(key, jsonObj[key]) )
            #topic                        ...topic
            #key                          ...key / variable
            #jsonObj[key]                 ...value
            p = Point("mqtt_scanner").tag("topic", topic).field(key, float(jsonObj[key])).time(datetime.now(), WritePrecision.MS)
            write_api.write(bucket=INFLUXDB_BUCKET, org=org, record=p)

    #ok, obviously not a JSON object (the "Pythonic" philosophy for this kind of situation is called EAFP, for Easier to Ask for Forgiveness than Permission.)
    except Exception as e:
        p = Point("mqtt_scanner").tag("topic", topic).field("payload", payload).time(datetime.now(), WritePrecision.MS)
        write_api.write(bucket=INFLUXDB_BUCKET, org=org, record=p)



def main():

    mqttScannerInstance = mqttScanner(brokerIP=MQTT_BROKER_IP, brokerPort=MQTT_BROKER_PORT, brokerKeepalive=MQTT_BROKER_KEEPALIVE, blocking=True, onMessageCallback=OnMessageReceivedMQTT)
    ### NO EXECUTION OF LINES BELOW BECAUSE MQTT IS CALLED BLOCKING ###


if __name__ == "__main__":
    print("Starting MQTT to InfluxDB...")
    main()