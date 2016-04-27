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
    """
    m += ":"
    m += motorAngle()
    m += ":"
    m += numpad()
    """
    m += "\n"
    return m

def motorAngle():
    return str(360)

# Send message through serial
def send(x, y):
    global uart
    m = message(x, y)
    uart.write(bytes(m.encode('ascii')))
    print("send:", m)

def sendLog(h):
    global uart
    l = "L:" + str(h)
    uart.write(bytes(l.encode('ascii')))
    print("Login:",h)

# Lists to calculate avarage temp and light
#tempList = []
#lightList = []

# Timer help
#sTime = time.time()

lcdWrite(1, "Waiting for key!")

# Initialize keys
i2cLCD.mem_write(0xFF, 0x20, 0x0C)
i2cLCD.mem_write(0xFF, 0x20, 0x00)
i2cLCD.mem_write(0x00, 0x20, 0x14)

# Keypads last pressed key
last = ""

# Keypad input code
taulukko = ["", "", "", ""]

logMes = ""

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
            lcdWrite(1, "Waiting for key!")
        # If pressed key is #
        elif ch == '#':
            logMes = ""
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

def checkTemp():
    pyb.delay(100)
    taulukko = ["", "", "", ""]
    tempList = []
    lightList = []
    sTime = time.time()
    lastPressed = ""
    lcdWrite(0,"Waiting values...")
    lcdWrite(1,"0000# to exit")
    while True:
        myTaulukko = taulukko
        keyInput = read_keypad(lastPressed,myTaulukko)
        myTaulukko = keyInput[1]
        lastPressed = keyInput[0]
        mes = keyInput[2]
        if mes == "0000":
            break
        if len(tempList) == 6 and len(lightList) == 6:
            av_values = get_averages(tempList,lightList)
            tempAverage = av_values[0]
            lightAverage = av_values[1]
            tempList[:] = []
            lightList[:] = []
        if time.time() - sTime >= 10:
            tl_values = add_values(tempList, lightList)
            tempList = tl_values[0]
            lightList = tl_values[1]
            sTime = time.time()

def get_averages(tempList, lightList):
    tempList = tempList
    lightList = lightList
    tempA = sum(tempList) / len(tempList)
    lightA = sum(lightList) / len(lightList)
    average_values = [tempA,lightA]
    send(str(tempA), str(lightA))
    return average_values

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

# rotate motor x rounds, set speed/time?
# NOT TESTED
def motorTime():
    angle = 90
    speed = 5
    taulukko = ["", "", "", ""]
    lastPressed = ""
    lcdWrite(0,"PLACEHOLDER")
    lcdWrite(1,"0000# to exit")
    while True:
        myTaulukko = taulukko
        keyInput = read_keypad(lastPressed,myTaulukko)
        myTaulukko = keyInput[1]
        lastPressed = keyInput[0]
        mes = keyInput[2]
        if mes == "0000":
            break
        # functionality
        if mes == "0001":
            lcdWrite(0,"Set angle and press #")
            keyInput = read_keypad(lastPressed,myTaulukko)
            myTaulukko = keyInput[1]
            lastPressed = keyInput[0]
            mes = keyInput[2]
            angle = int(mes)
        elif mes == "0002":
            lcdWrite(0,"set speed")
            keyInput = read_keypad(lastPressed,myTaulukko)
            myTaulukko = keyInput[1]
            lastPressed = keyInput[0]
            mes = keyInput[2]
            speed = int(mes)
        elif mes == "0003":
           motor.rotatemotor(angle,speed)

# Rotate motor on flash
# NOT TESTED
def motorFlash():
    taulukko = ["", "", "", ""]
    lastPressed = ""
    lcdWrite(0,"PLACEHOLDER")
    lcdWrite(1,"0000# to exit")
    while True:
        myTaulukko = taulukko
        keyInput = read_keypad(lastPressed,myTaulukko)
        myTaulukko = keyInput[1]
        lastPressed = keyInput[0]
        mes = keyInput[2]
        if mes == "0000":
            break
        # functionality
        flash.flashDetection()

menuDo = [checkTemp,motorTime,motorFlash]
menu = ["temperature & light", "rotate/time", "rotate/flash"]
menu2 = ["<=1 #select 3=>"]
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
