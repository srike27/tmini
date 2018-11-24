#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int32
import pygame

def talker():
    pubx = rospy.Publisher('left', Int32, queue_size=10)
    puby = rospy.Publisher('right',Int32,queue_size=10)
    rospy.init_node('joystick', anonymous=True)
    rate = rospy.Rate(30) # 10hz
    while not rospy.is_shutdown():
    	pygame.init()
    	done = False

    	pygame.joystick.init()
    
    	while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done=True 

            joystick_count = pygame.joystick.get_count()


            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                name = joystick.get_name()
        
                axes = joystick.get_numaxes()
        
                ls = joystick.get_axis(2)
                if ls<0:
                	ls =0
                rs = joystick.get_axis(5)
                if rs<0:
                	rs =0

                buttons = joystick.get_numbuttons()

                LB = joystick.get_button(4) ## 0 or 1 -> anti-clockwise rotation
                RB = joystick.get_button(5) ## 0 or 1 -> clockwise rotation


            	if(LB == 1):
                	LB = -1
            	else:
                	LB = 1
            	if(RB == 1):
                	RB = -1
            	else:
                	RB = 1
            
            	ls = LB*ls ## value from -0.2 to 0.2
            	rs = RB*rs ## value from -0.2 to 0.2   
            ls = int(127*ls)
            rs = int(127*rs)
            rospy.loginfo(ls)
            rospy.loginfo(rs)
            pubx.publish(ls)
            puby.publish(rs)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass