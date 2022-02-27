#!/usr/bin/python3

import Adafruit_DHT # https://github.com/adafruit/Adafruit_Python_DHT
import requests

sensormodel = Adafruit_DHT.AM2302 # Importing sensor for DHT library

# User defined variables
communicationpins = [7, 15, 16, 20, 30]
temp_field_names = ['temp1', 'temp2', 'temp3', 'temp4', 'temp5']
hum_field_names = ['hum1', 'hum2', 'hum3', 'hum4', 'hum5']

with open('config.ini', 'r') as file:
        global thingspeak_key 
        thingspeak_key = file.read()
        file.close()

def get_sensor(compin):
    hum, temp = Adafruit_DHT.read_retry(sensormodel, compin)
    return temp, hum

def main():
    data = {'api_key':thingspeak_key}

    for i in range(len(communicationpins)):
        temp, hum = get_sensor(communicationpins[i])
        data[temp_field_names[i]] = temp
        data[hum_field_names[i]] = hum

    requests.post('https://api.thingspeak.com/update?', data)

if __name__ == '__main__':
    main()
