#!/bin/sh -e

echo "ativando venv" > /home/pi/Desktop/monitor.log
bash -c 'source /home/pi/Desktop/camera-monitor/venv/bin/activate'
echo "venv ativada" > /home/pi/Desktop/monitor.log

echo "iniciando main_detector.py" > /home/pi/Desktop/monitor.log
bash -c 'python3 /home/pi/Desktop/camera-monitor/main_detector.py' &
echo "main_detector.py iniciado" > /home/pi/Desktop/monitor.log

echo "iniciando main_monitor.py" > /home/pi/Desktop/monitor.log
bash -c 'python3 /home/pi/Desktop/camera-monitor/main_monitor.py' &
echo "main_monitor.py iniciado" > /home/pi/Desktop/monitor.log

exit 0