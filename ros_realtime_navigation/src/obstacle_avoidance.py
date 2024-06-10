#! /usr/bin/env python

#Importing all the required Libraries and messages 
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


# Create a Twist message to control robot movement
move_robot = Twist()

move_robot.linear.x = 100
move_robot.angular.z = 0

#Defining a call back function for the Subcriber. 

def callback(msg):
	#Publish the movement command 
	Pub1.publish(move_robot)
	
	# Check distance directly in front of the robot (at the middle) 
	if(msg.ranges[355] > 0.50):

		# If the distance is greater than 0.10 meters, move forward 
		move_robot.linear.x = 100
		move_robot.angular.z = 0.0
		
	elif(msg.ranges[355] < 0.50):
	
		# If the distance is less than 0.10 meters, stop to avoid collis 
		move_robot.linear.x = 0.0
		move_robot.angular.z = 0.0
		
# Initialize the ROS node 
rospy.init_node('obstacle_avoidance')

# Set up the robot movement publisher
Pub1 = rospy.Publisher('follow_topic',Twist,queue_size = 1)

# Set up the Lidar data subscriber
Sub1 = rospy.Subscriber('scan',LaserScan,callback)

# Keep the node running and processing Lidar data 
rospy.spin()
