#!/usr/bin/env python3
import roslib
import rospy
import tf

from nav_msgs.msg import Odometry


def callback(msg):
    #br = tf.TransformBroadcaster()
    #br.sendTransform((-msg.pose.pose.position.x,
    #                  msg.pose.pose.position.y,
    #                  -msg.pose.pose.position.z),
    #                 (-msg.pose.pose.orientation.y,
    #                  msg.pose.pose.orientation.x,
    #                  msg.pose.pose.orientation.z,
    #                  msg.pose.pose.orientation.w),
    #                 rospy.Time(),
    #                 "central",
    #                 "map")

    br = tf.TransformBroadcaster()                     
    br.sendTransform((0,0,0), tf.transformations.quaternion_from_euler(0, 0, k),
                 rospy.Time(0),
                 "map",
                 "t265_odom_frame")

 
if __name__ == '__main__':
    rospy.init_node('tf_camera')


    rospy.loginfo("TF publisher is run")

    rospy.spin()
