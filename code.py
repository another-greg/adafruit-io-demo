# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# adapted by Greg Hainline - UCSD MAE dept

# adafruit_circuitpython_adafruitio usage with an esp32
from os import getenv

import adafruit_connection_manager
import adafruit_requests
import wifi
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from microcontroller import watchdog as w
from watchdog import WatchDogMode
from supervisor import reload

from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

def get_board_pin(name):
    try:
        return getattr(board, name)
    except AttributeError:
        raise ValueError(f"Invalid pin name in settings.toml: {name}")

# Get WiFi details and Adafruit IO keys, ensure these are setup in settings.toml
# (visit io.adafruit.com if you need to create an account, or if you need your Adafruit IO key.)
ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")
aio_username = getenv("ADAFRUIT_AIO_USERNAME")
aio_key = getenv("ADAFRUIT_AIO_KEY")
primary_feed_name = getenv("ADAFRUIT_AIO_FEED")
publish_rate = getenv("ADAFRUIT_IO_PUBLISH_RATE_SECONDS")

# setup watchdog timer so things don't go off in the weeds
w.timeout = getenv("WATCHDOG_MAXTIME_SECONDS")
# reset the microcontroller if watchdog expires
w.mode = WatchDogMode.RESET
w.feed() # we now have 90 seconds to hit next feed before mcu resets

# setup board LEDs to provide heartbeat when connected
led1 = DigitalInOut(get_board_pin(getenv("BOARD_LED1")))
led1.direction = Direction.OUTPUT
led1.value = True # set LED to on, no heartbeat until connected.

# many boards don't have a second LED- try and handle this nicely
try:
    led2 = DigitalInOut(get_board_pin(getenv("BOARD_LED2")))
    led2.direction = Direction.OUTPUT
    led2.value = True
except ValueError:
    led2 = None
    pass

# Connect to WiFi
print(f"Connecting to {getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(getenv("CIRCUITPY_WIFI_SSID"), getenv("CIRCUITPY_WIFI_PASSWORD"))
print("Connected!")

led1.value = False

# Initialize a requests session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)

try:
    # Get the 'primary feed' feed from Adafruit IO
    primary_feed = io.get_feed(primary_feed_name)
except AdafruitIO_RequestError:
    # If primary feed can't be found, raise error
    raise(Exception(f"Feed {primary_feed_name} not found"))

# Below is an example of manually publishing a new  value to Adafruit IO.
# sleep on connect to prevent a bootloop from spamming the feed
time.sleep(10) 
last = 0
print(f"Publishing a new message every {publish_rate} seconds...")
while True:
    try:
        # Send a new message every {publish_rate} seconds.
        if (time.monotonic() - last) >= publish_rate:
            value = wifi.radio.ap_info.rssi

            print(f"Publishing {value} to {primary_feed_name}.")
            io.send_data(primary_feed_name, value)
            last = time.monotonic()
            w.feed() # feed the watchdog
        
        # heartbeat the LED(s) every 2 seconds
        if (int(time.monotonic() - last)%2 == 0):
            led1.value = not led1.value
            if led2:
                led2.value = not led2.value
    except:
        pass # let it try again

reload() # we should never get here- if we do just reload code.py




