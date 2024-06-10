#!/usr/bin/env python
from __future__ import print_function
import rospy, sys, cv2, time
import numpy as np
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

I = 0
last_error = 0
twistMessage = Twist()
twistMessage.linear.x = 0
twistMessage.linear.y = 0
twistMessage.linear.z = 0
twistMessage.angular.x = 0
twistMessage.angular.y = 0
twistMessage.angular.z = 0

obstacle_detected = False

# Set up the robot movement publisher
pub = rospy.Publisher("follow_topic",Twist,queue_size=1)

def calculatePID(error,Kp,Ki,Kd):
	global last_error, I
#	
	P = error
	if P > 100:
		P = 100
	elif P < -100:
		P = -100

	I = I + error
	
	if I > 300:
		I = 300
	elif I < -300:
		I = -300

	if error < 10 and error > -10:
		I = I - I/2

	D = error - last_error

	PID = int(Kp*P + Ki*I + Kd*D)

	last_error = error
	
	return PID
	
def turnOffMotors():
	
	twistMessage.linear.x = 0
	twistMessage.angular.z = 0
	pub.publish(twistMessage)

def setSpeed(linear_speed,angular_speed):
	if linear_speed == 0 and angular_speed == 0:
		turnOffMotors()
	else:
		twistMessage.linear.x = linear_speed
		twistMessage.linear.y = 0
		twistMessage.linear.z = 0
		twistMessage.angular.x = 0
		twistMessage.angular.y = 0
		twistMessage.angular.z = angular_speed

		pub.publish(twistMessage)


def laserCallback(msg):

	global obstacle_detected
	
	if(msg.ranges[355] > 0.50):
	
		#print('Ningun obstaculo detectado!')
		obstacle_detected = False
		return obstacle_detected
	
	elif(msg.ranges[355] < 0.50):
	
		#print('Obstaculo detectado!')
		obstacle_detected = True
		return obstacle_detected
    		
		
def navCallback(lane_data):
	
	error = lane_data.data
	linear_speed = 150
	
	#Calculate PID
	PID = calculatePID(error,0.5,0,0)
	#PID = calculatePID(error,0.05,0.0005,0.005)
	print(PID)

	if (obstacle_detected == 0):
		print('Ningun obstaculo detectado!')
			
		if error == 0:
			setSpeed(linear_speed,0)
				
		elif (error > 0 and error < 150):
			setSpeed(linear_speed,PID)

		elif (error < 0):
			setSpeed(linear_speed,-PID)

		elif error == 152:
			setSpeed(linear_speed,5)

		elif error == 153:
			setSpeed(linear_speed,-5)

		else:
			if error == 154:
				time.sleep(0.5)
			turnOffMotors()

	else:
		turnOffMotors()
		print('Obstaculo detectado!')
		

def vehicle_navigation():
	rospy.init_node('vehicle_navigation', anonymous=True)
	
	# Set up the lane_detection data subscriber
	lane_data = rospy.Subscriber('lane_detection', Int32, navCallback)
	
	# Set up the Lidar data subscriber
	lidar_data = rospy.Subscriber('scan',LaserScan, laserCallback)
	
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
		

if __name__ == '__main__':
	vehicle_navigation()
