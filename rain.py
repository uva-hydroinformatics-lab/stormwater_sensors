# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import datetime
import csv
import requests
import json
import plotly.plotly as py
import time
import csv

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #this is the pin reading the gage
count = 0
data = []
print 'test'
GPIO.output(26,1) #I put an LED on pin 26 just as a check

#plotly stuff start
with open('./config.json') as config_file:
        plotly_user_config = json.load(config_file)

py.sign_in(plotly_user_config['plotly_username'], plotly_user_config['plotly_api_key'])

url = py.plot([
        {
                'x':[], 'y':[], 'type': 'scatter',
                'stream':
                        {'token': plotly_user_config['plotly_streaming_tokens'][0]
        }
}], filename='Raspberry Pi Streaming Example Values')

print 'View your streaming graph here: ', url

stream = py.Stream(plotly_user_config['plotly_streaming_tokens'][0])
stream.open()
#plotly stuff end

def timestamp():
        pass


def raining(channel):
        global count
        count += 1
	print 'count: ', count
        global data
	timestamp = datetime.datetime.now()
        data.append({'datetime':timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'count': count/100.0})
	with open('../raindata.csv', 'a') as csvfile:
		w = csv.writer(csvfile, delimiter=',')
		w.writerow([timestamp, count/100.0])        
	print 'data: ', data
	if count % 5  == 0:
                status = submitData(data)
		if status == 200 or status == 202:
			data = []
	        	

def submitData(datalist):
        json_data = json.dumps(datalist)
	print 'posting data'
        r = requests.post('http://54.186.3.124/submitRainData.php', data={'results':json_data})
	print 'the request has been submitted. here is the response', r.text
	print 'the response code is : ', r.status_code
	return r.status_code



GPIO.add_event_detect(23, GPIO.RISING, callback=raining, bouncetime=300)

while True:
	timestamp2=datetime.datetime.now()
	stream.write({'x':timestamp2,'y': count})
        with open('../batdata.csv', 'a') as csvfile:
                w = csv.writer(csvfile, delimiter=',')
                w.writerow([timestamp2])
	time.sleep(0.5)
	if len(data)>0:
		last_time_string = data[len(data)-1].get('datetime')
		last_time_minute = time.strptime(last_time_string, '%Y-%m-%d %H:%M:%S').tm_min 
		current_minute = datetime.datetime.now().minute
		current_minute = current_minute if current_minute>4 else current_minute+60 	
		if current_minute - last_time_minute>4:
			status = submitData(data)
			if status == 202 or status == 200:
				data = []
			

GPIO.cleanup()

