#!/usr/bin/env python3
import rospy
from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow,atan2,sqrt

class turtlebot():

    def __init__(self):
        #Creating our node,publisher and subscriber
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber1 = rospy.Subscriber('/turtle1/pose', Pose, self.callback1)
        self.pose1 = Pose()
        
        self.velocity_publisher2 = rospy.Publisher('/turtle5/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber2 = rospy.Subscriber('/turtle5/pose', Pose, self.callback2)
        self.pose2 = Pose()
        
        
        self.rate = rospy.Rate(10)

    #Callback function implementing the pose value received
    def callback1(self, data1):
        self.pose1 = data1
        
        self.pose1.x = round(self.pose1.x, 4)
        self.pose1.y = round(self.pose1.y, 4)
     
        
        
    
    
    def callback2(self, data2):
        self.pose2 = data2
        self.pose2.x = round(self.pose2.x, 4)
        self.pose2.y = round(self.pose2.y, 4)
    
    
    def move2goal(self):
        goal_pose1 = Pose()
        goal_pose2 = Pose()

        goal_pose1.x = int(input("Set your x goal:"))
        goal_pose1.y = int(input("Set your y goal:"))

        distance_tolerance = float(input("Set your tolerance:"))
        goal_pose2.x = self.pose1.x
        goal_pose2.y = self.pose1.y

        
        vel_msg1 = Twist()
        vel_msg2 = Twist()


        while sqrt(pow((goal_pose1.x - self.pose1.x), 2) + pow((goal_pose1.y - self.pose1.y), 2)) >= distance_tolerance:

            #Porportional Controller
            #linear velocity in the x-axis:
            vel_msg1.linear.x = 1.5 * sqrt(pow((goal_pose1.x - self.pose1.x), 2) + pow((goal_pose1.y - self.pose1.y), 2))
            vel_msg1.linear.y = 0
            vel_msg1.linear.z = 0

            #angular velocity in the z-axis:
            vel_msg1.angular.x = 0
            vel_msg1.angular.y = 0
            vel_msg1.angular.z = 4 * (atan2(goal_pose1.y - self.pose1.y, goal_pose1.x - self.pose1.x) - self.pose1.theta)

            #Publishing our vel_msg1
            self.velocity_publisher1.publish(vel_msg1)
            self.rate.sleep()
        #Stopping our robot after the movement is over
        vel_msg1.linear.x = 0
        vel_msg1.angular.z =0
        self.velocity_publisher1.publish(vel_msg1)


        while sqrt(pow((goal_pose2.x - self.pose2.x), 2) + pow((goal_pose2.y - self.pose2.y), 2)) >= distance_tolerance:

            #Porportional Controller
            #linear velocity in the x-axis:
            vel_msg2.linear.x = 1.5 * sqrt(pow((goal_pose2.x - self.pose2.x), 2) + pow((goal_pose2.y - self.pose2.y), 2))
            vel_msg2.linear.y = 0
            vel_msg2.linear.z = 0

            #angular velocity in the z-axis:
            vel_msg2.angular.x = 0
            vel_msg2.angular.y = 0
            vel_msg2.angular.z = 4 * (atan2(goal_pose2.y - self.pose2.y, goal_pose2.x - self.pose2.x) - self.pose2.theta)

            #Publishing our vel_msg2
            self.velocity_publisher2.publish(vel_msg2)
            self.rate.sleep()
        #Stopping our robot after the movement is over
        vel_msg2.linear.x = 0
        vel_msg2.angular.z =0
        self.velocity_publisher2.publish(vel_msg2)

        rospy.spin()

if __name__ == '__main__':
    try:
        #Testing our function
        x = turtlebot()
        x.move2goal()

    except rospy.ROSInterruptException: pass