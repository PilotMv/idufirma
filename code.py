#!/usr/bin/python3

import Adafruit_DHT # https://github.com/adafruit/Adafruit_Python_DHT
import requests
import time

sleeptime = 30 # User configurable part # in seconds
samplecount = 3 # Samples per run
sensorpin = 4
sensorpin1 = 17

sensormodel = Adafruit_DHT.AM2302 # Importing sensor for DHT library

with open('config.ini', 'r') as file:
        global thingspeak_key 
        thingspeak_key = file.read()
        file.close()

def sample():
    global humsealing
    global tempsealing
    global humout
    global tempout
    humsealing, tempsealing = Adafruit_DHT.read_retry(sensormodel, sensorpin) # Samples sensors and temporarely stores values in a float
    humout, tempout = Adafruit_DHT.read_retry(sensormodel, sensorpin1)

    if humsealing is None or tempsealing is None:
        requests.post('https://api.thingspeak.com/update.json', data = {'api_key':thingspeak_key, 'status':'failed to get reading'}) # In case of a measuring failure sends failed to get reading



def main():
    # allsum_humsealing = 0.0 # Not sure if needed, just keeping that for safety
    # allsum_tempsealing = 0.0
    # allsum_humout = 0.0
    # allsum_tempout = 0.0

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

    requests.post('https://api.thingspeak.com/update?', data = {'api_key':thingspeak_key, 'field1':tempsealing, 'field2':humsealing,'field3':tempout, 'field4':humout}) # Finally sending the data

if __name__ == '__main__':
    main()
