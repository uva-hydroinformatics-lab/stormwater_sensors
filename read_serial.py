from serial import Serial
import csv
data = []
ser = Serial(port=5, baudrate=19200) # set the parameters to what you want
text_file = open("rain_temp_data.txt", 'w')
while True:
	line = ser.readline()
	# with open('raindata.csv', 'a') as csvfile:
		# w = csv.writer(csvfile)
		# w.writerow(line)  
	text_file.write(line)
	print line