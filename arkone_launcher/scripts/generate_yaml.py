#!/usr/bin/env python3

from sh import cat,curl,hostname,echo,whoami, grep, uname, uptime, awk
import os

HOME_DIR = os.getenv("HOME")
ECU_data_directory = HOME_DIR+"/ECU_data"

ecuPort = cat(HOME_DIR+"/ECU_data/Port.txt")
ecuVideoPort = cat(HOME_DIR+"/ECU_data/VideoPort.txt")

os.system("touch $HOME/ECU_data/temp/vars.yaml")
c = open (HOME_DIR+'/ECU_data/temp/vars.yaml','w')
c.write("ecuPort: " + ecuPort.rstrip('\n'))
c.write("\n")
c.write("ecuVideoPort: " + ecuVideoPort.rstrip('\n'))
c.close()