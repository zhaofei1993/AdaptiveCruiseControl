#!/usr/bin/env python

import rospy
from race.msg import drive_param
from race.msg import pid_input

kp = 14.0
kd = 0.09
servo_offset = 18.5
prev_error = 0.0
vel_input = 0

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)


def control(data):
    global prev_error
    global vel_input
    global kp
    global kd

    ## Your code goes here
    # 1. Scale the error
    # 2. Apply the PID equation on error
    # 3. Make sure the error is within bounds
    current_error = 10 * data.pid_error
    angle = kp * current_error + kd * (prev_error - current_error)
    prev_error = current_error

    if angle > 100:
        angle = 100
    elif angle < -100:
        angle = -100
    else:
        angle = angle

    #vel_input = data.pid_vel
    ## END

    msg = drive_param();
    msg.velocity = vel_input
    msg.angle = angle
    print msg
    pub.publish(msg)



if __name__ == '__main__':
    global kp
    global kd
    global vel_input
    print("Listening to error for PID")
    kp = input("Enter Kp Value: ")
    kd = input("Enter Kd Value: ")
    vel_input = input("Enter Velocity: ")
    rospy.init_node('pid_controller', anonymous=True)
    rospy.Subscriber("error", pid_input, control)
    rospy.spin()
