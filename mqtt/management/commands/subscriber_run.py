import json
import asyncio

from paho.mqtt import client as mqtt_client
from json.decoder import JSONDecodeError

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from api.serializers import DataSeriesSerializer
from perangkat.models import Perangkat
from warga.models import Warga
from awasbanjir import notifications


broker = 'broker.emqx.io'
port = 1883
topic = "awas_banjir_bagelen"
username = 'nanonoa'
password = 'best'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! ")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def get_device_cache(device_id, set_status):
        status = cache.get(device_id)
        if not status:
            cache.set(device_id, set_status)
            status = set_status
        return status

    def on_message(client, userdata, msg):
        try:
            data_str = msg.payload.decode()
            data_dict = json.loads(data_str)
            print(f"Received `{data_str}` from `{msg.topic}` topic")
        except JSONDecodeError:
            print(msg.payload)
            return

        serializer = DataSeriesSerializer(data=data_dict)
        if serializer.is_valid():
            try:
                perangkat = Perangkat.objects.filter(device_id=data_dict['device_id']).first()
                if perangkat:
                    data_series = serializer.save(perangkat=perangkat)
                    data_series.set_status()
                    status = get_device_cache(data_dict['device_id'], data_series.status)
                    print(status, data_series.status)
                    if status != data_series.status:
                        print("kirim notif ", data_series.get_status_display())
                        cache.set(data_dict['device_id'], data_series.status)
                        for warga in Warga.objects.all():
                            n = notifications.send_telegram_personal(
                                warga.no_hp, f"Awas Banjir!, status {data_series.get_status_display()}")
                            asyncio.run(n)
                else:
                    print("gak ada perangkat")
            except ValidationError:
                print("UUID tidak ditemukan")

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
