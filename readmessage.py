import  string, sys, pymysql

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)
conn = pymysql.connect(host='palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com', user='palm', passwd='palmbeach192', db='test')
cur = conn.cursor()

def read(message):
    """
    print("before if")
    if message.find(":") >= 0:
        print("Working!!")  
        temp = message.split(":")
        temperature = temp[0]
        light = temp[1]
        angle = temp[2]
        numpad = temp[3]
        
        readings = (temperature, light, angle, numpad)
        return readings
    else:
        print("Not working!")
        return ""
    """
    return message
    

def listen():
    global ser
    message = ser.readline().decode('ascii')
    
    return message

def writeToSql(stri):
       global cur
       s = 'INSERT INTO test (value) VALUES ("'
       s += stri
       s += '")'
       cur.execute(s)
       conn.commit()

def readFromSql():
        cur.execute("SELECT id, value from test order by id desc limit 5;")
        for r in cur:
            print(r)
        

while True:
    try:
        while True:
            writeToSql("makkaraa")
            readFromSql()
            x = read(listen())
            if x:
                print(x)
                break
    except KeyboardInterrupt:
        cur.close()
        conn.close()
        ser.close()
        sys.exit()

