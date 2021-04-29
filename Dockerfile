#https://docs.docker.com/engine/reference/builder/
#docker build --rm -t mqttscanner:1.0.0 .
#docker save -o mqttscanner-1-0-0.tar mqttscanner:1.0.0
#docker run -d --rm --network host -e MQTT_BROKER_IP=localhost -e MQTT_BROKER_PORT=1883 --name mqttscanner-app mqttscanner
#docker run -d --rm -p 8086:8086 -v influxdb2:/var/lib/influxdb2 influxdb:2.0.4-alpine
#docker run -d --rm -p 3000:3000 --name=grafana grafana/grafana:7.5.2

#docker logs mqttscanner-app
#docker container stop mqttscanner-app



FROM python:3-alpine

ADD . /
ADD main.py /

RUN pip3 install influxdb-client
RUN pip3 install paho-mqtt


#start python with unbuffered output option to see print outputs in docker log
CMD [ "python", "-u", "main.py" ]