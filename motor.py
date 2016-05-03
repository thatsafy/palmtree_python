#!/usr/bin/python3

import pyb
from pyb import Pin

print("start")
# initializing pins
Y8 = Pin('Y8',Pin.OUT_PP)
Y7 = Pin('Y7',Pin.OUT_PP)
Y6 = Pin('Y6',Pin.OUT_PP)
Y5 = Pin('Y5',Pin.OUT_PP)
Y4 = Pin('Y4',Pin.OUT_PP)
Y3 = Pin('Y3',Pin.OUT_PP)
print("pins ready")

# full steps
# 1 step = 1.8 degrees
# motorTuple = [(1,0,1,0),(1,0,0,1),(0,1,0,1),(0,1,1,0)]

# full steps
# ½ step = 0.9 degrees
motorTuple = [(1,0,1,0),(1,0,0,0),(1,0,0,1),(0,0,0,1),(0,1,0,1),(0,1,0,0),(0,1,1,0),(0,0,1,0)]

# Delay between steps (min. 5ms)
# stepDelay smaller = faster
def rotatemotor(angle, motorStepN, stepDelay = 30):

    steps = 0
    while angle >= 9:
        steps += 10
        angle -= 9
    
    if angle == 8:
        steps += 9
        angle -= 8
        
    elif angle == 7:
        steps += 8
        angle -= 7
        
    elif angle == 6:
        steps += 7
        angle -= 6

    elif angle == 5:
        steps += 6
        angle -= 5
        
    elif angle == 4:
        steps += 4
        angle -= 4

    elif angle == 3:
        steps += 3
        angle -= 3
    
    elif angle == 2:
        steps += 2
        angle -= 2
        
    elif angle == 1:
        steps += 1
        angle -= 1
        
    stepDelay = stepDelay
    # enable stepper motor jumpers in L298
    Y8.high()
    Y3.high()
    temp = motorStepN
    for i in range(motorStepN, 9):
        x = i
        print(str(x))
        motorStepN = x
        x = motorTuple[x]
        if x[0]:
            Y4.high()
        else:
            Y4.low()
        if x[1]:
            Y5.high()
        else:
            Y5.low()
        if x[2]:
            Y6.high()
        else:
            Y6.low()
        if x[3]:
            Y7.high()
        else:
            Y7.low()
        pyb.delay(stepDelay)
    
    for i in range(0,(steps+1)):
        x = i%8
        print(str(x))
        motorStepN = x
        x = motorTuple[x]
        if x[0]:
            Y4.high()
        else:
            Y4.low()
        if x[1]:
            Y5.high()
        else:
            Y5.low()
        if x[2]:
            Y6.high()
        else:
            Y6.low()
        if x[3]:
            Y7.high()
        else:
            Y7.low()
        pyb.delay(stepDelay)
    # disable stepper motor jumpers in L298
    Y8.low()
    Y3.low()
    return motorStepN
    
# for test purposes, just rename file to 'main.py' for this to run
if __name__ == "__main__":
    nappi = pyb.Switch()
    while True:
        if nappi():
            rotatemotor(45,10)