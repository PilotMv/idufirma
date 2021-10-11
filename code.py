#!/usr/bin/python3

from array import array
import Adafruit_DHT # Import a (probably proprietary) deprecated library https://github.com/adafruit/Adafruit_Python_DHT
import requests
import time
from struct import pack, unpack

sleeptime = 30 # User configurable part # in seconds
samplecount = 3 # Samples per run
sensorpin = 4
sensorpin1 = 17
reportunstable = True

f = open('config.ini', 'r') # Opening config.ini file
thingspeak_key = f.read()
f.close()

sensormodel = Adafruit_DHT.AM2302 # Importing sensor for DHT library

allsum_humsealing = 0.0 # Not sure if needed, just keeping that for safety
allsum_tempsealing = 0.0
allsum_humout = 0.0
allsum_tempout = 0.0

tolerance_humout = 40
tolerance_humsealing = 20
tolerance_tempout = 10
tolerance_tempsealing = 5

def sample():
    global humsealing
    global tempsealing
    global humout
    global tempout
    humsealing, tempsealing = Adafruit_DHT.read_retry(sensormodel, sensorpin) # Samples sensors and temporarely stores values in a float
    humout, tempout = Adafruit_DHT.read_retry(sensormodel, sensorpin1)

    if humsealing is None or tempsealing is None:
        mf = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'failed to get reading'}) # In case of a measuring failure sends failed to get reading

for x in range(samplecount):
    sample()
    allsum_humout = allsum_humout + humout # Adds all values to sums, later used to calculate the avarage, too bored to do it with an array
    allsum_humsealing = allsum_humsealing + humsealing
    allsum_tempout = allsum_tempout + tempout
    allsum_tempsealing = allsum_tempsealing + tempsealing
    if (x != samplecount): # In case of the last measurement no delay is needed
        time.sleep(sleeptime)

humout = allsum_humout / samplecount # Calculating avarages
humsealing = allsum_humsealing / samplecount
tempout = allsum_tempout / samplecount
tempsealing = allsum_tempsealing /samplecount
try:
    with open('.last', 'rb') as file:
        packed = file.read()
        array = unpack('d' * (len(packed) // 8), packed) # 8 bytes per double
        file.close()
except FileNotFoundError:
    array = [0,0,0,0]
    with open('.last', 'wb') as file:
        file.write(pack('d' * len(array) , *array))
        file.close()

if (abs(array[0] - humout) > tolerance_humout or abs(array[1] - humsealing) > tolerance_humsealing or abs(array[2] - tempout) > tolerance_tempout or abs(array[3] - tempsealing) > tolerance_tempsealing):
    if (reportunstable):
        mf = requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'Reading unstable'})
    for x in range(samplecount * 5):
        sample()
    allsum_humout = allsum_humout + humout # Adds all values to sums, later used to calculate the avarage, too bored to do it with an array
    allsum_humsealing = allsum_humsealing + humsealing
    allsum_tempout = allsum_tempout + tempout
    allsum_tempsealing = allsum_tempsealing + tempsealing
    if (x != (samplecount * 5)): # In case of the last measurement no delay is needed
        time.sleep(sleeptime / 10)

    humout = allsum_humout / (samplecount * 5) # Calculating avarages
    humsealing = allsum_humsealing / (samplecount * 5)
    tempout = allsum_tempout / (samplecount * 5)
    tempsealing = allsum_tempsealing /(samplecount * 5)

array = [humout, humsealing, tempout, tempsealing] # Store value
with open('.last', 'wb') as file:
    file.write(pack('d' * len(array) , *array))
    file.close()

r = requests.post('https://api.thingspeak.com/update?', data = {'api_key':thingspeak_key, 'field1':tempsealing, 'field2':humsealing,'field3':tempout, 'field4':humout}) # Finally sending the data