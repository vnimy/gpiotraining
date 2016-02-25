#!/usr/bin/env python
# encodeing: utf-8

import RPi.GPIO as GPIO
import time

DO_PIN = 27
ALERT_PIN = 26
BLINK_PIN = 22

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DO_PIN, GPIO.IN)
#    GPIO.setup(ALERT_PIN, GPIO.OUT)
    GPIO.setup(BLINK_PIN, GPIO.OUT)
    GPIO.output(BLINK_PIN, GPIO.LOW)

def loop():
    while True:
        GPIO.output(BLINK_PIN, GPIO.input(DO_PIN))
        time.sleep(0.5)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
