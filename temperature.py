
from pyb import Pin, ADC

adc = ADC(Pin('X1'))

tempDict = {1613:'1613x0x1754x10',1754:'1754x10x1903x10',1903:'1903x20x1980x5'
		,1980:'1980x25x2059x5'}

def calcTemp(tr){
	global tempDict
	# Get values from tempDict

	value = ""
	for key in tempDict:
		if tr > key:
			keyval = tempDict[key]

			
	value = value.split("x")		
	
	return value
}

while True:
	
	# x1U = port x1 U (voltage)
	x1u = adc.read()/4095 * 3.3
	
	# front resistor R1 1780 ohm
	r1 = 1790
	
	# MicroPython board output voltage
	mpu = 3.3

	# Temperature resistor KTY81/210 resistance
	tr = x1u * r1 / (mpu - x1u)
	
	print(tr)

	# Get temperature in celsius	
	print (calcTemp(tr))

	pyb.delay(500)
