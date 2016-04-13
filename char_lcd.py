# HD44780 class for micropython board (http://micropython.org)
# Written by Will Pimblett, based on http://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
# http://github.com/wjdp/micropython-lcd
# http://wjdp.co.uk
# modified for i2c based io expander by Keijo Lansikunnas

# enable = bit0
# rs = bit1

import pyb
from pyb import I2C

class HD44780(object):
    
    # Enable and register select bits
    ENABLE = 0x01
    RS = 0x02
    
    # Define some device constants
    LCD_WIDTH = 16    # Maximum characters per line
    # Designation of T/F for character and command modes
    LCD_CHR = True
    LCD_CMD = False

    LINES = {
        0: 0x80, # LCD RAM address for the 1st line
        1: 0xC0, # LCD RAM address for the 2nd line
        # Add more if desired
    }

    # Timing constants
    E_PULSE = 50
    E_DELAY = 50

    def __init__(self, i2c):
        # Initialize i2c
        self.i2c = i2c
        # set all pins to output on port B
        self.i2c.send(b'\x01\x00',32)

        # Initialise display
        self.lcd_byte(0x33,self.LCD_CMD)
        self.lcd_byte(0x32,self.LCD_CMD)
        self.lcd_byte(0x28,self.LCD_CMD)
        self.lcd_byte(0x0C,self.LCD_CMD)
        self.lcd_byte(0x06,self.LCD_CMD)
        self.lcd_byte(0x01,self.LCD_CMD)

    def clear(self):
        # Clear the display
        self.lcd_byte(0x01,self.LCD_CMD)

    def set_line(self, line):
        # Set the line that we're going to print to
        self.lcd_byte(self.LINES[line], self.LCD_CMD)

    def set_string(self, message):
        # Pad string out to LCD_WIDTH
        # message = message.ljust(LCD_WIDTH," ")
        m_length = len(message)
        if m_length < self.LCD_WIDTH:
            short = self.LCD_WIDTH - m_length
            blanks=str()
            for i in range(short):
                blanks+=' '
            message+=blanks
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command
        nh = bits & 0xF0
        nl = (bits << 4) & 0xF0
  
        # High bits
        self.pin_action(nh, mode, False)
        
        # Toggle 'Enable' pin
        self.udelay(self.E_DELAY)
        self.pin_action(nh, mode, True)
        self.udelay(self.E_PULSE)
        self.pin_action(nh, mode, False)
        self.udelay(self.E_DELAY)

        # Low bits
        self.pin_action(nl, mode, False)
        
        # Toggle 'Enable' pin
        self.udelay(self.E_DELAY)
        self.pin_action(nl, mode, True)
        self.udelay(self.E_PULSE)
        self.pin_action(nl, mode, False)
        self.udelay(self.E_DELAY)

    def udelay(self, us):
        # Delay by us microseconds, set as function for portability
        pyb.udelay(us)

    def pin_action(self, bits, mode, enable):
        # Pin high/low functions, set as function for portability
        if mode:
            bits = bits | self.RS
        if enable:
            bits = bits | self.ENABLE
        # write to io expander
        cmd = bytearray(2)
        cmd[0] = 0x15
        cmd[1] = bits
        self.i2c.send(cmd, 32)
