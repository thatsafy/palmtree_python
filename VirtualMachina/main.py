import random, time, pymysql


def generate_temp():
        num = random.uniform(10, 30)
        t = time.ctime()
        # tuple = http://www.tutorialspoint.com/python/python_tuples.htm
        values = round(num, 2), t
        return values


def generate_log():
        people = ["matti", "teppo", "seppo", "maija"]
        person = people[random.randint(0, len(people)-1)]
        t = time.ctime()
        values = person, t
        return values

while True:
    print(generate_temp())
    time.sleep(1)
    print(generate_log())
    time.sleep(2)