#!/usr/bin/env python

import rospy, time
from std_msgs.msg import Int32MultiArray

f = open('/home/nvidia/Desktop/res.txt','w')

motor_pub = None
usonic_data = None
cur_speed = 90
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
    #f.write("{:d} {:d} {:f}\n".format(usonic_data[0],usonic_data[1],time.time()-deltime))
    deltime = time.time()
    front_data.data = data.data[0]
    back_data.data = data.data[1]

#grad_lst = [-21.65, -46.96, -59.76, -81.5]
grad_lst = [-21.65, -46.96, -81.5]

def front_data():
    global front_offset, mode, cnt
    dt = time.time() - front_data.tmv
    front_data.tmv = time.time()
    if(mode == 1):
        front_data.data += grad_lst[cnt]*0.1
    return front_data.data

def back_data():
    global mode, cnt 
    dt = time.time() - back_data.tmv 
    back_data.tmv = time.time()
    if(mode == 4):
        back_data.data += grad_lst[0]*0.1 
    return back_data.data

    

    

if __name__ == "__main__":
    global usonic_data, cur_speed, mode, cnt
    init_node()
    front_data.tmv = time.time()
    back_data.tmv = time.time()
    speedlst = [115, 125, 200]
###    speedlst = [124, 124, 124, 127]
#    rangelst = [50, 88, 119, 130]
    rangelst = [41.5, 62, 110]
    rangelst = [40, 57, 81]
###    rangelst = [61, 61, 61, 61]
    cnt = 0
    cur_speed = 90
    tar_speed = 90
    rate = rospy.Rate(10)
    time.sleep(3)
    main_deltime = time.time()
    mode = 0
    while not rospy.is_shutdown():
        if mode == 0:
            mode = 1
            tar_speed = speedlst[cnt]
        elif mode == 1:
            if(rangelst[cnt]-2 <= front_data() and front_data.data < rangelst[cnt]+4):
                tar_speed = speedlst[cnt]-4
            if(rangelst[cnt]-6 <= front_data.data and front_data.data <rangelst[cnt]-2):
                tar_speed = speedlst[cnt]-7
            if (front_data.data < rangelst[cnt]-6):
                mode = 2
                cur_speed = 60
                tar_speed = 90
        elif mode == 2:
            #if (front_data() <= 35):
            #    cur_speed = 90
            if cur_speed == 90:
                #tar_speed = 90
                mode = 3
                time.sleep(2)
        elif mode == 3:
            for i in range(10):
                drive(90,90+i*1.5)
                rate.sleep()
            for i in range(10):
                drive(90,105-i*1.5)
                rate.sleep()
            for i in range(10):
                drive(90,90-i*1.5)
                rate.sleep()
            for i in range(10):
                drive(90,75+i*1.5)
                rate.sleep()
            mode = 4
            tar_speed = 70
        elif mode == 4:
            if(44.5<back_data()<46.5):
                tar_speed = 73
            if(40.5<back_data.data<43.5):
                tar_speed = 75
            if (back_data.data<39.5):
                mode = 5
                cur_speed = 90
                tar_speed = 90
        elif mode == 5:
            if cur_speed == 90:
                mode = 0
                time.sleep(5)
                cnt=cnt+1
                if(cnt>=3):
                    break


        drive(90,cur_speed)
        if(cur_speed != tar_speed):
            cur_speed = cur_speed - 0.5*(cur_speed-tar_speed)-5*abs(cur_speed-tar_speed)/(cur_speed-tar_speed)
        if(abs(cur_speed-tar_speed)<2.7):
            cur_speed = tar_speed
        '''
        if(cur_speed != tar_speed):
            cur_speed = cur_speed+2*abs(tar_speed-cur_speed)/(tar_speed-cur_speed)
        '''
        dt = time.time()-main_deltime
        main_deltime = time.time()
        f.write("%f %f %f\n"%(front_data.data,back_data.data,dt))
        rate.sleep()
    f.close()
    rospy.on_shutdown(exit_node)


