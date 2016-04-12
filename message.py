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


def message():
    m = ""
    m += measureTemp()
    m += ":"
    m += measureLight()
    """
    m += ":"
    m += motorAngle()
    m += ":"
    m += numpad()
    """
    m += "\n"
    return m

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
    
    # Get values from tempDict
    
    value = ""
    for key in tempDict:
        if tr > key:
            value = tempDict[key]


    values = value.split("x")
    
    step = int(values[3]) / (int(values[1]) - int(values[0]))

    steps = tr - int(values[0])

    temperature = int(values[2]) + steps * step
        
    return str(temperature)

def measureLight():
    # Visible & Infrared
    i2c.send(0x43, 0x39)
    data1 = i2c.recv(1, addr=0x39)
    # Primarly infrared
    i2c.send(0x83, 0x39)
    data2 = i2c.recv(1, addr=0x39)

    step  = data1 & 0x07
	chordnr = (data1 >> 4) & 0x07
	"""
    # convert to light level (lux)
    r = data2 / data1
    light = data1 * 0.46 * (math.e**(-3.13*r))
	"""
    return str(step + " " + chordnr)

def motorAngle():
    return str(360)

def numpad():
    return str(1)

def send():
    global uart
    m = message()
    uart.write(bytes(m.encode('ascii')))

    print("send:", m)

while True:
    send()  
    pyb.delay(500)
