# adafruit-io-demo
A simple example for using adafruit IO on an esp32 microcontroller running CircuitPython. I found the adafruit examples a little too clunky.


## Quickstart
This example assumes you have already created a [feed](https://learn.adafruit.com/adafruit-io-basics-feeds/overview) on adafruitIO and you specify that feed in your settings.toml file.

In settings.toml, simply configure your wifi network, password, adafruit-io username, api-key, and the name of the feed you've created. The example _code.py_ file publishes the RSSI signal strength of the microcontroller every 60 seconds to the feed.

```toml
# settings.toml

# wifi settings
CIRCUITPY_WIFI_SSID = "Your-WiFi-Network-Here"
CIRCUITPY_WIFI_PASSWORD = "Your-WiFi-Password-Here"

# Adafruit IO
ADAFRUIT_AIO_USERNAME = "your-adafruit-io-username here"
ADAFRUIT_AIO_KEY      = "your-adafruit-io-api-key-here"
ADAFRUIT_AIO_FEED     = "name-of-the-feed-you-want-to-publish-to"
ADAFRUIT_IO_PUBLISH_RATE_SECONDS = 60

# Watchdog settings
WATCHDOG_MAXTIME_SECONDS = 90

# LEDs
BOARD_LED1 = "your-board-led-pin1-here"
# BOARD_LED2 = "your-board-led-pin2-here" # if your board has multiple LED pins
```
Just update your _settings.toml_ file and load your code onto your microcontroller. Refer to _include.txt_ for what libraries need to be added to your microcontroller's _/lib_ folder.

## What is adafruitIO?
Adafruit IO is a cloud service hosted by Adafruit that enables sending data to/from internet of things (IoT) devices. AdafruitIO has 2 APIs that enable sending data to/from your microcontroller. You can send data to feeds from your microcontroller, or monitor feeds from your microcontroller and trigger actions based off of specific feed values or value changes.
### The APIs
An API, or application programming interface, enables you to communicate with their application (AdafruitIO) from your device/code using standardized network communication protocols. Adafruit offers an API for HTTP and an API for MQTT. There are some differences in the capabilities of each, and I'd recommend reading [this summary] of the differences. If your goal is to just get your feet wet with interacting with APIs and web services, I'd recommend using the HTTP api. If your goal is to develop more experience with IoT specifically, I'd recommend using the MQTT api.

[__AdafruitIO HTTP API__](https://docs.circuitpython.org/projects/adafruitio/en/latest/api.html#adafruit_io.adafruit_io.IO_HTTP): 

Adafruit offers a [REST API](https://www.geeksforgeeks.org/node-js/rest-api-introduction/) for http communication. REST APIs are broadly similar to one another. 

[__AdafruitIO MQTT API__](https://docs.circuitpython.org/projects/adafruitio/en/latest/api.html#adafruit_io.adafruit_io.IO_MQTT): 

[MQTT](https://learn.sparkfun.com/tutorials/introduction-to-mqtt/all) is better suited for IoT devices because it requires less overhead per message and offers [quality of service](https://www.geeksforgeeks.org/computer-networks/computer-network-quality-of-service-and-multimedia/) support for better controlling your traffic. These features make the code a little more confusing to follow in the beginning. 
