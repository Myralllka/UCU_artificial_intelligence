#!/usr/bin/env python

# to start: rosrun moving src/listener.py
import rospy
from std_msgs.msg import String
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist

def callback(data):
#    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose)
    
    movement_publisher= rospy.Publisher('cmd_vel', Twist , queue_size=10)
    movement_cmd = Twist()
    movement_cmd.linear.x = data.pose[2].position.x - data.pose[1].position.x - 1
    movement_cmd.linear.y = data.pose[2].position.y - data.pose[1].position.y - 1
    movement_cmd.linear.z = 0
    movement_cmd.angular.x = 0
    movement_cmd.angular.y = 0              
    movement_cmd.angular.z = 0	
    movement_publisher.publish(movement_cmd)    
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/gazebo/model_states", ModelStates, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

