import json
import asyncio

from paho.mqtt import client as mqtt_client
from json.decoder import JSONDecodeError

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from api.serializers import DataSeriesSerializer
from perangkat.models import Perangkat
from warga.models import Warga
from mqtt.utils import connect_mqtt
from awasbanjir import notifications


TOPIC = settings.TOPICS["received_data"]


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
            except ValidationError:
                perangkat = None
                print("UUID tidak ditemukan")

            if perangkat:
                data_series = serializer.save(perangkat=perangkat)
                data_series.set_status()
                status = get_device_cache(data_dict['device_id'], data_series.status)
                print(status, data_series.status)
                if status != data_series.status:
                    print("kirim notif ", data_series.get_status_display())
                    cache.set(data_dict['device_id'], data_series.status)
                    if settings.NOTIFICATION_ON:
                        for warga in Warga.objects.all():
                            n = notifications.send_telegram_personal(
                                warga.no_hp, f"Awas Banjir!, status {data_series.get_status_display()}")
                            asyncio.run(n)
            else:
                print("gak ada perangkat")
        else:
            print("data not valid")

    client.subscribe(TOPIC, qos=1)
    client.on_message = on_message


class Command(BaseCommand):
    help = "Start to listen topic subscription"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('listen topic start'))
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
