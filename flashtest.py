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

lights = [0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0]
print(lights)
while True:
    x1u = adc.read()
    if 0 in lights:
        for i in range(0,51):
            if lights[i] == "":
                lights[i] = x1u
                break
    else:
        for i in range (0,50):
            lights[i] = lights[i+1]
        lights[50] = x1u
        sum = 0
        for i in range(0,51):
            sum += lights[i]
        x1u = sum/50
        lcdWrite(1, str(x1u))
    print(lights)
    
