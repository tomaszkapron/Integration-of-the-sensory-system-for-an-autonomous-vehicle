#!/bin/bash 

nc 10.5.5.1 7501 
sudo ptp4l -i eno1 -m -S
