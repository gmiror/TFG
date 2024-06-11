#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sh import cat,curl,hostname,echo,whoami, grep, uname, uptime, awk
import importlib
import shlex, subprocess
import re
import os
import time

#Define the calls to the system

HOME_DIR = os.getenv("HOME")
ECU_Private_IP =hostname("-I") # ECU_Private_Address

def ecu_prip():
    pub = rospy.Publisher('ecu_privateIP', String, queue_size=10) #Declares that the node is publishing to the chatter topic using the message type String.
    rospy.init_node('publisher', anonymous=True) #Name of the topic, anonymous = True ensures that your node has a unique name by adding random numbers to the end of NAME.
    rate = rospy.Rate(10) # 10 hz ,  loop 10 times per second.
    while not rospy.is_shutdown(): #Check if your program exists
        time.sleep(5)
        ecu_private_ip = '%s' % (ECU_Private_IP)
        rospy.loginfo(ecu_private_ip) #Performs triple-duty: the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout.
        pub.publish(ecu_private_ip) #Publishes a string to our chatter topic.
        rate.sleep() #The loop calls rate.sleep(), which sleeps just long enough to maintain the desired rate through the loop.

if __name__ == '__main__':
    try:
        ecu_prip()
    except rospy.ROSInterruptException:
        pass