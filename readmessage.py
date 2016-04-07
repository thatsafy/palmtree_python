import serial, string, sys

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 0.5)

def read(message):
	"""
	print("before if")
	if message.find(":") >= 0:
		print("Working!!")	
		temp = message.split(":")
		temperature = temp[0]
		light = temp[1]
		angle = temp[2]
		numpad = temp[3]
		
		readings = (temperature, light, angle, numpad)
		return readings
	else:
		print("Not working!")
		return ""
	"""
	return message
	

def listen():
	global ser
	message = ser.readline().decode('ascii')
	
	return message

while True:
	print("sending info")
	
	ser.write(bytes("info\r".encode('ascii')))
	print("listening")
	print(listen())
	try:
		
		"""
		while True:
			x = read(listen())
			if x:
				print(x)
				break
		"""
	except KeyboardInterrupt:
		ser.close()
		sys.exit()
