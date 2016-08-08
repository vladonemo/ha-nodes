#!/usr/bin/env python3

import time
import pigpio

class MotionSensor:

	def __init__(self, pin):
                self.pi = pigpio.pi()
                self.pin = pin
		#self.pi.set_mode(self.Data, pigpio.INPUT)
	
	def __del__(self):
		self.pi.stop()
		self.pi = None

	def start(self, callback_rising, callback_falling):
		sent_rising = False
		sent_falling = False
		while True:
			motion = self.pi.read(self.pin)
			if motion and not sent_rising:
				sent_rising = True
				sent_falling = False
				callback_rising()
			if not motion and not sent_falling:
				sent_falling = True
				sent_rising = False
				callback_falling()
			time.sleep(1)
