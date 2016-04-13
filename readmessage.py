#!/usr/bin/python3
import serial, string, sys, pymysql, time

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout = 1)
conn = pymysql.connect(host='palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com', user='palm', passwd='palmbeach192', db='data')
cur = conn.cursor()

# Compile the message from data given
def read(message):
    print(message)
    print("before if")
    if message.count(":") > 0:
        print("Working!!")  
        temp = message.split(":")
        temperature = temp[0]
        light = temp[1]
        light = light[0:light.index("\n")]
        readings = (temperature, light)
        return readings
    else:
        print("Not working!")
        return ""

# get data from serial
def listen():
    global ser
    message = ser.readline().decode('ascii')    
    return message

# write to SQL database
def writeToDataSql(stri):
       global cur
       s = 'INSERT INTO data (temperature, brightness) VALUES ("'
       s += str(stri[0])
       s += '","'
       s += str(stri[1])
       s += '")'
       cur.execute(s)
       conn.commit()

# Read from SQL database
def readFromSql():
        cur.execute("SELECT id,temperature,brightness from data order by id desc limit 5;")
        for r in cur:
            print(r)

while True:
    try:
        while True:
            # readFromSql()
            x = read(listen())
            if x:
                print(x)
                writeToDataSql(x)
                readFromSql()
                break
        time.sleep(60)
    except KeyboardInterrupt:
        cur.close()
        conn.close()
        ser.close()
        sys.exit()

