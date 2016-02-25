#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import requests
import json

RELAY_PIN = 16

api_key = '' #yeelink apikey
api_headers = {'U-ApiKey': api_key, 'content-type': 'application/json'}
device_id = 344760
sensor_id = 383361
api_url = r'http://api.yeelink.net/v1.0/device/%s/sensor/%s/datapoints' % (device_id, sensor_id)

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.output(RELAY_PIN, GPIO.HIGH)

if __name__ == '__main__':
    try:
        init_gpio()
        print "等待远程开关命令"
        while True:
            res = requests.get(api_url, headers = api_headers)
            if res.status_code == requests.codes.ok:
                data = res.json()
                if data['value'] == 1:
                    GPIO.output(RELAY_PIN, GPIO.LOW)
                else:
                    GPIO.output(RELAY_PIN, GPIO.HIGH)
            else:
                print "  访问远端出错 CODE: %s (%s)" % (res.status_code, time.strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
