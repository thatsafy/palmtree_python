import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 0.5)

reading = ser.readline()
print(reading)