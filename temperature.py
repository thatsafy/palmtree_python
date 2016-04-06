
from pyb import Pin, ADC

adc = ADC(Pin('X1'))

tempDict = {1613:'1613x0x1754x10',1754:'1754x10x1903x10',1903:'1903x20x1980x5'
		,1980:'1980x25x2059x5'}

def calcTemp(tr){
	global tempDict
	# Get values from tempDict

	if (tr >= 1613) and (tr < 1754):
		v = tempDict.get(1613)
	elif (tr >= 1754) and (tr < 1903):
		v = tempDict.get(1754)
	elif (tr >= 1903) and (tr < 1980):
		v = tempDict.get(1903)
	elif (tr >= 1980) and (tr < 2059):
		v = tempDict.get(1980)

	i = v.split("x")

	

	"""
	# roskiin(?)
	# Temp 0 - 10
	if tr >= 1613 and tr < 1754:
		tempFinal = (tr - 1613) / (1754 - 1613) * 10 + 0
	# Temp 10 - 20
	elif tr >= 1754 and tr < 1903:
		tempFinal = (tr - 1754) / (1903 - 1754) * 10 + 10
	# Temp 20 - 25
	elif tr >= 1903 and tr < 1980:
		tempFinal = (tr - 1903) / (1980 - 1903) * 5 + 20
	# Temp 25 - 30
	elif tr >= 1980 and tr < 2059:
		tempFinal = (tr - 1980) / (2059 - 1980) * 5 + 25
	return tempFinal
	"""
	
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
