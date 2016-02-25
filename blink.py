#!/usr/bin/env python
import RPi.GPIO as io
import time

LED_PIN = 18
sleepTime = 0.5
ioValue = io.LOW

def ioInit():
    global ioValue
    io.setmode(io.BCM)
    io.setup(LED_PIN, io.OUT)
    io.output(LED_PIN, ioValue)

def loop():
    global ioValue
    while True:
        if ioValue == io.LOW:
            ioValue = io.HIGH
        else:
            ioValue = io.LOW

        io.output(LED_PIN, ioValue)
        time.sleep(sleepTime)

def destroy():
    io.output(LED_PIN, io.LOW)
    io.setup(LED_PIN, io.IN)

if __name__ == '__main__':
    ioInit()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
