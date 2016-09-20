#!/bin/bash

if [ -a /var/run/pigpio.pid ]
  then
    echo "pigpiod running"
  else
    pigpiod
fi

mkdir -p /home/pi/log/sensors/

(sudo python /home/pi/ha-nodes/raspberry/TemeperatureAndHumidityObserver.py > /home/pi/log/sensors/tah.log ) &
(sudo python3 /home/pi/ha-nodes/raspberry/MotionSensorObserver.py > /home/pi/log/sensors/motion.log) &
(sudo python /home/pi/ha-nodes/raspberry/LightIntensityObserver.py > /home/pi/log/sensors/light.log) &
