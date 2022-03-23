from mqtt.utils import connect_mqtt


def publish(topic: str, msg: str):
    client = connect_mqtt()
    client.publish(topic, msg, qos=1)
