#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
import XBee_Threaded
from time import sleep
print 'Enter port  number /dev/ttyACM'
st="/dev/ttyACM"
port = raw_input()
xbee = XBee_Threaded.XBee(st+port)
print "connected"

ls =0
rs = 0

def callbackx(datax):
    global ls
    ls = datax.data

def callbacky(datay):
    global rs
    rs = datay.data
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    while True:

        rospy.Subscriber("left", Int32, callbackx)
        rospy.Subscriber("right", Int32, callbacky)
        s= str(ls) + ':' + str(rs) + ':'
        sent = xbee.SendStr(s.encode())


    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    ls
    rs
    listener()
        
