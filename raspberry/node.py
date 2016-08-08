import sys
import paho.mqtt.client as mqtt
from secrets import MQTT_USER
from secrets import MQTT_PASSWORD

class MqttNode:    
    def __init__(self, topic):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.client.connect("192.168.0.111", 1883)
        self.topic = topic

    def __del__(self):
        self.client.loop_stop
        self.client.disconnect()

    def publish(self, message):
        self.client.reconnect()
        self.client.publish(self.topic, message, qos=0)
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        print("CONNACK received with code %d." % (rc))

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected ... reconnecting")
        self.client.reconnect()
