#!/bin/bash 

source ~/catkin_ws/devel/setup.bash

sudo ip addr flush dev eno1
ip addr show dev eno1
sleep 0.5
sudo ip link set eno1 down
sleep 0.5
sudo ip addr add 10.5.5.1/24 dev eno1
sleep 0.5
sudo ip link set eno1 up
sleep 0.5
sudo ip addr show dev eno1
sudo dnsmasq -C /dev/null -kd -F 10.5.5.50,10.5.5.100 -i eno1 --bind-dynamic


