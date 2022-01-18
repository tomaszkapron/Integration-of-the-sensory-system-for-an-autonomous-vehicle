#!/usr/bin/env python3
import rospy
import sys
import tf
import tf2_ros
import geometry_msgs.msg

import termios
import tty
import os
import time
import math
import json


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    return

def publish_status(status, from_cam, to_cam):
    static_transformStamped = geometry_msgs.msg.TransformStamped()
    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = from_cam

    static_transformStamped.child_frame_id = to_cam
    static_transformStamped.transform.translation.x = status['x']['value']
    static_transformStamped.transform.translation.y = status['y']['value']
    static_transformStamped.transform.translation.z = status['z']['value']

    quat = tf.transformations.quaternion_from_euler(math.radians(status['roll']['value']),
                                                    math.radians(status['pitch']['value']),
                                                    math.radians(status['azimuth']['value']))
    static_transformStamped.transform.rotation.x = quat[0]
    static_transformStamped.transform.rotation.y = quat[1]
    static_transformStamped.transform.rotation.z = quat[2]
    static_transformStamped.transform.rotation.w = quat[3]
    return static_transformStamped
    #broadcaster.sendTransform(static_transformStamped)


if __name__ == '__main__':
    
    file_MR = open('src/integr_sensors/scripts/t265_d435.txt', 'r')
    #file_MR = open('t265_d435.txt', 'r')
    file_MR_list = []
    print
    print ('t265_d435:')
    for elem in file_MR:
        file_MR_list.append(elem)
        print (float(elem))
    file_MR.close()
    x1, y1, z1, yaw1, pitch1, roll1 = [float(arg) for arg in file_MR_list]

    file_ML = open('src/integr_sensors/scripts/t265_lidar.txt', 'r')
    #file_ML = open('t265_lidar.txt', 'r')
    file_ML_list = []
    print
    print ('t265_lidar:')
    for elem in file_ML:
        file_ML_list.append(elem)
        print (float(elem))
    file_ML.close()
    x2, y2, z2, yaw2, pitch2, roll2 = [float(arg) for arg in file_ML_list]

    status1 = {'mode': 'pitch',
              'x': {'value': x1, 'step': 0.1},
              'y': {'value': y1, 'step': 0.1},
              'z': {'value': z1, 'step': 0.1},
              'azimuth': {'value': yaw1, 'step': 1},
              'pitch': {'value': pitch1, 'step': 1},
              'roll': {'value': roll1, 'step': 1},
              'message': ''}
    status2 = {'mode': 'pitch',
              'x': {'value': x2, 'step': 0.1},
              'y': {'value': y2, 'step': 0.1},
              'z': {'value': z2, 'step': 0.1},
              'azimuth': {'value': yaw2, 'step': 1},
              'pitch': {'value': pitch2, 'step': 1},
              'roll': {'value': roll2, 'step': 1},
              'message': ''}
    status3 = {'mode': 'pitch',
              'x': {'value': 0, 'step': 0.1},
              'y': {'value': 0, 'step': 0.1},
              'z': {'value': 0, 'step': 0.1},
              'azimuth': {'value': 0, 'step': 1},
              'pitch': {'value': 0, 'step': 1},
              'roll': {'value': 0, 'step': 1},
              'message': ''}


    rospy.init_node('my_static_tf2_broadcaster')
    broadcaster = tf2_ros.StaticTransformBroadcaster()

    
    status1_keys = [key[0] for key in status1.keys()]
    st_trans_stmp1 = publish_status(status1, 't265_link', 'd435_link')

    
    status3_keys = [key[0] for key in status3.keys()]
    st_trans_stmp2 = publish_status(status3, 'map', 't265_odom_frame')
    
    time.sleep(1)

    status2_keys = [key[0] for key in status2.keys()]
    st_trans_stmp3 = publish_status(status2, 't265_link', 'os_sensor')

    static_transform_stmp_list = [st_trans_stmp1, st_trans_stmp2, st_trans_stmp3]

    broadcaster.sendTransform(static_transform_stmp_list)
    
    

    print()
    print('Transforms published')
    print('Press Q to quit')
    print()

    while True:
        kk = getch()
        if kk.upper() == 'Q':
            sys.stdout.write('\n')
            exit(0)
