#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sh import cat,curl,hostname,echo,whoami, grep, uname, uptime, awk
import importlib
import shlex, subprocess
import re
import os
import time
import sys 
import linux_sysinfo as sysinfo 

HOME_DIR = os.getenv("HOME")

def mem():
    pub = rospy.Publisher('ecu_mem', String, queue_size=10) #Declares that the node is publishing to the chatter topic using the message type String.
    rospy.init_node('publisher', anonymous=True) #Name of the topic, anonymous = True ensures that your node has a unique name by adding random numbers to the end of NAME.
    rate = rospy.Rate(10) # 10 hz ,  loop 10 times per second.
    while not rospy.is_shutdown(): #Check if your program exists
        # ECU_MEM_Total = grep ("MemTotal", "/proc/meminfo") # MEM_total (/cat /proc/meminfo)
        # ECU_MEM_free = grep ("MemFree" , "/proc/meminfo") # MEM_free
        # ECU_MEM_Available = grep ("MemAvailable", "/proc/meminfo") # MEM_available
        ECU_MEM_Total = sysinfo.memory_total() # MEM_total (/cat /proc/meminfo)
        ECU_MEM_Available = sysinfo.memory_available() # MEM_available time.sleep(2)
        rospy.loginfo(ecu_mem) #Performs triple-duty: the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout.
        pub.publish(ecu_mem) #Publishes a string to our chatter topic.
        rate.sleep() #The loop calls rate.sleep(), which sleeps just long enough to maintain the desired rate through the loop.

if __name__ == '__main__':
    try:
        mem()
    except rospy.ROSInterruptException:
        pass
