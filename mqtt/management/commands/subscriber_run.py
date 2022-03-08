import json

from paho.mqtt import client as mqtt_client
from django.core.management.base import BaseCommand
from api.serializers import DataSeriesSerializer
from perangkat.models import Perangkat


broker = 'test.mosquitto.org'
port = 1883
topic = "python/mqtt"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! ")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data_str = msg.payload.decode()
        data_dict = json.loads(data_str)
        print(f"Received `{data_str}` from `{msg.topic}` topic")
        serializer = DataSeriesSerializer(data=data_dict)
        if serializer.is_valid():
            print("valid")
            perangkat = Perangkat.objects.filter(device_id=data_dict['device_id']).first()
            if perangkat:
                data_series = serializer.save(perangkat=perangkat)
                data_series.set_status()
                print("berhasil simpen data")
            else:
                print("gak ada perangkat")
        else:
            print("data not valid")

    client.subscribe(topic, qos=1)
    client.on_message = on_message


class Command(BaseCommand):
    help = "Start to listen topic subscription"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('listen topic start'))
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
