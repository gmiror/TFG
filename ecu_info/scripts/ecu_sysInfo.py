#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from std_msgs.msg import String
from sh import cat,curl,hostname,echo,whoami, grep, uname, uptime, awk
import importlib
import shlex, subprocess
import re
import os

#Define the calls to the system
ECU_VIN = cat(""+HOME_DIR+"/ecuData/VIN.txt")
ECU_TYPE = hostname("-s") #ECU_ID
ECU_ID =cat("/sys/class/net/wlp5s0/address") # ECU_ID
ECU_Public_IP = curl("-s","https://ipinfo.io/ip") # ECU_Public_Address
ECU_Private_IP =hostname("-I") # ECU_Private_Address
ECU_Port = cat(""+HOME_DIR+"/ecuData/Port.txt")
ECU_OS_Type = uname("-o") # OS_Type
ECU_OS_Architecture = uname ("-m") # OS_Architecure
ECU_SOinfo = cat(""+HOME_DIR+"/ecuData/ECU_SOinfo.txt")
ECU_CPU_info = grep("model name","/proc/cpuinfo") # CPU_info (/cat /proc/cpuinfo)
#ECU_CPU_Usage = # CPU_usage
ECU_CPU_MHz = grep("cpu MHz", "/proc/cpuinfo") # CPU_MHz
#ECU_CPU_Tmp = # CPU_temp
ECU_MEM_Total = grep ("MemTotal", "/proc/meminfo") # MEM_total (/cat /proc/meminfo)
ECU_MEM_free = grep ("MemFree" , "/proc/meminfo") # MEM_free
ECU_MEM_Available = grep ("MemAvailable", "/proc/meminfo") # MEM_available
ECU_HDD_Usage = cat(""+HOME_DIR+"/ecuData/HDD_usage.txt")
ECU_USER = whoami() # ECU_USER (Alternative -> os.getlogin())
ECU_Boot = uptime ("-s") # LastSystem_Boot
HOME_DIR = os.getenv("HOME")

def talker():
    pub = rospy.Publisher('ecu_info', String, queue_size=10) #Declares that the node is publishing to the chatter topic using the message type String.
    rospy.init_node('publisher', anonymous=True) #Name of the topic, anonymous = True ensures that your node has a unique name by adding random numbers to the end of NAME.
    rate = rospy.Rate(10) # 10 hz ,  loop 10 times per second.
    while not rospy.is_shutdown(): #Check if your program exists
	print('\n')
        ECU_Info = '{ECU_VIN: %s ECU_TYPE: %s ECU_ID: %s ECU_Public_IP: %s ECU_Private_IP: %s ECU_Port: %s ECU_OS_Type: %s ECU_OS_Architecture: %s ECU_OS_Version_%s ECU_cpu_%s ECU_%s ECU_%s ECU_%s ECU_%s ECU_HDD_Usage: %s ECU_USER: %s ECU_Boot: %s}' % (ECU_VIN, ECU_TYPE, ECU_ID, ECU_Public_IP, ECU_Private_IP, ECU_Port, ECU_OS_Type, ECU_OS_Architecture, ECU_SOinfo, ECU_CPU_info, ECU_CPU_MHz, ECU_MEM_Total, ECU_MEM_free, ECU_MEM_Available,ECU_HDD_Usage, ECU_USER, ECU_Boot)
        rospy.loginfo(ECU_Info) #Performs triple-duty: the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout.
        pub.publish(ECU_Info) #Publishes a string to our chatter topic.
        rate.sleep() #The loop calls rate.sleep(), which sleeps just long enough to maintain the desired rate through the loop.

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
