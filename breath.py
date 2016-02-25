#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

LED_PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(12, 50)
pwm.start(0)

try:
    while True:
        for i in xrange(0, 101, 1):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.01)
        for i in xrange(100, -1, -1):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.01)
except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
