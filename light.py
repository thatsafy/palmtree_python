#!/usr/bin/python3

import math
from pyb import I2C

# Light sensor
i2c = I2C(1, I2C.MASTER, baudrate=20000)
def measureLight():
    # Visible & Infrared
    i2c.send(0x43, 0x39)
    data1 = i2c.recv(1, addr=0x39)[0]
    # Primarly infrared
    i2c.send(0x83, 0x39)
    data2 = i2c.recv(1, addr=0x39)[0]

    step  = data1 & 0x0f
    chordnr = (data1 >> 4) & 0x07

    step2 = data2 & 0x0f
    chordnr2 = (data2 >> 4) & 0x07

    chordv = int(16.5 * ((2**chordnr)-1))
    stepv = 2**chordnr

    chordv2 = int(16.5 * ((2**chordnr2)-1))
    stepv2 = 2**chordnr2

    adccv = chordv + stepv * step
    adccv2 = chordv2 + stepv2 * step2

    # Convert to light level (lux)
    try:
        r = adccv2 / adccv
        light = adccv * 0.46 * (math.e**(-3.13*r))
    except ZeroDivisionError:
        return 0
    return light 