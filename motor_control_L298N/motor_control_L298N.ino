/* 
 * rosserial ADC Example
 * 
 * This is a poor man's Oscilloscope.  It does not have the sampling 
 * rate or accuracy of a commerical scope, but it is great to get
 * an analog value into ROS in a pinch.
 */

#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <ros.h>
#include <rosserial_arduino/Adc.h>
#include <ArduinoHardware.h>
#include <ros.h>
#include <Servo.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Int64.h>
#include <std_msgs/Int16.h>
#include <std_msgs/UInt16.h>

// Handles startup and shutdown of ROS
ros::NodeHandle  nh;  
geometry_msgs::Twist msg;

// ******************************* Motor Controller Variables and Constants ***********************************

// Motor connections
const int pinENA = 6;
const int pinIN1 = 7;
const int pinIN2 = 8;

// Servo connections
#define servo_pin 9
Servo servo;

// Initial Motor speed and Servo position
int vel_linear;
int vel_linear_rect = 0;
int vel_angular; 
int vel_angular_rect;
int initial_servo_position = 90;
const int speed = 80;

// ******************************* ROS Motor/Servo control ***********************************

void velCallback(const geometry_msgs::Twist& vel)
{
  // Calculating speeds
  vel_linear = (vel.linear.x);
  vel_angular = (vel.angular.z);

  // Define motor speed
  int vel_linear_rect = map(vel_linear, 0, 100, 0 , 255); // Map the output value from 0 to 255
  analogWrite(ENB, vel_linear_rect); // Send PWM signal to L298N Enable pin

  // Define servo position taking into account that the center is 90º
  vel_angular_rect = (initial_servo_position + vel_angular);

  // Forward
  if(vel_linear > 0){
    digitalWrite(pinIN1, HIGH);
    digitalWrite(pinIN2, LOW);
    analogWrite(pinENA, speed);
    servo.write(vel_angular_rect);
  }

  // Back
  else if(vel_linear < 0) {
    digitalWrite(pinIN1, LOW);
    digitalWrite(pinIN2, HIGH);
    analogWrite(pinENA, speed);
    servo.write(vel_angular_rect);
  }
  
  //stop
  else {
    digitalWrite(pinIN1, LOW);
    digitalWrite(pinIN2, LOW);
    servo.write(vel_angular_rect);
  }
}

// Set up ROS subscriber to the velocity command
ros::Subscriber<geometry_msgs::Twist> subCmdVel("follow_topic",velCallback);

void setup() 
{
  // Motor control pins are outputs
  pinMode(pinIN1, OUTPUT);
  pinMode(pinIN2, OUTPUT);
  pinMode(pinENA, OUTPUT);

  // Set the motor speed
  //analogWrite(pinENA, 0);

  // Servo definition
  servo.attach(servo_pin);

  // Set the servo initial position
  servo.write(initial_servo_position);
  
  // ROS Setup
  nh.getHardware()->setBaud(57600);
  nh.initNode();
  nh.subscribe(subCmdVel);
}

// ******************************************************************************
void loop() {
  nh.spinOnce();
  delay(1);
} 
