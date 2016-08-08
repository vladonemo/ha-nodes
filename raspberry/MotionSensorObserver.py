#!/usr/bin/env python3

import signal
import sys
import node
import MotionSensor
import logging

class MotionSensorObserver():
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.sensor = MotionSensor.MotionSensor(25)
        self.node = node.MqttNode("office/motion")
        
    def signal_handler(self, signal, frame):
        sys.exit(0)

    def motionOn(self):
        logging.log("Motion detected")
        self.node.publish("True")

    def motionOff(self):
        logging.log("Motion gone")
        self.node.publish("False")
  
    def observe(self):
        self.sensor.start(self.motionOn, self.motionOff)

observer = MotionSensorObserver()
observer.observe()
