#!/usr/bin/env python

from imapclient import IMAPClient
import time

import RPi.GPIO as GPIO

DEBUG = True

HOSTNAME = '' #服务器
USERNAME = '' #用户
PASSWORD = '' #密码
MAILBOX = 'Inbox'

NEWMAIL_OFFSET = 1
MAIL_CHECK_FREQ = 60

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GREEN_LED = 18
RED_LED = 23
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

def loop():
    server = IMAPClient(HOSTNAME, use_uid=True, ssl=False)
    server.login(USERNAME, PASSWORD)

    if DEBUG:
        print('Logging in as ' + USERNAME)
        select_info = server.select_folder(MAILBOX)
        print('%d messages in INBOX' % select_info['EXISTS'])

    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status['UNSEEN'])

    if DEBUG:
        print('You hav %d new emails!' % newmails)

    if newmails > NEWMAIL_OFFSET:
        GPIO.output(GREEN_LED, True)
        GPIO.output(RED_LED, False)
    else:
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, True)

    time.sleep(MAIL_CHECK_FREQ)

if __name__ == '__main__':
    try:
        print('Press Ctrl-C to quit.')
        while True:
            loop()
    finally:
        GPIO.cleanup()
