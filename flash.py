#!/usr/bin/python3
import pyb
import char_lcd,motor
from pyb import ADC, Pin, I2C

i2cLCD = I2C(2, I2C.MASTER, baudrate=20000)
lcd_screen = char_lcd.HD44780(i2cLCD)

def lcdWrite(row, stri):
    lcd_screen.set_line(row)
    lcd_screen.set_string(stri)

adc = ADC(Pin('X7'))

# x1u = adc.read()
# lcdWrite(0, "makkara!!!")

lights = [0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0,
          0,0,0,0,0,0,0,0,0,0]

lightCopy = lights

print(lights)

# LED lights
# 1 = Red
# 2 = Green
# 3 = Yellow
overLED = pyb.LED(1)
middleLED = pyb.LED(2)
underLED = pyb.LED(3)

lightOver = False
lightMiddle = False
lightUnder = False

averages = []
av = 0

# motor.rotatemotor(45)

def flashDetection():
    global av
    global middleLED
    global overLED
    global underLED
    x1u = adc.read()
    if av != 0 and x1u > av + 50:
        motor.rotatemotor(90)
        # lights = lightCopy
        middleLED.on()
        overLED.on()
        underLED.on()
        pyb.delay(200)
        middleLED.off()
        overLED.off()
        underLED.off()
        #continue
    if 0 in lights:
        for i in range(0,200):
            if lights[i] == 0:
                lights[i] = x1u
                break
    else:
        for i in range (0,199):
            lights[i] = lights[i+1]
        lights[199] = x1u
        sum = 0
        for i in range(0,200):
            sum += lights[i]
        x1u = sum/200
        av = x1u
        averages.append(x1u)
        if len(averages) == 100:
            # lcdWrite(0, "Ready")
            averages[:] = []
        # lcdWrite(1, str(av))
    print(lights.count(0))



"""
while True:
    x1u = adc.read()
    if av != 0 and x1u > av + 50:
        motor.rotatemotor(45)
        # lights = lightCopy
        middleLED.on()
        overLED.on()
        underLED.on()
        pyb.delay(200)
        middleLED.off()
        overLED.off()
        underLED.off()
        continue
    if 0 in lights:
        for i in range(0,200):
            if lights[i] == 0:
                lights[i] = x1u
                break
    else:
        for i in range (0,199):
            lights[i] = lights[i+1]
        lights[199] = x1u
        sum = 0
        for i in range(0,200):
            sum += lights[i]
        x1u = sum/200
        av = x1u
        averages.append(x1u)
        if len(averages) == 100:
            lcdWrite(0, "Ready")
            averages[:] = []
        lcdWrite(1, str(av))
    print(lights.count(0))
"""
