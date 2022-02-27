# idufirma
Code to check and send sensor data from DHT sensors running on a Raspberry Pi

Dependencies:

    build-essential python3-dev python3-gpiozero pip3

Used libraries:

    Adafruit_DHT, requests, time, struct, array, RPi.GPIO
    
A config.ini file is also required to store the Thingyspeak key

Install the Adafruit_DHT library by running:

    sudo setup.sh

Install script creates a new command in crontab what can be accessed by: `sudo crontab -e`
