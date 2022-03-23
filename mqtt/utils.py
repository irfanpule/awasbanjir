from paho.mqtt import client as mqtt_client
from django.core.exceptions import ValidationError
from mqtt.models import MQTTBroker


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker! ")
        else:
            print("Failed to connect, return code %d\n", rc)
    broker_server = MQTTBroker.get_config()
    if not broker_server:
        raise ValidationError("Broker server not set")

    client = mqtt_client.Client()
    client.username_pw_set(broker_server.username, broker_server.password)
    client.on_connect = on_connect
    client.connect(broker_server.broker, broker_server.port)
    return client
