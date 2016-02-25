#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import RPi.GPIO as GPIO
import time
import requests
import json

GREEN_PIN = 19
RED_PIN = 26
ALERT_PIN = 13
LOW_TEMP = 16.0
HIGH_TEMP = 20.0
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-*')[0]
device_file = device_folder + '/w1_slave'

api_key = '' #yeelink apykey
api_headers = {'U-ApiKey': api_key, 'content-type': 'application/json'}
device_id = 344760
sensor_id = 383360
api_url = r'http://api.yeelink.net/v1.0/device/%s/sensor/%s/datapoints' % (device_id, sensor_id)

def init_gpio():
    print('  初始化GPIO...')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
#    GPIO.setup(ALERT_PIN, GPIO.OUT)
#    GPIO.output(ALERT_PIN, GPIO.HIGH)

def init_drivers():
    print('  加载传感器驱动...')
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

def read_temp_raw():
    f = open(device_file)
    lines = f.readlines(2)
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        lines = read_temp_raw()

    str_pos = lines[1].find('t=')
    if str_pos != -1:
        temp_string = lines[1].strip()[str_pos+2:]
        temp_c = float(temp_string) / 1000
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def check_temp(temp=None):
    if temp[0] < LOW_TEMP:
        print('  低温预警：%.1f℃' % temp[0])
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.HIGH)
#        GPIO.output(ALERT_PIN, GPIO.LOW)
    elif temp[0] > HIGH_TEMP:
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.HIGH)
#        GPIO.output(ALERT_PIN, GPIO.LOW)
        print('  高温预警：%.1f℃' % temp[0])
    else:
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
#        GPIO.output(ALERT_PIN, GPIO.HIGH)
        print('  实时温度：%.1f℃，%.1f℉' % temp)
    upload_temp(temp[0])

def upload_temp(temp):
    strftime = time.strftime('%Y-%dT%H:%M:%S')
    data = {'timestamp': strftime, 'value': temp}
    res = requests.post(api_url, headers = api_headers, data = json.dumps(data))
    if res.status_code == requests.codes.ok:
        print '  已上传温度 (%s)' % strftime
    else:
        print '  温度上传失败 CODE: %s' % res.status_code

if __name__ == '__main__':
    try:
        init_drivers()
        init_gpio()
        while True:
            check_temp(read_temp())
            time.sleep(15)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('  结束温度检测')
    
