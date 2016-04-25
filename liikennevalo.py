# main.py -- put your code here!
nappi = pyb.Switch()

ledvihr = pyb.LED(2)

ledpuna = pyb.LED(1)

ledkelta = pyb.LED(3)

ledsin = pyb.LED(4)

def odota():
        while not(nappi()):
                pass
                pyb.delay(250)
        while (nappi()):
                pass

while True:
        ledkelta.off()
        ledpuna.on()
        odota()
        ledkelta.on()
        odota()
        ledpuna.off()
        ledkelta.off()
        ledvihr.on()
        odota()
        ledvihr.off()
        ledkelta.on()
        odota()
