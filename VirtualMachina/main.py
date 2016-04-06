import random, time

def generateTemp():
        num = random.uniform(10,30)
        t = time.ctime()
        # tuple = http://www.tutorialspoint.com/python/python_tuples.htm
        values = round(num,2), t
        return values

def generateLog():
        people = ["matti", "teppo", "seppo", "maija"]
        person = people[random.randint(0, len(people)-1)]
        t = time.ctime()
        values = person, t
        return values

while True:
	print(generateTemp())
	time.sleep(1)
	print(generateLog())
	time.sleep(2)
	
	
	
