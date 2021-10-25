#! /bin/sh

if [ $(id -u) != "0" ]; then
echo "You must be the superuser to run this script" >&2
exit 1
fi

sudo apt-get update
sudo apt-get install build-essential python3-dev
sudo apt-get install python3-gpiozero
sudo pip3 install Adafruit_DHT

#going to also set up the automation