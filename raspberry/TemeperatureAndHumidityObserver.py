#!/usr/bin/env python

import sys
import Adafruit_DHT
import signal
import time 
import node
import logging

class Observer():
    sensor = Adafruit_DHT.DHT11 #if not using DHT22, replace with Adafruit_DHT.DHT11 or Adafruit_DHT.AM2302
    pinNum = 4  #if not using pin number 4, change here
    lastHumidity = 0
    lastTemperature = 0
    timerInMinutes = 2

    def __init__(self):
        self.tempNode = node.MqttNode("office/temperature")
        self.humidNode = node.MqttNode("office/humidity")
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        sys.exit(0)

    def readAndPublish(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pinNum) #read_retry - retry getting temperatures for 15 times

        if humidity is not None:
            if humidity == self.lastHumidity:
                logging.log("Humidity no change {0:0.1f}%".format(humidity))
            else:
                logging.log("Humidity changed {0:0.1f}% - {1:0.1f}%".format(self.lastHumidity, humidity))
            self.humidNode.publish(humidity)
            self.lastHumidity = humidity

        else:
            logging.log("Failed to read humidity. Trying again")

        if temperature is not None:
            if temperature == self.lastTemperature:
                logging.log("Temperature no change {0:0.1f} C".format(temperature))
            else:
                logging.log("Temperature changed {0:0.1f} C - {1:0.1f} C".format(self.lastTemperature, temperature))
            self.tempNode.publish(temperature)
            self.lastTemperature = temperature

        else:
            logging.log("Failed to read temperature. Trying again.")
    
    def observe(self):
        while (True):
            self.readAndPublish()
            time.sleep(self.timerInMinutes*60)

observer = Observer()
observer.observe()
