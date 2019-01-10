#!/usr/bin/env python2
from hermes_python.hermes import Hermes

import json
import requests

import paho.mqtt.client as mqtt
# import requests

# MQTT client to connect to the bus
mqtt_client = mqtt.Client()
HOST = "raspi-master.local"
PORT = 1883
# WIKI_TOPICS = ['hermes/intent/NinjaPanda:SearchInWikipedia']
WIKI_TOPICS = ['hermes/intent/NinjaPanda:search']
WIKI_SEND_TOPICS = ['wiki/information']

# WIKIPEDIA API
WIKI_API_BASE_URL = "https://fr.wikipedia.org/w/api.php"
S = requests.Session()

# Subscribe to the important messages
def on_connect(client, userdata, flags, rc):
    print('Connected')
    for topic in WIKI_TOPICS:
        print(topic)
        mqtt_client.subscribe(topic)

# Process a message as it arrives
def on_message(client, userdata, msg):
	print('On message')
	print(msg.topic)
	intent_json = json.loads(msg.payload)
	input = intent_json['input']
	slots = intent_json['slots']
	val = processing(slots)
	result = searchInWiki(val)
	Hermes.publish_end_session(msg.session_id, result)


def processing(slots):
	value = ''
	for slot in slots:
		value += slot['value']['value'] + ' '
	return value

def searchInWiki(word):

	PARAMS = {
	    'action':"opensearch",
	    'search':word,
	    'limit': 5,
	    'namespace':0,
	    'format':"json"
	}

	R = S.get(url=WIKI_API_BASE_URL, params=PARAMS)
	DATA = R.json()

	print(DATA)


if __name__ == '__main__':
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(HOST, PORT)
    mqtt_client.loop_forever()
