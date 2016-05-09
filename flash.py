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

print(lights)

# LED lights
# 1 = Red
# 2 = Green
# 3 = Yellow
overLED = pyb.LED(1)
middleLED = pyb.LED(2)
underLED = pyb.LED(3)

averages = []
av = 0

# motor.rotatemotor(45)

lcdWrite(0, "Calibrating!")
def flash_detection(motorStepN, angle=90):
    global av
    global middleLED
    global overLED
    global underLED
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
        lcdWrite(0, "Calibrating!")
        continue
    # Adding light data to list
    if 0 in lights:
        for i in range(0, 200):
            if lights[i] == 0:
                lights[i] = x1u
                break
    else:
        for i in range (0, 199):
            lights[i] = lights[i+1]
        lights[199] = x1u
        sum = 0
        for i in range(0, 200):
            sum += lights[i]
        x1u = sum/200
        av = x1u
        averages.append(x1u)
        if len(averages) == 100:
            lcdWrite(0, "Ready")
            averages[:] = []
        # lcdWrite(1, str(av))
    print(lights.count(0))
