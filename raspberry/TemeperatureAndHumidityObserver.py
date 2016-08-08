import sys
import Adafruit_DHT

import signal
import time 
import datetime
import node

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
                print("Humidity hasn't changed from {0:0.1f} %".format(humidity))
            else:
                print("Humidity changed from {0:0.1f} % to {1:0.1f} %".format(self.lastHumidity, humidity))
            self.humidNode.publish(humidity)
            self.lastHumidity = humidity

        else:
            print("Failed to read humidity. Trying again")

        if temperature is not None:
            if temperature == self.lastTemperature:
                print("Temperature hasn't changed from {0:0.1f} C".format(temperature))
            else:
                print("Temperature changed from {0:0.1f} C to {1:0.1f} C".format(self.lastTemperature, temperature))
            self.tempNode.publish(temperature)
            self.lastTemperature = temperature

        else:
            print("Failed to read temperature. Trying again.")
    
    def observe(self):
        while (True):
            self.readAndPublish()
            time.sleep(self.timerInMinutes*60)

print('Pres CTRL+C to stop')

observer = Observer()
observer.observe()
