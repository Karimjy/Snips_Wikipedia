#!/usr/bin/env python2
from hermes_python.hermes import Hermes

import json

import paho.mqtt.client as mqtt
import requests

# MQTT client to connect to the bus
mqtt_client = mqtt.Client()
HOST = "localhost"
PORT = 1883
WIKI_TOPICS = ['hermes/intent/SeachWikipedia']
WIKI_SEND_TOPICS = ['wiki/information']

# WIKIPEDIA API
WIKI_API_BASE_URL = "https://fr.wikipedia.org/w/api.php"

# Subscribe to the important messages
def on_connect(client, userdata, flags, rc):
    for topic in WIKI_TOPICS:
        mqtt_client.subscribe(topic)

# Process a message as it arrives
def on_message(client, userdata, msg):
	print(msg.payload.input)
    # if msg.topic == 'hermes/intent/SeachWikipedia':
    #     print("Wakeword detected!")

if __name__ == '__main__':
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(HOST, PORT)
    mqtt_client.loop_forever()
