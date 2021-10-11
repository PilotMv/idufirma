#! /bin/sh

if [ $(id -u) != "0" ]; then
echo "You must be the superuser to run this script" >&2
exit 1
fi

sudo pip3 install Adafruit_DHT

#going to also set up the automation