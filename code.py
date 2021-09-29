#!/usr/bin/python3

import Adafruit_DHT
import requests
import time
import configparser

sensorpin = 4
sensorpin1 = 17
sensormodel = Adafruit_DHT.AM2302
config = configparser.ConfigParser()
config.read('config.ini')
thingspeak_key = config['keys']['thingy']

def sample():
    humsealing, tempsealing = Adafruit_DHT.read_retry(sensormodel, sensorpin)
    humout, tempout = Adafruit_DHT.read_retry(sensormodel, sensorpin1)

    if humsealing is None or tempsealing is None:
        mf = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'failed to get reading'})

    else:
        r = requests.post('https://api.thingspeak.com/update?', data = {'api_key':thingspeak_key, 'field1':tempsealing, 'field2':humsealing,'field3':tempout, 'field4':humout})

sample()
time. sleep(30)
sample()