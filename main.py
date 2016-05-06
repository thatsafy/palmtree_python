#!/usr/bin/python3

# Final Product version

from pyb import UART, delay, Pin, ADC, I2C
# from binascii import hexlify
import math, char_lcd, time, keyboard, flash, motor

# LCD I2C Init (keypad uses this too)
i2cLCD = I2C(2, I2C.MASTER, baudrate=20000)
lcd_screen = char_lcd.HD44780(i2cLCD)

motorStepN = 0

# LCD write
def lcd_write(row, stri):
    lcd_screen.set_line(row)
    lcd_screen.set_string(stri)

# Initialize keys
i2cLCD.mem_write(0xFF, 0x20, 0x0C)
i2cLCD.mem_write(0xFF, 0x20, 0x00)
i2cLCD.mem_write(0x00, 0x20, 0x14)

# Keypads last pressed key
last = ""
# Keypad input code
user_input = ["", "", "", ""]
log_message = ""


# Read keyboard input
def read_keypad(last):
    global user_input
    last = last
    # Keypad loop
    tuloste = ""
    ch = keyboard.getch(i2cLCD)
    log_message = ""
    # When key has been pressed
    if ch != "":
        # If Pressed key is *
        if ch == '*':
            # Reset array and screen
            user_input = ["0", "0", "0", "0"]
            log_message = ""
            tuloste = ""
            lcd_write(1, "Waiting for key!")
        # If pressed key is #
        elif ch == '#':
            log_message = ""
            tuloste = ""
            # If user_input has space
            if "" in user_input:
                # Write error message to user
                mes = "Invalid code:"
                for s in user_input:
                    if s != "":
                        mes += "" + s
                lcd_write(1, mes)
            else:
                for h in user_input:
                    log_message += str(h)
                user_input = ["0", "0", "0", "0"]
                lcd_write(1, "Waiting for key!")
        # If pressed key is not same as last key pressed, * or #
        elif last != ch:
            # if user_input has space
            if "" in user_input:
                # Set pressed key to first empty space in user_input
                for i in range(0, 4):
                    if user_input[i] == "":
                        user_input[i] = ch
                        break
            # If user_input has no space
            else:
                # Move all values one space down and add just pressed key to last space
                user_input[0] = user_input[1]
                user_input[1] = user_input[2]
                user_input[2] = user_input[3]
                user_input[3] = ch
            # After adjustment is done print info to user
            for i in range(0, 4):
                tuloste += user_input[i]
            lcd_write(1, tuloste)
            last = ch
    # When key is not pressed
    else:
        # Reset last key pressed
        last = ""
    return (last, log_message)


# rotate motor x angles at y speed
# * exits, 1 to set angle, 2 set speed, 3 to start
def motor_time():
    global motorStepN
    global user_input
    pyb.delay(100)
    angle = 90
    speed = 5
    default_user_input = ["0", "0", "0", "0"]
    default_value = ""
    for numb in default_user_input:
        default_value += numb
    last_pressed = ""
    angle_text = "A:" + str(angle) + " | S:" + str(speed)
    lcd_write(0, angle_text)
    lcd_write(1, "* exits")
    # functionality starts
    while True:
        angle_text = "A:" + str(angle) + " | S:" + str(speed)
        lcd_write(0, angle_text)
        lcd_write(1, "* exits")
        ch = keyboard.getch(i2cLCD)
        if ch != "":
            # if '* pressed exit mode
            if ch == "*":
                break
            # set angle
            elif ch == "1":
                lcd_write(0, "Set angle")
                lcd_write(1, default_value)
                user_input = default_user_input
                while True:
                    pyb.delay(100)
                    key_input = read_keypad(last_pressed)
                    last_pressed = key_input[0]
                    mes = key_input[2]
                    if mes != "":
                        angle = int(mes)
                        user_input = ["0","0","0","0"]
                        break
            # set turning speed
            elif ch == "2":
                lcd_write(0, "set speed")
                lcd_write(1, default_value)
                user_input = default_user_input
                while True:
                    pyb.delay(100)
                    key_input = read_keypad(last_pressed, user_input)
                    user_input = key_input[1]
                    last_pressed = key_input[0]
                    mes = key_input[2]
                    if mes != "":
                        speed = int(mes)
                        user_input = ["0","0","0","0"]
                        break
            # start rotation
            elif ch == "3":
                motorStepN = motor.rotate_motor(angle, motorStepN, speed)
            last_pressed = ch
        else:
            last_pressed = ""


# Rotate motor on flash
# * exits, 1 set angle, 3 to start
def motor_flash():
    global motorStepN
    global user_input
    pyb.delay(100)
    default_user_input = ["0", "0", "0", "0"]
    user_input = default_user_input
    default_value = ""
    for numb in default_user_input:
        default_value += numb
    last_pressed = ""
    angle = 90
    angle_text = "Angle:" + str(angle)
    lcd_write(0, angle_text)
    lcd_write(1, "* to exit")
    # start functionality loop
    while True:
        angle_text = "Angle:" + str(angle)
        lcd_write(0, angle_text)
        lcd_write(1, "* exits")
        ch = keyboard.getch(i2cLCD)
        if ch != "":
            # Exit mode
            if ch == "*":
                break
            # Set turning angle
            elif ch == "1":
                user_input = default_user_input
                print (user_input)
                lcd_write(1, default_value)
                while True:
                    pyb.delay(100)
                    lcd_write(0, "Set angle")
                    last_pressed = ""
                    key_input = read_keypad(last_pressed)
                    
                    last_pressed = key_input[0]
                    mes = key_input[2]
                    if mes != "":
                        angle = int(mes)
                        user_input = default_user_input
                        break
            # Start flash detection
            elif ch == "3":
                while True:
                    # if '*' pressed exit flash detection
                    ch = keyboard.getch(i2cLCD)
                    if ch != "":
                        if ch == "*":
                            break
                    flash.flash_detection(motorStepN, angle)
        else:
            last_pressed = ""


# Functions
menuDo = [motor_time, motor_flash]
# menu titles
menu = ["rotate/time", "rotate/flash"]
# main menu info
menu2 = ["<=1 #select 3=>"]
# initial menu position
menuItem = 0

# Initial rotation
motor.rotate_motor(9, motorStepN, 10)

# Main loop
# 1 goes left, 3 goes right, # is select
# rotates cycle if too far either direction
while True:
    lcd_write(0, menu2[0])
    lcd_write(1, menu[menuItem])
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