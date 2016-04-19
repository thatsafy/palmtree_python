import time
from pyb import I2C

class keypad_module:

  i2c        = ""
  I2CADDR    = 0x20   	# valid range is 0x20 - 0x27
  
  IODIR = 0x00		# I/O direction register base address
  PULUP = 0x0C		# PullUp enable register base address
  GPIO  = 0x12		# GPIO pin register base address
    
  # Keypad Column output values
  COLS = [0b11101111, 0b10111111, 0b11111011]
  ROWS = [0b11011111, 0b11110111, 0b11111101, 0b11111110]
  MASKS = [0b00100000, 0b00001000, 0b00000010, 0b00000001]

  # Keypad Keycode matrix

  keys = {0x30: '1', 0x60: '2', 0x24: '3', 0x18: '4', 0x48: '5', 0x0C: '6', 0x012: '7', 0x42: '8', 0x06: '9', 0x11: '*', 0x41: 0, 0x05: '#'}

  # get a keystroke from the keypad
  def getch(self):
    for col in range(0,3)
      print("col: %" % col)
      self.i2c.mem_write(COLS[col], I2CADDR, IODIR)
      self.i2c.mem_write(0xff, I2CADDR, PULUP)
      time.sleep(0.01)
      key = i2c.mem_read(1, I2CADDR, GPIO)
      print("key: %" % key)
      for m in MASKS:
        if key & m != 0x00:
          return (keys[key & m])
      return "" 

  # initialize the keypad class
  def __init__(self,i2c,addr):
    self.i2c = i2c
    self.I2CADDR = addr
    
LCD = I2C(2, I2C.MASTER, baudrate=20000)

# test code
def main(): 
  keypad = keypad_module(LCD,0x20)  
  while 1:
    ch = keypad.getch()
    print(ch)

    if ch == 'D':
      exit()

# don't runt test code if we are imported
if __name__ == '__main__':
  main()

