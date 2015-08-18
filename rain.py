# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import datetime
import csv
import requests
import json

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
count = 0
data = []
print 'test'

def timestamp():
        pass


def raining(channel):
        global count
        count += 1
	print 'count: ', count
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        global data
        data.append({'datetime':timestamp, 'count': count/100.0})
        print 'data: ', data
	if count % 10 == 0:
                submitData(data)
	        data = []

def submitData(datalist):
        json_data = json.dumps(datalist)
	print 'posting data'
        r = requests.post('http://54.186.3.124/submitRainData.php', data={'results':json_data})
	print 'the request has been submitted. here is the response', r.text




GPIO.add_event_detect(23, GPIO.RISING, callback=raining, bouncetime=300)

while True:
        pass

GPIO.cleanup()

