#!/usr/bin/python3

from array import array
import Adafruit_DHT # Import a (probably proprietary) deprecated library https://github.com/adafruit/Adafruit_Python_DHT
import requests
import time
from struct import pack, unpack
import RPi.GPIO as GPIO

sensorpin = 4
reportunstable = False

f = open('config.ini', 'r') # Opening config.ini file
thingspeak_key = f.read()
f.close()

sensormodel = Adafruit_DHT.AM2302 # Importing sensor for DHT library

hum = 0
temp = 0

target_temp = 29
relay_pin = 11

def sample():
    # global hum
    # global temp
    hum, temp = Adafruit_DHT.read_retry(sensormodel, sensorpin) # Samples sensors and temporarely stores values in a float

    if hum is None or temp is None:
        mf = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'failed to get reading'}) # In case of a measuring failure sends failed to get reading

    return hum, temp

sample()
r = requests.post('https://api.thingspeak.com/update?', data = {'api_key':thingspeak_key, 'field1':temp, 'field2':hum}) # Finally sending the data

GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_pin, GPIO.OUT)

if (temp < target_temp):
    GPIO.output(relay_pin, GPIO.LOW)
elif (temp > target_temp):
    GPIO.output(relay_pin, GPIO.HIGH)