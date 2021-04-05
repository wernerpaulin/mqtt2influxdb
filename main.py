#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import paho.mqtt.client as mqtt 
from influxdb import InfluxDBClient
#pip3 install paho-mqtt
#pip3 install influxdb-client

from helper.env_support import initializeENV


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
INFLUXDB_PASSWORD = initializeENV("INFLUXDB_USERNAME", "X!rA69c6BqnnMDat")
INFLUXDB_BUCKET = initializeENV("INFLUXDB_BUCKETNAME", "app_mon")
INFLUXDB_RP_DURATION = initializeENV("INFLUXDB_RP_DURATION", "1d")



def InitializeInfluxDB():
    #connect to InfluxDB time series database
    influxdb_client = InfluxDBClient(INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
    
    #create bucket (database + retention policy)
    databaseList = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_BUCKET, databaseList))) == 0:
        influxdb_client.create_database(INFLUXDB_BUCKET)
        influxdb_client.create_retention_policy('monitoring_ret_policy', INFLUXDB_RP_DURATION, default=True)
    
    influxdb_client.switch_database(INFLUXDB_BUCKET)


def main():
    InitializeInfluxDB()

if __name__ == "__main__":
    print("Starting MQTT to InfluxDB...")
    main()