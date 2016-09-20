#!/usr/bin/env python

import sys
import signal
import time 
import node
import logging
import RPi.GPIO as GPIO

class Observer():
    pinNum = 17
    timerInMinutes = 2

    def __init__(self):
        # Tell the GPIO library to use
        # Broadcom GPIO references
        GPIO.setmode(GPIO.BCM)
        self.node = node.MqttNode("office/lightIntensity")
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        GPIO.cleanup()
        sys.exit(0)

    def GetLightIntensity(self):
        measurement = 0
        # Discharge capacitor
        GPIO.setup(self.pinNum, GPIO.OUT)
        GPIO.output(self.pinNum, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(self.pinNum, GPIO.IN)
        # Count loops until voltage across
        # capacitor reads high on GPIO
        while (GPIO.input(self.pinNum) == GPIO.LOW):
            measurement += 1
        return measurement

    def readAndPublish(self):
        intensity = self.GetLightIntensity()
        logging.log("Light intensity is {0}".format(intensity))
        self.node.publish(intensity)
    
    def observe(self):
        while (True):
            self.readAndPublish()
            time.sleep(self.timerInMinutes*60)

observer = Observer()
observer.observe()
