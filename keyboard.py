import time
from pyb import I2C

i2c = I2C(2, I2C.MASTER, baudrate=20000)

def getch(self):
	global i2c
	COLS = [0b11101111, 0b10111111, 0b11111011]
	ROWS = [0b11011111, 0b11110111, 0b11111101, 0b11111110]
	MASKS = [0b00100000, 0b00001000, 0b00000010, 0b00000001]
	keys = {0x30: '1', 0x60: '2', 0x24: '3', 0x18: '4', 0x48: '5', 0x0C: '6', 0x012: '7', 0x42: '8', 0x06: '9', 0x11: '*', 0x41: 0, 0x05: '#'}

	I2CADDR    = 0x20   	# valid range is 0x20 - 0x27    

	IODIR = 0x00
	GPIO  = 0x12		# GPIO pin register base address
	PULUP = 0x0C		# PullUp enable register base address

	for col in range(0,3):
	  i2c.mem_write(COLS[col], I2CADDR, IODIR)
	  time.sleep(0.01)
	  key = i2c.mem_read(1, I2CADDR, GPIO)[0]
	  for m in MASKS:
		print("key: " + key)
		print("mask: " + m)
		print("end: " + (key & m))
		if key & m != 0x00:
		  return (str(keys[key & m]))


i2c.mem_write(0xFF, 0x20, 0x0C)
i2c.mem_write(0xFF, 0x20, 0x00)
i2c.mem_write(0x00, 0x20, 0,14)

while 1:
  ch = keypad.getch()


