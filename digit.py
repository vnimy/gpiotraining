#!/usr/bin/env python
# encoding: utf-8

import RPi.GPIO as GPIO
import time

DS = 5
SHCP = 13
STCP = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(DS, GPIO.OUT)
GPIO.setup(SHCP, GPIO.OUT)
GPIO.setup(STCP, GPIO.OUT)

GPIO.output(STCP, False)
GPIO.output(SHCP, False)

#(A,B,C,D,E,F,G,DP) 共阳：输出低电平亮灯
#Q0->Q7对应DP->A，移位顺序Q0->Q7，所以DS电平输出排列顺序应为A->DP，Q0->Q7
digits = ((0,0,0,0,0,0,1),
    (1,0,0,1,1,1,1),
    (0,0,1,0,0,1,0),
    (0,0,0,0,1,1,0),
    (1,0,0,1,1,0,0),
    (0,1,0,0,1,0,0),
    (0,1,0,0,0,0,0),
    (0,0,0,1,1,1,1),
    (0,0,0,0,0,0,0),
    (0,0,0,0,1,0,0))

def setBitData(data):
    GPIO.output(DS, data)
    GPIO.output(SHCP, False)
    GPIO.output(SHCP, True)

def showDigit(num, showDotPoint):
    for digit in digits[num]:
        setBitData(digit)
    
    setBitData(not showDotPoint)

    GPIO.output(STCP, False)
    GPIO.output(STCP, True)

if __name__ == '__main__':
    try:
        while True:
            for x in range(0,10):
                showDigit(x, False)
                time.sleep(0.5)
            
            for y in range(0, 10):
                showDigit(y, True)
                time.sleep(0.5)
    
    except KeyboardInterrupt:
        pass
    print "退出"
    GPIO.cleanup()
