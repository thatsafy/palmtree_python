from pyb import UART, delay, Pin, ADC, I2C
# from binascii import hexlify
import math, char_lcd, time, temperature, light, keyboard

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
tempList = []
lightList = []

# Timer help
sTime = time.time()

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

# Main loop
# Collect data every 10 seconds to lists
# When lists' lengths are 6, calculate averages and send data through serial port
while True:
    # Temperature loop
    if len(tempList) >=  6 and len(lightList) >=  6:
        tempA = sum(tempList) / len(tempList)
        lightA = sum(lightList) / len(lightList)
        send(str(tempA), str(lightA))
        tempList[:] = []
        lightList[:] = []
    elif (time.time() - sTime) >= 10:
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

    else:
        # Keypad loop
        tuloste = ""
        ch = keyboard.getch()
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
        continue
    # Reset timer
    sTime = time.time()
    # pyb.delay(10000)
