
from pyb import Pin, ADCi

adc = ADC(Pin('X1'))

while True:
	
	# x1U = port x1 U (voltage)
	x1u = adc.read()/4095 * 3.3
	
	# front resistor R1 1780 ohm
	r1 = 1780
	
	# MicroPython board output voltage
	mpu = 3.3

	# Temperature resistor KTY81/210 resistance
	tr = x1u * r1 / (mpu - x1u)
	
	print(tr)
	
	pyb.delay(500)
