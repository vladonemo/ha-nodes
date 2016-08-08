#!/bin/bash

if [ ! -a /var/run/pigpio.pid ]
  then
    echo "pigpiod running"
  else
    pigpiod
fi

(echo $BASHPID > /tmp/sensors_tah.pid
sudo sh -c 'python /home/pi/ha-nodes/raspberry/TemeperatureAndHumidityObserver.py > /home/pi/ha-nodes/log/tah.log' ) &
(echo $BASHPID > /tmp/sensors_m.pid
sudo sh -c 'python3 /home/pi/ha-nodes/raspberry/MotionSensorObserver.py > /home/pi/ha-nodes/log/motion.log') &
