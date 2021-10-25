#!/usr/bin/python3

from array import array
import Adafruit_DHT # Import a (probably proprietary) deprecated library https://github.com/adafruit/Adafruit_Python_DHT
import requests
import time
from struct import pack, unpack
import RPi.GPIO as GPIO

sleeptime = 5 # User configurable part # in seconds
samplecount = 3 # Samples per run
sensorpin = 4
reportunstable = True

f = open('config.ini', 'r') # Opening config.ini file
thingspeak_key = f.read()
f.close()

sensormodel = Adafruit_DHT.AM2302 # Importing sensor for DHT library

allsum_hum = 0.0 # Not sure if needed, just keeping that for safety
allsum_temp = 0.0

tolerance_hum = 20
tolerance_temp = 5

target_temp = 29
relay_pin = 11

def sample():
    global hum
    global temp
    hum, temp = Adafruit_DHT.read_retry(sensormodel, sensorpin) # Samples sensors and temporarely stores values in a float

    if hum is None or temp is None:
        mf = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'failed to get reading'}) # In case of a measuring failure sends failed to get reading

for x in range(samplecount):
    sample()
    allsum_hum = allsum_hum + hum # Adds all values to sums, later used to calculate the avarage, too bored to do it with an array
    allsum_temp = allsum_temp + temp
    if (x != samplecount): # In case of the last measurement no delay is needed
        time.sleep(sleeptime)

hum = allsum_hum / samplecount# Calculating avarages
temp = allsum_temp /samplecount
try:
    with open('.last', 'rb') as file:
        packed = file.read()
        array = unpack('d' * (len(packed) // 8), packed) # 8 bytes per double
        file.close()
except FileNotFoundError:
    array = [0,0]
    with open('.last', 'wb') as file:
        file.write(pack('d' * len(array) , *array))
        file.close()

if (abs(array[0] - hum) > tolerance_hum or abs(array[1] - temp) > tolerance_temp):
    if (reportunstable):
        mf = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'Reading unstable'})
    for x in range(samplecount * 5):
        sample()
    allsum_hum = allsum_hum + hum # Adds all values to sums, later used to calculate the avarage, too bored to do it with an array
    allsum_temp = allsum_temp + temp
    if (x != (samplecount * 5)): # In case of the last measurement no delay is needed
        time.sleep(sleeptime / 10)

    hum = allsum_hum / (samplecount * 5)  # Calculating avarages
    temp = allsum_temp /(samplecount * 5)

array = [hum, temp] # Store value
with open('.last', 'wb') as file:
    file.write(pack('d' * len(array) , *array))
    file.close()

r = requests.post('https://api.thingspeak.com/update?', data = {'api_key':thingspeak_key, 'field1':temp, 'field2':hum}) # Finally sending the data

GPIO.setmode(GPIO.board)
GPIO.setup(relay_pin, GPIO.OUT)

if (temp < target_temp):
    GPIO.output(relay_pin, GPIO.LOW)
elif (temp > target_temp):
    GPIO.output(relay_pin, GPIO.HIGH)