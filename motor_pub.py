#!/usr/bin/env python

import rospy, time
from std_msgs.msg import Int32MultiArray

#f = open('/home/nvidia/Desktop/res.txt','w')

motor_pub = None
usonic_data = None
deltime = time.time()

def init_node():
    global motor_pub
    rospy.init_node('sample')
    rospy.Subscriber('ultrasonic',Int32MultiArray, callback)
    motor_pub = rospy.Publisher('xycar_motor_msg',Int32MultiArray, queue_size=1)

def exit_node():
    print('finished')

def drive(angle,speed):
    global motor_pub
    drive_info = [angle, speed]
    pub_data = Int32MultiArray(data=drive_info)
    motor_pub.publish(pub_data)

def callback(data):
    global usonic_data, deltime
    usonic_data = data.data
    #f.write("{:d} {:f}\n".format(usonic_data[0],time.time()-deltime))
    deltime = time.time()

if __name__ == "__main__":
    global usonic_data
    init_node()
    time.sleep(3)
    speedlst = [115, 125, 135]
    rangelst = [45, 45, 45]
    cnt = 0
    cur_speed = 90
    tar_speed = 90
    rate = rospy.Rate(10)

    mode = 0
    while not rospy.is_shutdown():
        if mode == 0:
            mode = 1
            tar_speed = speedlst[cnt]
        elif mode == 1:
            if(usonic_data[0] <rangelst[cnt]):
                mode = 2
                tar_speed = 90
            elif(usonic_data[0] <90 and cnt==1):
                tar_speed = 112
            elif(usonic_data[0] <140 and cnt==2):
                tar_speed = 112
        elif mode == 2:
            if cur_speed <= 90:
                tar_speed = 90
                mode = 3
                time.sleep(1)
        elif mode == 3:
            for i in range(10):
                drive(90,90+i*2)
                rate.sleep()
            for i in range(10):
                drive(90,110-i*2)
                rate.sleep()
            for i in range(10):
                drive(90,90-i*2)
                rate.sleep()
            for i in range(10):
                drive(90,70+i*2)
                rate.sleep()
            mode = 4
            tar_speed = 70
        elif mode == 4:
            if(usonic_data[1]<50):
                mode = 5
                tar_speed = 90
        elif mode == 5:
            if cur_speed == 90:
                mode = 0
                time.sleep(5)
                cnt=(cnt+1)%3
                if(cnt>=3):
                    break


        drive(90,cur_speed)
        if(cur_speed != tar_speed):
            cur_speed = cur_speed - 0.05*(cur_speed-tar_speed)-0.7*abs(cur_speed-tar_speed)/(cur_speed-tar_speed)
        if(abs(cur_speed-tar_speed)<0.5):
            cur_speed = tar_speed
        '''
        if(cur_speed != tar_speed):
            cur_speed = cur_speed+2*abs(tar_speed-cur_speed)/(tar_speed-cur_speed)
        '''

        rate.sleep()
    #f.close()
    rospy.on_shutdown(exit_node)


