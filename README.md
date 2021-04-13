# Regulate Humidity

Regulates the humidity of a mushroom farm plugged into a Kasa smart plug somewhere on the local wifi network.
Uses a DHT22 soldered to data pin 2 on a Raspberry Pi Zero W.

## Cron

Expects to be scheduled via cron to run every minute.

## Virtual Env

Use virtualenv and requirements.txt for dependencies.

## Logrotate

Logs to /var/log/regulate\_humdity.log. 
Install the logrotate/regulate\_humidity config file to /etc/logrotate.d/regulate\_humidity.
