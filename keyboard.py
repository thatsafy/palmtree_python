#!/usr/bin/python3

import time
from pyb import I2C


def getch(i2cg):
    i2c = i2cg
    COLS = [0b11101111, 0b10111111, 0b11111011]
    ROWS = [0b11011111, 0b11110111, 0b11111101, 0b11111110]
    MASKS = [0b00101011, 0b00001000, 0b00000010, 0b00000001]
    keys = {"[207, 191, 251]": '1', "[239, 159, 251]": '2', "[239, 191, 219]": '3',
            "[238, 191, 251]": '4', "[239, 190, 251]": '5', "[239, 191, 250]": '6',
            "[237, 191, 251]": '7', "[239, 189, 251]": '8', "[239, 191, 249]": '9',
            "[231, 191, 251]": '*', "[239, 183, 251]": '0', "[239, 191, 243]": '#'}

    I2CADDR = 0x20        # valid range is 0x20 - 0x27

    IODIR = 0x00
    GPIO  = 0x12          # GPIO pin register base address
    PULUP = 0x0C          # PullUp enable register base address

    cola = [0, 0, 0]
    for col in range(0, 3):
        i2c.mem_write(COLS[col], I2CADDR, IODIR)
        time.sleep(0.01)
        cola[col] = i2c.mem_read(1, I2CADDR, GPIO)[0]
    if str(cola) in keys:
        return keys[str(cola)]
    else:
        return ""
