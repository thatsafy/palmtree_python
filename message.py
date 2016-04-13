from pyb import UART, delay, Pin, ADC, I2C
# from binascii import hexlify
import math, char_lcd, time

# Serial port
uart = UART(6, 115200)

# Temperature
adc = ADC(Pin('X1'))

tempDict = {1630:'1630x1754x0x10',1772:'1772x1922x10x10',1922:'1922x2000x20x5'
        ,2000:'2000x2080x25x5',2080:'2080x2417x30x10'}
# Light sensor
i2c = I2C(1, I2C.MASTER, baudrate=20000)

# LCD
i2cLCD = I2C(2, I2C.MASTER, baudrate=20000)
lcd_screen = char_lcd.HD44780(i2cLCD)

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

# measure temperature
def measureTemp():
    global tempDict

    # x1U = port x1 U (voltage)
    x1u = adc.read()/4095 * 3.3

    # front resistor R1 1790 ohm
    r1 = 1790

    # MicroPython board output voltage
    mpu = 3.3

    # Temperature resistor KTY81/210 resistance
    tr = x1u * r1 / (mpu - x1u)
    
    # Return value from tempDict
    value = ""
    for key in tempDict:
        if tr > key:
            value = tempDict[key]

    values = value.split("x")
    step = int(values[3]) / (int(values[1]) - int(values[0]))
    steps = tr - int(values[0])

    temperature = int(values[2]) + steps * step
    return temperature

# Measure light level (lux)
def measureLight():
    while True:
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
            continue
        return light
    
def motorAngle():
    return str(360)

def numpad():
    return str(1)

# Send message through serial
def send(x, y):
    global uart
    m = message(x, y)
    uart.write(bytes(m.encode('ascii')))
    print("send:", m)

# calculate average
tempList = []
lightList = []

sTime = time.time()

# Collect data every 10 seconds to lists
# When lists' lengths are 6, calculate averages and send data through serial port
while True:
    if (time.time() - sTime) >= 10:
        tempList.append(measureTemp())
        lightList.append(measureLight())
        
        if len(tempList) > 6:
            tempList.pop(0)
        if len(lightList) > 6:
            lightList.pop(0)
        if len(tempList) == 6 and len(lightList) == 6:
            tempA = str(sum(tempList) / len(tempList))
            lightA = str(sum(lightList) / len(lightList))
            lcd_screen.set_line(0)
            lcd_screen.set_string("C:" + tempA)
            lcd_screen.set_line(1)
            lcd_screen.set_string("lx:" + lightA)
            send(tempA, lightA)
    else:
        continue
    sTime = time.time()
    # pyb.delay(10000)
