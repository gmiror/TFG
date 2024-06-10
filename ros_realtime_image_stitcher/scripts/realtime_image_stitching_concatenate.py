#!/usr/bin/env python
from __future__ import print_function

import roslib
roslib.load_manifest('ros_realtime_image_stitcher')
import sys
import cv2
import rospy
import message_filters 
import numpy as np
import math
import imutils
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_stitcher/image_raw",Image, queue_size=10)
    self.bridge = CvBridge()
    self.image_left = message_filters.Subscriber("/camera2/front_left/image_raw", Image)
    self.image_right = message_filters.Subscriber("/camera1/front_right/image_raw", Image)
    
  def callback(self,image_left, image_right):
    
    try:
      cv_image1 = self.bridge.imgmsg_to_cv2(image_left, "bgr8")
      cv_image2 = self.bridge.imgmsg_to_cv2(image_right, "bgr8")
    except CvBridgeError as e:
      print(e)
    
    # Rotate images 180º
    #cv_image1 = imutils.rotate(cv_image1, 180)
    #cv_image2 = imutils.rotate(cv_image2, 180) 
    
    # Selecting coordinates of the ROI
    tl = (0,100)    # top left
    tr = (640, 100) # top right
    bl = (0,480)    # bottom left
    br = (640,480)  # bottom left
    
    # Apply Geometrical transformation
    pts1 = np.float32([tl, bl, tr, br])
    pts2 = np.float32([[0,0], [0,480], [640,0], [640,480]])

    matrix = cv2.getPerspectiveTransform(pts1,pts2)
   
    cv_image1 = cv2.warpPerspective(cv_image1, matrix, (640,480))
    cv_image2 = cv2.warpPerspective(cv_image2, matrix, (640,480))
    
    # ROI coordinates 
    cv_image1 = cv_image1[100:480, 0:640,:]
    cv_image2 = cv_image2[100:480, 0:640,:]
    
    # Concatenate both images
    cv_image1 = cv2.hconcat([cv_image1, cv_image2])
    
    #cv2.imshow("Image window", cv_image1)
    #cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image1, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    ts = message_filters.ApproximateTimeSynchronizer([ic.image_left, ic.image_right], 10, 0.1, allow_headerless=True)
    ts.registerCallback(ic.callback)
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
      
      
      
		
	
