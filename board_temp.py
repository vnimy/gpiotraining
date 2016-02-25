#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json

api_key = 'apikey' #yeelink apikey
api_headers = {'U-ApiKey': api_key, 'content-type': 'application/json'}
device_id = 344760
sensor_id = 383366
api_url = r'http://api.yeelink.net/v1.0/device/%s/sensor/%s/datapoints' % (device_id, sensor_id)

TEMP_FILE = '/sys/class/thermal/thermal_zone0/temp'


def upload_temp(temp):
    strftime = time.strftime('%Y-%m-%dT%H:%M:%S')
    data = {'timestamp': strftime, 'value': temp}
    res = requests.post(api_url, headers = api_headers, data = json.dumps(data))
    if res.status_code == requests.codes.ok:
        print "  已上传温度 (%s)" % strftime
    else:
        print "  温度上传失败 CODE: %s" % res.status_code

if __name__ == '__main__':
    try:
        while True:
            file = open(TEMP_FILE)
            temp = float(file.read()) / 1000
            file.close()
            print '  主机温度：%.1f ℃' % temp
            upload_temp(temp)
            time.sleep(15)
    except KeyboardInterrupt:
        print '  退出温度监测'
