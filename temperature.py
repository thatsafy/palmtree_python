
from pyb import Pin, ADCi

adc = ADC(Pin('X1'))

while True:
	
	temp = adc.read() * 3.3 / 4095
	print(temp)
	
	pyb.delay(500)
