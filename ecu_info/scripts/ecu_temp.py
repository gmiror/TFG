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

def temp():
    pub = rospy.Publisher('ecu_temp', String, queue_size=10) #Declares that the node is publishing to the chatter topic using the message type String.
    rospy.init_node('publisher', anonymous=True) #Name of the topic, anonymous = True ensures that your node has a unique name by adding random numbers to the end of NAME.
    rate = rospy.Rate(10) # 10 hz ,  loop 10 times per second.
    while not rospy.is_shutdown(): #Check if your program exists
        time.sleep(5)
        os.system("sensors > "+HOME_DIR+"/ecuData/temp/temp.txt")
        os.system("grep Core "+HOME_DIR+"/ecuData/temp/temp.txt | awk '{ print $3 }' > "+HOME_DIR+"/ecuData/temp/tempFinal.txt")
        ECU_Temp = os.system("tail -n 1 "+HOME_DIR+"/ECU_data/temp/tempFinal.txt > "+HOME_DIR+"/ecuData/temp/tempFinal_def.txt")
        ECU_Temp = cat(""+HOME_DIR+"/ecuData/temp/tempFinal_def.txt")
        ecu_temp = '%s' % (ECU_Temp)
        rospy.loginfo(ecu_temp) #Performs triple-duty: the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout.
        pub.publish(ecu_temp) #Publishes a string to our chatter topic.
        rate.sleep() #The loop calls rate.sleep(), which sleeps just long enough to maintain the desired rate through the loop.

if __name__ == '__main__':
    try:
        temp()
    except rospy.ROSInterruptException:
        pass
