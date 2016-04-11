import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='tree', db='test')
cur = conn.cursor()
cur.execute("SELECT id, value FROM test")

for r in cur:
    print(r)

cur.execute('INSERT INTO test (value) VALUES ("joku stringi")')
conn.commit()

cur.close()
conn.close()
