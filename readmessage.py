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
        if temp[0] == "L":
            who(temp[1])
        elif temp[0] == "T":
            temperature = temp[1]
            light = temp[2]
            light = light[0:light.index("\n")]
            readings = (temperature, light)
            return readings
        return ""
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
            
def who(code):
    cur.execute("SELECT name FROM users WHERE access_code = " + code + ";")
    for r in cur: 
        cur.execute('INSERT INTO log (name) VALUES ("' + str(r) + '");')
        conn.commit()
    
while True:
    try:
        x = read(listen())
        if x:
            print(x)
            writeToDataSql(x)
            readFromSql()
    except KeyboardInterrupt:
        cur.close()
        conn.close()
        ser.close()
        sys.exit()

