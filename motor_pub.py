#!/usr/bin/env python

import rospy, time
from std_msgs.msg import Int32MultiArray

motor_pub = None
usonic_data = None

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
    global usonic_data
    usonic_data = data.data

if __name__ == "__main__":
    global usonic_data
    init_node()
    time.sleep(3)
    speedlst = [110, 120, 130]
    cnt = 0
    cur_speed = 90
    tar_speed = 90
    rate = rospy.Rate(10)

    mode = 0
    while not rospy.is_shutdown():
        if mode == 0:
            mode = 1
            tar_speed = speedlst[cnt]
        if mode == 1:
            if(usonic_data[1] <2*(speedlst[cnt]-90)):
                mode = 2
                tar_speed = 90
        if mode == 2:
            if cur_speed == 90:
                mode = 3
                time.sleep(5)
        if mode == 3:
            mode = 4
            tar_speed = 70
        if mode == 4:
            if(usonic_data[4]<40):
                mode = 5
                tar_speed = 90
        if mode == 5:
            if cur_speed == 90:
                mode = 0
                time.sleep(5)
                cnt+=1
                if(cnt>=3):
                    break


        drive(90,cur_speed)

        if(cur_speed != tar_speed):
            cur_speed = cur_speed+2*abs(tar_speed-cur_speed)/(tar_speed-cur_speed)
        rate.sleep()
    rospy.on_shutdown(exit_node)


