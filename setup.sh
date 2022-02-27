#!/bin/sh

if [ $(id -u) != "0" ]; then
    echo "You must be the superuser to run this script" >&2
    exit 1
fi

apt-get update
apt-get install build-essential python3-dev
apt-get install python3-gpiozero
apt-get install pip3 # currently only needed to install the Adafruit_DHT python library    

pip3 install Adafruit_DHT

BASEDIR=$(pwd $0)

# run crontab twice per hour
(crontab -l ; echo "0,30 * * * * python3 ${BASEDIR}/code.py")| crontab -
