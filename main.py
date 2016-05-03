#!/usr/bin/python3

# Final Product version

from pyb import UART, delay, Pin, ADC, I2C
# from binascii import hexlify
import math, char_lcd, time, keyboard, flash, motor

# LCD I2C Init (keypad uses this too)
i2cLCD = I2C(2, I2C.MASTER, baudrate=20000)
lcd_screen = char_lcd.HD44780(i2cLCD)

# LCD write
def lcdWrite(row, stri):
    lcd_screen.set_line(row)
    lcd_screen.set_string(stri)

# Initialize keys
i2cLCD.mem_write(0xFF, 0x20, 0x0C)
i2cLCD.mem_write(0xFF, 0x20, 0x00)
i2cLCD.mem_write(0x00, 0x20, 0x14)

# Keypads last pressed key
last = ""
# Keypad input code
taulukko = ["", "", "", ""]
logMes = ""

# Read keyboard input
def read_keypad(last, taulukko):
    last = last
    taulukko = taulukko
    # Keypad loop
    tuloste = ""
    ch = keyboard.getch(i2cLCD)
    logMes = ""
    # When key has been pressed
    if ch != "":
        # If Pressed key is *
        if ch == '*':
            # Reset array and screen
            taulukko = ["", "", "", ""]
            logMes = ""
            tuloste = ""
            lcdWrite(1, "Waiting for key!")
        # If pressed key is #
        elif ch == '#':
            logMes = ""
            tuloste = ""
            # If taulukko has space
            if "" in taulukko:
                # Write error message to user
                mes = "Invalid code:"
                for s in taulukko:
                    if s != "": mes += "" + s
                lcdWrite(1, mes)
            else:
                for h in taulukko:
                    logMes += str(h)
                taulukko = ["","","",""]
                lcdWrite(1, "Waiting for key!")
        # If pressed key is not same as last key pressed, * or #
        elif last != ch:
            # if taulukko has space
            if "" in taulukko:
                # Set pressed key to first empty space in taulukko
                for i in range(0,4):
                    if taulukko[i] == "":
                        taulukko[i] = ch
                        break
            # If taulukko has no space
            else:
                # Move all values one space down and add just pressed key to last space
                taulukko[0] = taulukko[1]
                taulukko[1] = taulukko[2]
                taulukko[2] = taulukko[3]
                taulukko[3] = ch
            # After adjustment is done print info to user
            for i in range(0,4):
                tuloste += taulukko[i]
            lcdWrite(1, tuloste)
            last = ch
    # When key is not pressed
    else:
        # Reset last key pressed
        last = ""
    return (last, taulukko, logMes)

# rotate motor x angles at y speed
# * exits, 1 to set angle, 2 set speed, 3 to start
def motorTime():
    pyb.delay(100)
    angle = 90
    speed = 5
    taulukko = ["", "", "", ""]
    lastPressed = ""
    lineText = "A:" + str(angle) + " - S:" + str(speed)
    lcdWrite(0,lineText)
    lcdWrite(1,"* exits")
    while True:
        lineText = "A:" + str(angle) + " - S:" + str(speed)
        lcdWrite(0,lineText)
        lcdWrite(1,"* exits")
        ch = keyboard.getch(i2cLCD)
        if ch != "":
        # functionality
            if ch == "*":
                break
            elif ch == "1":
                lcdWrite(0,"Set angle")
                myTaulukko = taulukko
                while True:
                    keyInput = read_keypad(lastPressed,myTaulukko)
                    myTaulukko = keyInput[1]
                    lastPressed = keyInput[0]
                    mes = keyInput[2]
                    if mes != "":
                        angle = int(mes)
                        break
            elif ch == "2":
                lcdWrite(0,"set speed")
                myTaulukko = taulukko
                while True:
                    keyInput = read_keypad(lastPressed,myTaulukko)
                    myTaulukko = keyInput[1]
                    lastPressed = keyInput[0]
                    mes = keyInput[2]
                    if mes != "":
                        speed = int(mes)
                        break
            elif ch == "3":
                motor.rotatemotor(angle,speed)
            lastPressed = ch
        else:
            lastPressed = ""

# Rotate motor on flash
# * exits, 1 set angle, 3 to start
def motorFlash():
    pyb.delay(100)
    taulukko = ["", "", "", ""]
    lastPressed = ""
    angle = 90
    lineText = "Angle:" + str(angle)
    lcdWrite(0,lineText)
    lcdWrite(1,"* to exit")
    while True:
        lineText = "Angle:" + str(angle)
        lcdWrite(0,lineText)
        lcdWrite(1,"* exits")
        ch = keyboard.getch(i2cLCD)
        if ch != "":
            if ch == "*":
                break
            elif ch == "1":
                myTaulukko = taulukko
                while True:
                    lcdWrite(0,"Set angle")
                    lastPressed = ""
                    keyInput = read_keypad(lastPressed,myTaulukko)
                    myTaulukko = keyInput[1]
                    lastPressed = keyInput[0]
                    mes = keyInput[2]
                    if mes != "":
                        angle = int(mes)
                        break
            elif ch == "3":
                while True:
                    ch = keyboard.getch(i2cLCD)
                    if ch != "":
                        if ch == "*":
                            break
                    flash.flashDetection(angle)
        else:
            lastPressed = ""
        # functionality
        #flash.flashDetection()

# Functions
menuDo = [motorTime,motorFlash]
# menu titles
menu = ["rotate/time", "rotate/flash"]
# main menu info
menu2 = ["<=1 #select 3=>"]
# initial menu position
menuItem = 0

# Main loop
# 1 goes left, 3 goes right, # is select
# rotates cycle if too far either direction
while True:
    lcdWrite(0, menu2[0])
    lcdWrite(1, menu[menuItem])
    ch = keyboard.getch(i2cLCD)
    if ch != "":
        if ch == "1":
            menuItem -= 1
        elif ch == "3":
            menuItem += 1
        if ch == '#':
            menuDo[menuItem]()
        if menuItem >= len(menu):
            menuItem = 0
        if menuItem < 0:
            menuItem = len(menu) - 1
        last = ch
    else:
        last = ""