from pyb import UART, sys

uart = UART(6,9600)

try:
	while True:
		uart.write('hello, from pyboard')
		reading = uart.readline()
		print(reading)
except KeyboardInterrupt:
	uart.close()
	sys.exit()