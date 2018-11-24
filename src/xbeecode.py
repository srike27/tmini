import XBee_Threaded
from time import sleep
print 'Enter port  number /dev/ttyACM'
st="/dev/ttyACM"
port = raw_input()
xbee = XBee_Threaded.XBee(st+port)
print "connected"
import pygame

if __name__ == "__main__":
    pygame.init()
    done = False

    r = 50.760/1000 # metres
    R = 150.000/1000 # metres
    wz = 0.5 #rps

    clock = pygame.time.Clock()

    pygame.joystick.init()
    
    while True:
        try:
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


            s= str(ls) + ':' + str(rs) + ':'
            sent = xbee.SendStr(s.encode())    
            clock.tick(20)
        except KeyboardInterrupt:
            break
    

    xbee.shutdown()
pygame.quit ()