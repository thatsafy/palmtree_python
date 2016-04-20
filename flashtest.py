#!/usr/bin/python3

import char_lcd
from pyb import ADC, Pin, I2C

i2cLCD = I2C(2, I2C.MASTER, baudrate=20000)
lcd_screen = char_lcd.HD44780(i2cLCD)

def lcdWrite(row, stri):
    lcd_screen.set_line(row)
    lcd_screen.set_string(stri)

adc = ADC(Pin('X7'))

# x1u = adc.read()
lcdWrite(0, "makkara!!!")
while True:
    x1u = adc.read()
    lcdWrite(1, str(x1u))
