from pyb import UART, delay, Pin, ADC

uart = UART(6, 115200)

adc = ADC(Pin('X1'))

tempDict = {1613:'1613x0x1754x10',1754:'1754x10x1903x10',1903:'1903x20x1980x5'
        ,1980:'1980x25x2059x5'}

def message():
    m = ""
    m += measureTemp()
    m += ":"
    m += measureLight()
    m += ":"
    m += motorAngle()
    m += ":"
    m += numpad()
    return m

def measureTemp():
    global tempDict

    # x1U = port x1 U (voltage)
    x1u = adc.read()/4095 * 3.3

    # front resistor R1 1780 ohm
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
    
    step = int(values[3]) / (int(values[2]) - int(values[0]))

    steps = tr - int(values[0])

    temperature = int(values[1]) + steps * step
    
    
    return temperature

def measureLight():
    return str(450)

def motorAngle():
    return str(360)

def numpad():
    return str(1)

def send():
    global uart
    uart.write(bytes(message().encode("ascii")))
    print("send:",message())

while True:
    send()  
