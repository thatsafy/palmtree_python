from pyb import UART, delay, Pin, ADC, I2C
# from binascii import hexlify
import math, char_lcd, time, temperature, light, keyboard

# Serial port
uart = UART(6, 115200)

# LCD
i2cLCD = I2C(2, I2C.MASTER, baudrate=20000)
lcd_screen = char_lcd.HD44780(i2cLCD)

# LCD write
def lcdWrite(row, stri):
    lcd_screen.set_line(row)
    lcd_screen.set_string(stri)

# Construct and return message
def message(temp, light):
    m = ""
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

def numpad():
    return "1"

# Send message through serial
def send(x, y):
    global uart
    m = message(x, y)
    uart.write(bytes(m.encode('ascii')))
    print("send:", m)

tempList = []
lightList = []

sTime = time.time()

# Collect data every 10 seconds to lists
# When lists' lengths are 6, calculate averages and send data through serial port
lcdWrite(1, "Waiting for key!")
# Initialize keys
i2cLCD.mem_write(0xFF, 0x20, 0x0C)
i2cLCD.mem_write(0xFF, 0x20, 0x00)
i2cLCD.mem_write(0x00, 0x20, 0x14)
last = ""
taulukko = ["", "", "", ""]
while True:
    if (time.time() - sTime) >= 10:
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
        if len(tempList) == 6 and len(lightList) == 6:
            tempA = sum(tempList) / len(tempList)
            lightA = sum(lightList) / len(lightList)
            send(str(tempA), str(lightA))
            tempList[:] = []
            lightList[:] = []
    else:
        tuloste = ""
        ch = keyboard.getch()
        if ch != "":
          if ch == '*':
            taulukko = ["", "", "", ""]
            lcdWrite(1, "Waiting for key!")
          elif last != ch:
            if "" in taulukko:
              for i in range(0,4):
                if taulukko[i] == "":
                  taulukko[i] = ch
                  break
            else:
              taulukko[0] = taulukko[1]
              taulukko[1] = taulukko[2]
              taulukko[2] = taulukko[3]
              taulukko[3] = ch
            for i in range(0,4):
              tuloste += taulukko[i]
            lcdWrite(1, tuloste)
            last = ch
        else:
          last = ""
        continue
    sTime = time.time()
    # pyb.delay(10000)
