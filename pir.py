#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_PIR = 24

print "  人体红外测试 (按 CTRL-C 退出)"

GPIO.setup(GPIO_PIR, GPIO.IN)

Current_State = 0
Previous_State = 0

try:
    print "  正在初始化模块..."
    while GPIO.input(GPIO_PIR) == 1:
        Current_State = 0

    print "  等一下"

    while True:
        Current_State = GPIO.input(GPIO_PIR)

        if Current_State == 1 and Previous_State == 0:
            print "  有人走过来了！！！"
            Previous_State = 1
        elif Current_State == 0 and Previous_State == 1:
            print "  等一下"
            Previous_State = 0

        time.sleep(0.01)

except KeyboardInterrupt:
    print "  退出"
    GPIO.cleanup();
