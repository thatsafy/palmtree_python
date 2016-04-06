from pyb import UART, delay

uart = UART(6, 115200)

def message():
	m = ""
	m += measureTemp()
	m += ":"
	m += measureLight()
	m += ":"
	m += motorAngle()
	m += ":"
	m += numpad()
	return m

def measureTemp():
	return str(25.1)

def measureLight():
	return str(450)

def motorAngle():
	return str(360)

def numpad():
	return str(1)

def send():
	global uart
	uart.write(bytes(message().encode("ascii")))
	print("send:",message())

while True:
	i = uart.readline().decode("ascii")
	print ("Read:",i)
	#send()	
