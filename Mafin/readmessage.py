import serial, sys

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 0)

try:
	while True:
		reading = ser.readline()
		print(reading)
		ser.write('hello, from rasp')
except KeyboardInterrupt:
	ser.close()
	sys.exit()
