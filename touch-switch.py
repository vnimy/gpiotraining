#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

SWITCH_PIN = input("触摸开关PIN值：")
LED_PIN = input("LED灯PIN值")
LEDStatus = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
dutyCycle = 100
blinkFreq = 50
pwm = GPIO.PWM(LED_PIN, blinkFreq)

def initswitch():
    print "等待操作触摸开关，按Ctrl-C退出程序"
    
    while True:
        timeCount = timekeeping()
        if timeCount >= 2:
            blink()
        elif timeCount >= 1:
            toggle()
        else:
            changeBrightness()

def toggle():
    global LEDStatus, pwm, dutyCycle
    if LEDStatus == 0:
        print "开灯"
        pwm.start(dutyCycle)
        LEDStatus = 1
    else:
        print "关灯"
        pwm.stop()
        LEDStatus = 0

def changeBrightness():
    global LEDStatus, pwm, dutyCycle
    if LEDStatus == 1:
        if dutyCycle == 100:
            dutyCycle = 30
        else:
            dutyCycle += 35
        print "调节亮度：", dutyCycle
        pwm.ChangeDutyCycle(dutyCycle)

def blink():
    global LEDStatus, pwm, blinkFreq
    if LEDStatus == 1:
        if blinkFreq == 50:
            print "开始闪烁"
            blinkFreq = 3
        else:
            print "结束闪烁"
            blinkFreq = 50
        pwm.ChangeFrequency(blinkFreq)

def timekeeping():
    preStatus = 0
    timeCount = 0
    
    while True:
        pinStatus = GPIO.input(SWITCH_PIN)
        if pinStatus == preStatus and pinStatus == 1:   #前后状态一样且为1
            timeCount += 0.1
            time.sleep(0.1)
        elif pinStatus != preStatus:    #前后状态不一样
            preStatus = pinStatus
            if pinStatus == 0:
                return timeCount
            continue

if __name__ == '__main__':
    try:
        initswitch()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print "退出"
