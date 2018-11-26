#include <DCMotor.h>

#include <XBee.h>

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();

Rx16Response rx16 = Rx16Response();


uint8_t option = 0;
uint8_t data;

// 1 is left 2 is right

dcm m1(8,22,23);
dcm m2(9,24,25);


volatile long int oldtime1,c1=0,t1,rpm1,e1,eo1,es1,ed1,kp1=4,kd1=1,ki1=1,pid1,r1,dir1,rpmo1;
volatile long int oldtime2,c2=0,t2,rpm2,e2,eo2,es2,ed2,kp2=4,kd2=1,ki2=1,pid2,r2,dir2,rpmo2;

volatile long int count1,count2;

void setup() 
{
  m2.minit();
  m1.minit();
  attachInterrupt(digitalPinToInterrupt(2), count1, FALLING);
  attachInterrupt(digitalPinToInterrupt(3), count2, FALLING);
  Serial3.begin(115200);
  Serial.begin(9600);
  xbee.setSerial(Serial3);

}

void loop() 
{
    xbee.readPacket();
    getspeed();
    
    if (xbee.getResponse().isAvailable()) {
      
      if (xbee.getResponse().getApiId() == RX_16_RESPONSE || xbee.getResponse().getApiId() == RX_64_RESPONSE) {
        
        if (xbee.getResponse().getApiId() == RX_16_RESPONSE) {
                xbee.getResponse().getRx16Response(rx16);
          option = rx16.getOption();
          //Serial.print(j++);
            //Serial.print(" ");

          String s;
          int count = 1;
          for (int i = 0; i <  rx16.getDataLength(); i++) {
            if(rx16.getData(i)!=58){
              s += (rx16.getData(i)-48);
              //Serial.print(s);
              }
            else
            {
              //s += '\n';
              switch(count)
              {
                case 1:
                  
                  ::r1 = s.toInt();
                  ::r1=rerange(r1);
                  actuate1(r1);
                  /*Serial.print("Wheel 1: ");*/
                  //Serial.print(r1);
                  break;
                case 2:
                  
                  ::r2 = s.toInt();
                  ::r2 = rerange(r2);
                  actuate2(r2);
                  //Serial.print("Wheel 2: ");
                  //Serial.print(r2);
                  break;            
              }
              
              count++;
              s = "";
            }
           }
        }
      }
    }
}

void getspeed(){
  if (t1!=oldtime1)
    {
      rpm1 = (60000)/(30*(t1-oldtime1));
      t1 = oldtime1;
    }
    else{
      rpm1 = 0;
    }
    if (t2!=oldtime2)
    {
      rpm2 = (60000)/(30*(t2-oldtime2));
      t2 = oldtime2;
    }
    else{
      rpm2 = 0;
    }
}

int rerange(int x){
  if(x > -40 && x < -30){
    x += 30;
  }
  else if(x > -400 && x< -309){
    x+= 300;
  }
  else if(x > -500 && x< -409){
    x+= 400;
  }
  else if(x > 4000 && x < -3099){
    x += 3000;
  }
  return x;
}

void actuate1(int r){
    /*detachInterrupt(19);
    detachInterrupt(3);
    detachInterrupt(18);*/
    dir1 = r/abs(r);

    e1 = abs(r - dir1*rpm1);
    ed1 = (e1 - eo1);
    es1 += e1;

    pid1 = kp1*e1 + kd1*ed1 + ki1*es1;
    
    if(pid1>255) pid1 = 255;

    if(abs(r-rpm1)<5) es1=0;

    if(abs(rpm1)>abs(r)) m1.mspeed(0);
    else m1.mspeed(dir1*pid1);

    eo1 = e1;
    /*attachInterrupt(digitalPinToInterrupt(19), count1, FALLING);
    attachInterrupt(digitalPinToInterrupt(3), count2, FALLING);
    attachInterrupt(digitalPinToInterrupt(18), count3, FALLING);*/
}

void actuate2(int r){
    /*detachInterrupt(19);
    detachInterrupt(3);
    detachInterrupt(18);*/
    dir2 = r/abs(r);

    e2 = abs(r - dir2*rpm2);
    ed2 = (e2 - eo2);
    es2 += e2;

    pid2 = kp2*e2 + kd2*ed2 + ki2*es2;
    
    if(pid2>255) pid2 = 255;

    if(abs(r-rpm2)<5) es2=0;

    if(abs(rpm2)>abs(r)) m2.mspeed(0);
    else m2.mspeed(dir2*pid2);

    eo2 = e2;
    /*attachInterrupt(digitalPinToInterrupt(19), count1, FALLING);
    attachInterrupt(digitalPinToInterrupt(3), count2, FALLING);
    attachInterrupt(digitalPinToInterrupt(18), count3, FALLING);*/
}


