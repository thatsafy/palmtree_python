#!/usr/bin/python3
import pyb
import char_lcd,motor, keyboard, time
from pyb import ADC, Pin, I2C

adc = ADC(Pin('X12'))

lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print(lights)

# LED lights
# 1 = Red
# 2 = Green
# 3 = Yellow
over_led = pyb.LED(1)
middle_led = pyb.LED(2)
under_led = pyb.LED(3)

averages = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
av = 0


def flash_detection(i2cLCD, motor_step_n, angle=90):
    global averages
    global av
    global middle_led
    global over_led
    global under_led
    global lights
    ave = 0
    # If detected light is over average and average is not 0
    startTime = time.time()
    while True:
        # if '*' pressed exit flash detection
        if time.time() - startTime >= 0.2:
            ch = keyboard.getch(i2cLCD)
            if ch == "0":
                break
            else:
                startTime = time.time()
        x1u = adc.read()
        if av != 0 and x1u > av + 50:
            motor_step_n = motor.rotate_motor(angle, motor_step_n)
            middle_led.on()
            over_led.on()
            under_led.on()
            pyb.delay(200)
            middle_led.off()
            over_led.off()
            under_led.off()
            av = 0
            averages = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            continue
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

        print("av:" , av , " averages: " , averages)
