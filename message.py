from pyb import UART, delay, Pin, ADC, I2C

uart = UART(6, 115200)

# Temperature
adc = ADC(Pin('X1'))

tempDict = {1630:'1630x1754x0x10',1772:'1772x1922x10x10',1922:'1922x2000x20x5'
        ,2000:'2000x2080x25x5',2080:'2080x2417x30x10'}

# i2c = I2C(1)


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
    """
    i2c.init(I2C.MASTER, baudrate=115200)
    i2c.init(I2C.SLAVE, addr=0x43)

    i2c.send(0x43)
    data1 = i2c.recv(7)

    i2c.send(0x83)
    data2 = i2c.recv(7)

    i2c.deinit()

    tuloste = str(data1) + ":" + str(data2)
    return tuloste
    """
    return str(2)
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
