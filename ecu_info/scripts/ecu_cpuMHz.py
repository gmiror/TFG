#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sh import cat,curl,hostname,echo,whoami, grep, uname, uptime, awk
import importlib
import shlex, subprocess
import re
import os
import time

HOME_DIR = os.getenv("HOME")

def cpuMHz():
    pub = rospy.Publisher('ecu_cpuMHz', String, queue_size=10) #Declares that the node is publishing to the chatter topic using the message type String.
    rospy.init_node('publisher', anonymous=True) #Name of the topic, anonymous = True ensures that your node has a unique name by adding random numbers to the end of NAME.
    rate = rospy.Rate(10) # 10 hz ,  loop 10 times per second.
    while not rospy.is_shutdown(): #Check if your program exists
        #time.sleep(5)
        os.system("grep MHz /proc/cpuinfo | awk '{ print $4 }' > "+HOME_DIR+"/ecuData/temp/cpuMHz.txt") # CPU_MHz
        os.system("tail -n 1 "+HOME_DIR+"/ecuData/temp/cpuMHz.txt > "+HOME_DIR+"/ecuData/temp/cpuMHz_def.txt")
        ECU_CPU_MHz = cat(""+HOME_DIR+"/ecuData/temp/cpuMHz_def.txt")
        ecu_cpuMHz = '%s MHz' %(ECU_CPU_MHz)
        rospy.loginfo(ecu_cpuMHz) #Performs triple-duty: the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout.
        pub.publish(ecu_cpuMHz) #Publishes a string to our chatter topic.
        rate.sleep() #The loop calls rate.sleep(), which sleeps just long enough to maintain the desired rate through the loop.

if __name__ == '__main__':
    try:
        cpuMHz()
    except rospy.ROSInterruptException:
        pass
