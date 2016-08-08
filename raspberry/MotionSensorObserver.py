#!/usr/bin/env python3

import signal
import sys
import node
import MotionSensor

class MotionSensorObserver(node.MqttNode):
    def __init__(self):
        super().__init__("office/motion")
        signal.signal(signal.SIGINT, self.signal_handler)
        self.sensor = MotionSensor.MotionSensor(25)
        
    def signal_handler(self, signal, frame):
        sys.exit(0)

    def motionOn(self):
        print("Motion detected")
        super().publish("True")

    def motionOff(self):
        print("Motion gone")
        super().publish("False")
  
    def observe(self):
        self.sensor.start(self.motionOn, self.motionOff)

   
print('Pres CTRL+C to stop')

observer = MotionSensorObserver()
observer.observe()
