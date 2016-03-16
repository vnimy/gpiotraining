#!/usr/bin/env python
# encoding: utf-8

from digits import Digits
import commands
import threading
import time

def showTime(digits):
    while True:
        localtime = time.localtime(time.time())
        tm_year = localtime[0]
        tm_mon = localtime[1]
        tm_mday = localtime[2]
        tm_hour = localtime[3]
        tm_min = localtime[4]
        tm_sec = localtime[5]
        strtime = (tm_sec%2, tm_hour/10%10, tm_hour%10, tm_min/10%10, tm_min%10)
        for t in range(1,5):
            if t == 2 and strtime[0]:
                dot = True
            else:
                dot = False
            digits.showDigit(t, strtime[t], dot)
            time.sleep(0.001)

cpu_temp = None
def getTemp():
    global cpu_temp
    while True:
        tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
        cpu_temp = tempFile.read()
        tempFile.close()
        time.sleep(5)

def showTemp(digits):
    global cpu_temp
    while True:
        if cpu_temp == None:
            print '等待获取CPU温度'
            time.sleep(0.1)
        temp = int(cpu_temp)/1000
        strtemp = (temp/10%10, temp%10, 10, 11)
        for t in range(1,5):
            if t == 1 and strtemp[0] == 0:
                continue
            digits.showDigit(t, strtemp[t-1], False)
            time.sleep(0.001)

def showAll(digits):
    tot = ''
    while True:
        localtime = time.localtime(time.time())
        if localtime[5]/10%2:
            if tot != 'time':
                tot = 'time'
            tm_year = localtime[0]
            tm_mon = localtime[1]
            tm_mday = localtime[2]
            tm_hour = localtime[3]
            tm_min = localtime[4]
            tm_sec = localtime[5]
            strtime = (tm_sec%2, tm_hour/10%10, tm_hour%10, tm_min/10%10, tm_min%10)
            for t in range(1,5):
                if t == 2 and strtime[0]:
                    dot = True
                else:
                    dot = False
                digits.showDigit(t, strtime[t], dot)
                time.sleep(0.001)
        else:
            global cpu_temp
            if cpu_temp == None:
                print '等待获取CPU温度'
                time.sleep(0.1)
            temp = int(cpu_temp)/1000
            if tot != 'temp':
                tot = 'temp'
                print "本地时间：%s" % time.asctime(localtime)
                print '核心温度：%d ℃' % temp
            strtemp = (temp/10%10, temp%10, 10, 11)
            for t in range(1,5):
                if t == 1 and strtemp[0] == 0:
                    continue
                digits.showDigit(t, strtemp[t-1], False)
                time.sleep(0.001)

if __name__ == '__main__':
    try:
        digits = Digits(13, 26, 19)
        tGetTemp = threading.Thread(target=getTemp, name='刷新温度')
        tGetTemp.setDaemon(True)
        tGetTemp.start()
        showAll(digits)
    except KeyboardInterrupt:
        pass
    print "退出"
    digits.gpio.cleanup()
