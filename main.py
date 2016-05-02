#!/usr/bin/python3

from pyb import UART, delay, Pin, ADC, I2C
# from binascii import hexlify
import math, char_lcd, time, temperature, light, keyboard, flash, motor

# Serial port connection to raspberry pi
uart = UART(6, 115200)

# LCD I2C Init (keypad uses this too)
i2cLCD = I2C(2, I2C.MASTER, baudrate=20000)
lcd_screen = char_lcd.HD44780(i2cLCD)

# LCD write
def lcdWrite(row, stri):
    lcd_screen.set_line(row)
    lcd_screen.set_string(stri)

# Construct and return message
def message(temp, light):
    m = ""
    m += "T"
    m += ":"
    m += str(temp)
    m += ":"
    m += str(light)
    m += "\n"
    return m

# Currently not in use
def motorAngle():
    return str(360)

# Send message through serial
def send(x, y):
    global uart
    m = message(x, y)
    uart.write(bytes(m.encode('ascii')))
    print("send:", m)

# send login data through serial
def sendLog(h):
    global uart
    l = "L:" + str(h)
    uart.write(bytes(l.encode('ascii')))
    print("Login:",h)

# Lists to calculate average temp and light
# tempList = []
# lightList = []

# Timer help
# sTime = time.time()

# lcdWrite(1, "Waiting for key!")

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
    ch = keyboard.getch()
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
            """
            if "" in taulukko:
                # Write error message to user
                mes = "Invalid code:"
                for s in taulukko:
                    if s != "": mes += "" + s
                lcdWrite(1, mes)
            else:
            """
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
    
# Read keyboard input, login feature
def read_keypad_login(last, taulukko):
    last = last
    taulukko = taulukko
    # Keypad loop
    tuloste = ""
    ch = keyboard.getch()
    logMes = ""
    # When key has been pressed
    if ch != "":
        # If Pressed key is *
        if ch == '*':
            # Reset array and screen
            taulukko = ["", "", "", ""]
            tuloste = ""
            logMes = ""
            lcdWrite(1, "Waiting for key!")
        # If pressed key is #
        elif ch == '#':
            tuloste = ""
            # If taulukko has space
            if "" in taulukko:
                # Write error message to user
                mes = "Invalid code:"
                for s in taulukko:
                    if s != "": mes += "" + s
                taulukko = ["","","",""]
                lcdWrite(1, mes)
            else:
                for h in taulukko:
                    logMes += str(h)
                sendLog(logMes)
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

# temperature, brightness and login loop
# 0000 exits
def checkTemp():
    pyb.delay(100)
    taulukko = ["", "", "", ""]
    myTaulukko = taulukko
    tempList = []
    lightList = []
    sTime = time.time()
    lastPressed = ""
    lcdWrite(0,"Waiting values...")
    lcdWrite(1,"0000# to exit")
    while True:
        keyInput = read_keypad_login(lastPressed,myTaulukko)
        myTaulukko = keyInput[1]
        lastPressed = keyInput[0]
        mes = keyInput[2]
        # stop loop if '0000' given
        if mes == "0000":
            break
        # when enough items in lists calculate averages
        if len(tempList) == 6 and len(lightList) == 6:
            av_values = get_averages(tempList,lightList)
            tempAverage = av_values[0]
            lightAverage = av_values[1]
            tempList[:] = []
            lightList[:] = []
        # every 10 seconds check temperature and brightness
        if time.time() - sTime >= 10:
            tl_values = add_values(tempList, lightList)
            tempList = tl_values[0]
            lightList = tl_values[1]
            sTime = time.time()

# calculate temperature and brightness averages from lists given
def get_averages(tempList, lightList):
    tempList = tempList
    lightList = lightList
    tempA = sum(tempList) / len(tempList)
    lightA = sum(lightList) / len(lightList)
    average_values = [tempA,lightA]
    send(str(tempA), str(lightA))
    return average_values

# check temperature and brightness, add to lists and return
def add_values(tempList, lightList):
    tempList = tempList
    lightList = lightList
    curTemp = temperature.measureTemp()
    curLight = light.measureLight()
    # Write LCD every time sample is taken
    row1 = "C:%.1f lx:%.1f" %(curTemp, curLight)
    lcdWrite(0,row1)
    # Add Samples to lists
    tempList.append(curTemp)
    lightList.append(curLight)
    if len(tempList) > 6:
        tempList.pop(0)
    if len(lightList) > 6:
        lightList.pop(0)
    return [tempList,lightList]

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
        #myTaulukko = taulukko
        #keyInput = read_keypad(lastPressed,myTaulukko)
        #myTaulukko = keyInput[1]
        #lastPressed = keyInput[0]
        #mes = keyInput[2]
        #if mes == "0000":
            #break
        lineText = "A:" + str(angle) + " - S:" + str(speed)
        lcdWrite(0,lineText)
        lcdWrite(1,"* exits")
        ch = keyboard.getch()
        if ch != "":
        # functionality
            if ch == "*":
                break
            elif ch == "1":
                lcdWrite(0,"Set angle")
                myTaulukko = taulukko
                while True:
                    lastPressed = ""
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
                    lastPressed = ""
                    keyInput = read_keypad(lastPressed,myTaulukko)
                    myTaulukko = keyInput[1]
                    lastPressed = keyInput[0]
                    mes = keyInput[2]
                    if mes != "":
                        speed = int(mes)
                        break
                lastPressed = ""
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
        ch = keyboard.getch()
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
                    ch = keyboard.getch()
                    if ch != "":
                        if ch == "*":
                            break
                    flash.flashDetection(angle)
        else:
            lastPressed = ""
        # functionality
        #flash.flashDetection()

# Functions
menuDo = [checkTemp,motorTime,motorFlash]
# menu titles
menu = ["temperature & light", "rotate/time", "rotate/flash"]
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
    ch = keyboard.getch()
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

    """
    # Flash detection
    flash.flashDetection()
    # Temperature loop
    if len(tempList) >= 6 and len(lightList) >= 6:
        temp = get_averages(tempList, lightList)
        tempList = temp[0]
        lightList = temp[1]

    elif (time.time() - sTime) >= 10:
        temp = add_values(sTime, tempList, lightList)
        tempList = temp[0]
        lightList = temp[1]

    else:
        temp = read_keypad(last, taulukko)
        last = temp[0]
        taulukko = temp[1]
        continue
    # Reset timer
    sTime = time.time()
    # pyb.delay(10000)
    """