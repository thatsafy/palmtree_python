#!/usr/bin/python3
#
# keypad16.py
#
# Jan.25/2015: v1.00 released
#
# 4x4 matrix keypad via MCP23017 I2C I/O expander  Python library
# for the Raspberry Pi. Please see URL below for the introductory article.
#
# http://www.mikronauts.com/raspberry-pi/raspberry-pi-4x4-keypad-i2c-MCP23017-howto/
#
# Copyright 2015 William Henning
# http://Mikronauts.com
#
# If the smbus module is re-entrant (ie allows multiple Python clients, keypad16
# supports multiple keypad modules simultaneously, requires one port of an
# MCP23017 I2C I/O port expander per keypad
#
# tested with generic 4x4 matrix keypad, right side up and up side down
#
# should also work unchanged with 4x3 keypad
#

import smbus
import time

class keypad_module:

  I2CADDR    = 0x20   	# valid range is 0x20 - 0x27
  UPSIDEDOWN = 1      	# direction keypad is facing in
  PORT       = 0      	# 0 for GPIOA, 1 for GPIOB

  IODIRA = 0x00		# I/O direction register base address
  PULUPA = 0x0C		# PullUp enable register base address
  GPIOA  = 0x12		# GPIO pin register base address
  OLATA  = 0x14		# Output Latch register base address
  
  # Keypad Column output values
  KEYCOL = [0b11110111,0b11111011,0b11111101,0b11111110]

  # Keypad Keycode matrix
  KEYCODE  = [['1','4','7','*'], # KEYCOL0
              ['2','5','8','0'], # KEYCOL1
              ['3','6','9','#'], # KEYCOL2
              ['A','B','C','D']] # KEYCOL3

  # Decide the row
  DECODE = [0,0,0,0, 0,0,0,0, 0,0,0,1, 0,2,3,0]

  # initialize I2C comm, 1 = rev2 Pi, 0 for Rev1 Pi
  i2c = smbus.SMBus(1) 

  # get a keystroke from the keypad
  def getch(self):
    while 1:
      for col in range(0,4):
        time.sleep(0.01)
        self.i2c.write_byte_data(self.I2CADDR, self.OLATA+self.port, self.KEYCOL[col]) # write 0 to lowest four bits
        key = self.i2c.read_byte_data(self.I2CADDR, self.GPIOA+self.port) >> 4
        if (key) != 0b1111:
          row = self.DECODE[key]
          while (self.i2c.read_byte_data(self.I2CADDR, self.GPIOA+self.port) >> 4) != 15:
            time.sleep(0.01)
          if self.UPSIDEDOWN == 0:
            return self.KEYCODE[col][row] # keypad right side up
          else:
            return self.KEYCODE[3-row][3-col] # keypad upside down

  # initialize the keypad class
  def __init__(self,addr,ioport,upside):
    self.I2CADDR = addr
    self.UPSIDEDOWN = upside
    self.port = ioport
    self.i2c.write_byte_data(self.I2CADDR,self.IODIRA+self.port,0xF0) # upper 4 bits are inputs
    self.i2c.write_byte_data(self.I2CADDR,self.PULUPA+self.port,0xF0) # enable upper 4 bits pullups
"""
# test code
def main(): 
  keypad = keypad_module(0x27,1,0)  
  while 1:
    ch = keypad.getch()
    print ch

    if ch == 'D':
      exit()

# don't runt test code if we are imported
if __name__ == '__main__':
  main()
"""
