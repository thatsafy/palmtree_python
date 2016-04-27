#!/usr/bin/python3

from pyb import Pin
print("start")
Y8 = Pin('Y8',Pin.OUT_PP)
Y7 = Pin('Y7',Pin.OUT_PP)
Y6 = Pin('Y6',Pin.OUT_PP)
Y5 = Pin('Y5',Pin.OUT_PP)
Y4 = Pin('Y4',Pin.OUT_PP)
Y3 = Pin('Y3',Pin.OUT_PP)
print("pins")

# full steps
# 1 step = 1.8 degrees
# motorTuple = [(1,0,1,0),(1,0,0,1),(0,1,0,1),(0,1,1,0)]

# full steps
# ½ step = 0.9 degrees
motorTuple = [(1,0,1,0),(1,0,0,0),(1,0,0,1),(0,0,0,1),(0,1,0,1),(0,1,0,0),(0,1,1,0),(0,0,1,0)]

# Delay between steps (min 5ms)
# stepDelay

def rotatemotor(angle, stepDelay = 5):
    angle = int(angle/1.8/len(motorTuple))

    Y8.high()
    Y3.high()
    for i in range(0,angle):
        for x in motorTuple:
            print(x)
            if x[0]:
                Y7.high()
            else:
                Y7.low()
            if x[1]:
                Y6.high()
            else:
                Y6.low()
            if x[2]:
                Y5.high()
            else:
                Y5.low()
            if x[3]:
                Y4.high()
            else:
                Y4.low()
            pyb.delay(stepDelay)

while True:
