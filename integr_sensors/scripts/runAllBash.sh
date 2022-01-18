#!/bin/bash 

source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

echo "Running Ouster OS0 network configuration file"
./conf_ou.sh &

echo "Waiting 10s..."
sleep 6

#Place to run Ouster and all cameras
echo "Running Ouster..."
roslaunch ouster_ros ouster.launch sensor_hostname:=os-122140000300.local metadata:=/home/lab/metaa.json &

echo "Waiting 10s..."
sleep 6

echo "Running Ouster configuration script"
./conf_ou2.sh &

echo "Waiting 10s..."
sleep 10

echo "Running RealSeanse cameras..."
roslaunch integr_sensors run_cam.launch &

#Place to run set_transform.py,
#drop of d435 frames,
#launch file for creating one topic,
#octomap.mapping

sleep 5
roslaunch integr_sensors two_topic.launch &

sleep 1
cd ~/catkin_ws
rosrun /home/lab/catkin_ws/src/integr_sensors set_transform.py

