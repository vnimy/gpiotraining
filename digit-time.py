#!/usr/bin/env python
# encoding: utf-8

import RPi.GPIO as GPIO
import time

DS = 13
SHCP = 26
STCP = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(DS, GPIO.OUT)
GPIO.setup(SHCP, GPIO.OUT)
GPIO.setup(STCP, GPIO.OUT)

GPIO.output(STCP, False)
GPIO.output(SHCP, False)

#(DP,G,F,E,D,C,B,A) 共阳：输出低电平亮灯
#Q0->Q7对应A->DP，移位方向Q0->Q7
#Q7对应的先入，所以数组第一位为Q7,最后才到Q0
digits = ((1,0,0,0,0,0,0),
    (1,1,1,1,0,0,1),
    (0,1,0,0,1,0,0),
    (0,1,1,0,0,0,0),
    (0,0,1,1,0,0,1),
    (0,0,1,0,0,1,0),
    (0,0,0,0,0,1,0),
    (1,1,1,1,0,0,0),
    (0,0,0,0,0,0,0),
    (0,0,1,0,0,0,0))

def posedge(clock):
    GPIO.output(clock, False)
    GPIO.output(clock, True)

def setBitData(data):
    GPIO.output(DS, data)
    posedge(SHCP)

def showDigit(dig, num, showDotPoint):
    setBitData(not showDotPoint)
    for value in digits[num]:
        setBitData(value)

    for x in range(0,8):
        if x == dig:
            setBitData(0)
        else:
            setBitData(1)
    
    posedge(STCP)

def showTime():
    while True:
        localtime = time.localtime(time.time())
        strtime = (localtime[3]/10%10,localtime[3]%10,localtime[4]/10%10,localtime[4]%10)
        
        for t in range(1,5):
            if t == 2 and localtime[5]%2:
                dot = True
            else:
                dot = False
            showDigit(t, strtime[t-1], dot)
            time.sleep(0.001)

if __name__ == '__main__':
    try:
        showTime()

    except KeyboardInterrupt:
        pass

    print "退出"
    GPIO.cleanup()
