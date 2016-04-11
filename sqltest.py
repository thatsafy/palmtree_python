import pymysql

conn = pymysql.connect(host='palm-beach.czexil0tgoyr.us-east-1.rds.amazonaws.com', user='palm', passwd='palmbeach192', db='test')
cur = conn.cursor()
cur.execute("SELECT id, value FROM test")

for r in cur:
    print(r)

cur.execute('INSERT INTO test (value) VALUES ("joku stringi")')
conn.commit()

cur.close()
conn.close()
