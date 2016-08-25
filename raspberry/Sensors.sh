#!/bin/bash

if [ -a /var/run/pigpio.pid ]
  then
    echo "pigpiod running"
  else
    pigpiod
fi

mkdir -p /home/pi/log/sensors/

(echo $BASHPID > /tmp/sensors_tah.pid
sudo python /home/pi/ha-nodes/raspberry/TemeperatureAndHumidityObserver.py > /home/pi/log/sensors/tah.log ) &
(echo $BASHPID > /tmp/sensors_m.pid
sudo python3 /home/pi/ha-nodes/raspberry/MotionSensorObserver.py > /home/pi/log/sensors/motion.log) &
