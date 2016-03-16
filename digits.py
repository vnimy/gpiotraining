#!/usr/bin/env python
# encoding: utf-8

import RPi.GPIO as GPIO
import commands
import time

class Digits(object):
    def __init__(self, ds, shcp, stcp):
        self.DS = ds #13
        self.SHCP = shcp #26
        self.STCP = stcp #19
        self.gpio = GPIO
        #(DP,G,F,E,D,C,B,A) 共阳：输出低电平亮灯
        #Q0->Q7对应A->DP，移位方向Q0->Q7
        #Q7对应的先入，所以数组第一位为Q7,最后才到Q0
        self.digitsList = ((1,0,0,0,0,0,0),  #0
            (1,1,1,1,0,0,1),    #1
            (0,1,0,0,1,0,0),    #2
            (0,1,1,0,0,0,0),    #3
            (0,0,1,1,0,0,1),    #4
            (0,0,1,0,0,1,0),    #5
            (0,0,0,0,0,1,0),    #6
            (1,1,1,1,0,0,0),    #7
            (0,0,0,0,0,0,0),    #8
            (0,0,1,0,0,0,0),    #9
            (0,0,1,1,1,0,0),    #。
            (1,0,0,0,1,1,0),    #C
            (0,1,1,1,1,1,1))    #-
        self.initGPIO()

    def initGPIO(self):
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.DS, self.gpio.OUT)
        self.gpio.setup(self.SHCP, self.gpio.OUT)
        self.gpio.setup(self.STCP, self.gpio.OUT)
        self.gpio.output(self.STCP, False)
        self.gpio.output(self.SHCP, False)

    def posedge(self, clock):
        self.gpio.output(clock, False)
        self.gpio.output(clock, True)

    def setBitData(self, data):
        self.gpio.output(self.DS, data)
        self.posedge(self.SHCP)

    def showDigit(self, dig, num, showDotPoint):
        self.setBitData(not showDotPoint)
        for value in self.digitsList[num]:
            self.setBitData(value)

        for x in range(0,8):
            if x == dig:
                self.setBitData(0)
            else:
                self.setBitData(1)
        
        self.posedge(self.STCP)

if __name__ == '__main__':
    try:
        digits = Digits(13, 26, 19)
        while True:
            for n in range(1, 5):
                digits.showDigit(n, n, False)
                time.sleep(0.001)
    except KeyboardInterrupt:
        pass

    print "退出"
    GPIO.cleanup()
