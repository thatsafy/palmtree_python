#!/usr/bin/python3

from pyb import Pin, ADC

# Temperature pin
adc = ADC(Pin('X1'))

tempDict = {1630:'1630x1754x0x10',1772:'1772x1922x10x10',1922:'1922x2000x20x5',2000:'2000x2080x25x5',2080:'2080x2417x30x10'}

def getTemperature():
    global tempDict
	
    # x1U = port x1 U (voltage)
    x1u = adc.read()/4095 * 3.3

    # front resistor R1 1780 ohm
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
