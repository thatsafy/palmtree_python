from pyb import UART

uart = UART(6,9600)
uart.write('hello')