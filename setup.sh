#! /bin/sh

if [ $(id -u) != "0" ]; then
echo "You must be the superuser to run this script" >&2
exit 1
fi

sudo pip3 install Adafruit_DHT
sudo echo "
0,30 * * * *  python3" pwd >> /tmp/cron*/crontab