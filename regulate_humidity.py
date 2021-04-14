# DHT22
import adafruit_dht
from board import D2 # Data pin of DHT22 is soldered to Data2

# Kasa Smart Plug
import asyncio
from kasa import Discover

import time
import logging
import sys

# Configs
HUMIDITY_LOW = 93
HUMIDITY_HIGH = 98

logging.basicConfig(filename='/var/log/regulate_humidity/regulate_humidity.log',
                     format='%(asctime)s %(message)s', level=logging.INFO)

dht22 = adafruit_dht.DHT22(D2)
logging.debug('Found DHT22 device')
devices = asyncio.run(Discover.discover())

humidity = None
mush_device = None

for addr, device in devices.items():
    asyncio.run(device.update())
    if 'Mushroom' in device.alias:
        mush_device = device

if not mush_device:
    logging.error('Failed to find the Mushroom smart plug')
    dht22.exit()
    sys.exit(1)

logging.debug('Found Mushroom device')

attempts = 5
while attempts > 0:
    try:
        humidity = dht22.humidity
        break
    except RuntimeError:
        attempts -= 1
        time.sleep(2) # Can only read DHT22 every 2 seconds

if not humidity:
    logging.error('Failed to read humidity from the DHT22')
    dht22.exit()
    sys.exit(1)

if humidity <= HUMIDITY_LOW  and mush_device.is_off:
    logging.info('Humidity is %.2f. Turning mushroom plug on \\(^w^)/', humidity)
    asyncio.run(mush_device.turn_on())
elif humidity >= HUMIDITY_HIGH and mush_device.is_on:
    logging.info('Humidity is %.2f. Turning mushroom plug off /(-_-)\\', humidity)
    asyncio.run(mush_device.turn_off())
else:
    plug_status_str = 'on' if mush_device.is_on else 'off'
    logging.info('No action required. Humidity is %.2f and Mushroom plug is %s', humidity, plug_status_str)

dht22.exit()

