import XBee_Threaded
from time import sleep
print 'Enter port  number /dev/ttyACM'
st="/dev/ttyACM"
port = raw_input()
if __name__ == "__main__":
    xbee = XBee_Threaded.XBee(st+port)
    while True:
        sent = xbee.SendStr("R")
    xbee.shutdown()
