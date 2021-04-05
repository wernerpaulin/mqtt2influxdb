#https://docs.docker.com/engine/reference/builder/
#docker build --rm -t mqtt2influxdb:1.0.0 .
#docker save -o mqtt2influxdb-1-0-0.tar mqtt2influxdb:1.0.0
#docker run -d --rm --network host -e MQTT_BROKER_IP=192.168.1.100 -e MQTT_BROKER_PORT=1883 --name mqtt2influxdb-app mqtt2influxdb-img
#docker logs mqtt2influxdb-app
#docker container stop mqtt2influxdb-app



FROM python:3-alpine

ADD . /
ADD main.py /

RUN pip3 install influxdb-client
RUN pip3 install paho-mqtt


#start python with unbuffered output option to see print outputs in docker log
CMD [ "python", "-u", "main.py" ]