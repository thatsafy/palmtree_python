#!/usr/bin/python3
import pyb
import char_lcd,motor
from pyb import ADC, Pin, I2C

# i2cLCD = I2C(2, I2C.MASTER, baudrate=20000)
# lcd_screen = char_lcd.HD44780(i2cLCD)
"""
def lcdWrite(row, stri):
    lcd_screen.set_line(row)
    lcd_screen.set_string(stri)
"""
adc = ADC(Pin('X12'))

# x1u = adc.read()
# lcdWrite(0, "makkara!!!")
lights[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
"""
lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
"""

print(lights)

# LED lights
# 1 = Red
# 2 = Green
# 3 = Yellow
overLED = pyb.LED(1)
middleLED = pyb.LED(2)
underLED = pyb.LED(3)

averages = [0,0,0,0,0,0,0,0,0]
av = 0

# motor.rotatemotor(45)

# lcdWrite(0, "Calibrating!")
def flash_detection(motorStepN, angle=90):
    global av
    global middleLED
    global overLED
    global underLED
    global lights
    x1u = adc.read()
    # If detected light is over average and average is not 0
    if av != 0 and x1u > av + 50:
        motorStepN = motor.rotate_motor(angle, motorStepN)
        middleLED.on()
        overLED.on()
        underLED.on()
        pyb.delay(200)
        middleLED.off()
        overLED.off()
        underLED.off()
        # lcdWrite(0, "Calibrating!")
        return
    # Adding light data to list
    if 0 in averages:
        if 0 in lights:
            for i in range(0, 50):
                if lights[i] == 0:
                    lights[i] = x1u
                    break
        else:
            sum = 0
            for x in range(0, 50):
                sum += lights[x]
            a = sum/50
            for x in range(0, 10):
                if averages[x] == 0:
                    averages[x] = a
            lights= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        sum = 0
        for x in range(0, 10):
            sum += averages[x]
        av = sum/10
        for x in range(0, 9):
            averages[x] = averages[x+1]
        averages[9] = 0

    print(lights.count(0))
