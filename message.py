from pyb import UART, delay, Pin, ADC, I2C
from binascii import hexlify
import math

uart = UART(6, 115200)

# Temperature
adc = ADC(Pin('X1'))

tempDict = {1630:'1630x1754x0x10',1772:'1772x1922x10x10',1922:'1922x2000x20x5'
        ,2000:'2000x2080x25x5',2080:'2080x2417x30x10'}
# Light sensor
i2c = I2C(1, I2C.MASTER, baudrate=20000)

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
    r = adccv2 / adccv
    light = adccv * 0.46 * (math.e**(-3.13*r))

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
def getAverage(z):
    sum = 0
    for item in z:
        sum += item
    return sum / len(z)

tempList = []
lightList = []

while True:
    tempList.append(measureTemp())
    lightList.append(measureLight())
    
    if len(tempList) > 6:
        tempList.pop(0)
    if len(lightList) > 6:
        lightList.pop(0)
    if len(tempList) == 6 and len(lightList) == 6:
        tempA = str(getAverage(tempList))
        lightA = str(getAverage(lightList))
        send(tempA, lightA)

    pyb.delay(10000)
