#include <stdio.h>
#include <iostream>

#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>

#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/image_encodings.h>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>


#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>

//#include <opencv2/features2d/features2d.hpp>
//#include <opencv2/nonfree/nonfree.hpp>
//#include <opencv2/calib3d/calib3d.hpp>

using namespace sensor_msgs;
using namespace message_filters;
using namespace cv;


static const std::string OPENCV_WINDOW = "Image window";

sensor_msgs::ImagePtr finalImage_pub;

void callback(const ImageConstPtr& image1, const ImageConstPtr& image2)
{
  
  // Pointer used for the conversion from a ROS message to 
  // an OpenCV-compatible image
  cv_bridge::CvImagePtr cv_ptr1;
  cv_bridge::CvImagePtr cv_ptr2;
   
  try
  { 
    // Convert the ROS message  
    cv_ptr1 = cv_bridge::toCvCopy(image1, "bgr8");
    cv_ptr2 = cv_bridge::toCvCopy(image2, "bgr8");
     
    // Store the values of the OpenCV-compatible image
    // into the current_frame variable
    cv::Mat cv_image1 = cv_ptr1->image;
    cv::Mat cv_image2 = cv_ptr2->image;
    
    // horizontally concatenates images of same height  
    cv::Mat result;
    vconcat(cv_image1,cv_image2,result); 

    //----------------------------------  Display the current frame  ----------------------------------------
    //cv::imshow("result1", result);
    //cv::waitKey(30); // Display frame for 30 milliseconds

    //-------------------------------------  Publish the matches  ------------------------------------------- 
    finalImage_pub = cv_bridge::CvImage(std_msgs::Header(), "mono8", result).toImageMsg();
    //------------------------------------------------------------------------------------------------------- 
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("Could not convert from '%s' to 'bgr8'.", image1->encoding.c_str());
  }
}


int main(int argc, char** argv)
{
  // Initialize the ROS Node
  ros::init(argc, argv, "panorama_stitching");

  // Default handler for nodes in ROS
  ros::NodeHandle nh;
  ros::Rate r(10);

  // Subscribe to camera topics
  message_filters::Subscriber<Image> image1_sub(nh, "/camera1/front_right/image_raw", 1);
  message_filters::Subscriber<Image> image2_sub(nh, "/camera2/front_Left/image_raw", 1);

  typedef sync_policies::ApproximateTime<Image, Image> MySyncPolicy;
  // ApproximateTime takes a queue size as its constructor argument, hence MySyncPolicy(10)
  Synchronizer<MySyncPolicy> sync(MySyncPolicy(10), image1_sub, image2_sub);
  sync.registerCallback(boost::bind(&callback, _1, _2));

  //publishers
  image_transport::ImageTransport it(nh);
  image_transport::Publisher pub_result = it.advertise("/panorama_stitching/image_raw", 1);

  // Running at 10Hz
  ros::Rate loop_rate(10);

  while (ros::ok()) 
  {
    pub_result.publish(finalImage_pub);
    ros::spinOnce();
    loop_rate.sleep();
  }

  return 0;
}
