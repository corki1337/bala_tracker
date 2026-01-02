#!/bin/bash

source /opt/ros/jazzy/setup.bash
source ~/microros_ws/install/local_setup.bash
source ~/bala/ros_ws/install/setup.bash

ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM1 -b 115200 &

sleep 2


ros2 run bala_perception start_kamera