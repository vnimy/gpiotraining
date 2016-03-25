#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json

def upload(api_key, device_id, sensor_id, value):
    api_headers = {'U-ApiKey': api_key, 'content-type': 'application/json'}
    api_url = r'http://api.yeelink.net/v1.0/device/%s/sensor/%s/datapoints' % (device_id, sensor_id)

    strftime = time.strftime('%Y-%m-%dT%H:%M:%S')
    data = {'timestamp': strftime, 'value': value}
    res = requests.post(api_url, headers=api_headers, data=json.dumps(data))
    return {'strftime': strftime, 'status_code': res.status_code}
