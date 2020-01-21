#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================
import sys
sys.path.append('/home/administrator/husky_ws/src/ur_pick/node/') 
import intf_arm_ur5
#===============================================

#Imports
from ar_track_alvar_msgs.msg import AlvarMarkers
from move_base_msgs.msg import MoveBaseActionResult
import rospy
import time
import tf
import math

class Grasp(object):
    def __init__(self):
        rospy.init_node('pick_node',anonymous=True)
        self.target_pose = None
        self.target_orientation = None
        self.ur5 = intf_arm_ur5.UR5()
        self.nav_result = MoveBaseActionResult()
        self.ready_pose = [0.10880633619503582, 0.4863965763642277, 0.4301484945795706, -0.0020035179685886618, -3.1253770302989254, 0.0030656173756715573]
        self.pick_pose = self.ready_pose[:]
        #self.start_pose = [0.12659056976406824, -0.10998811702626762, 0.17083575798211992, 0.002197744125332058, -2.835318895178615, 0.00023324024578012803]
        rospy.Subscriber('/ar_pose_marker', AlvarMarkers, self.object_callback)
        rospy.Subscriber('/move_base/result', MoveBaseActionResult, self.nav_callback)
        self.curent_pose = self.ur5.get_tcp_pose_vec()
        print self.curent_pose
        self.flag = False
        self.ur5.movel(self.start_pose)

    def nav_callback(self,res_msg):
        self.nav_result = res_msg
        if(self.nav_result.status.text == 'Goal reached.'):
            self.ur5.movel(self.ready_pose)
            time.sleep(2)
            self.flag = True
            print("Ready to pick.")

    def object_callback(self,msg):
        if len(msg.markers) > 0: 
            self.target_orientation = tf.transformations.euler_from_quaternion([msg.markers[0].pose.pose.orientation.x, msg.markers[0].pose.pose.orientation.y,msg.markers[0].pose.pose.orientation.z,msg.markers[0].pose.pose.orientation.w])
            self.target_pose = [msg.markers[0].pose.pose.position.x -  0.0304004096392, msg.markers[0].pose.pose.position.y - 0.0562846137435, msg.markers[0].pose.pose.position.z -0.03, self.target_orientation[2]]
            if self.flag :
                self.pick_pose[0] -= self.target_pose[1]
                self.pick_pose[1] -= self.target_pose[0]
                self.pick_pose[2] -= self.target_pose[2] 
                self.ur5.movel(self.pick_pose)
                time.sleep(4)
                print("Got it.")
                self.ur5.movel(self.ready_pose)
                time.sleep(4)
                self.ur5.movel(self.start_pose)
                self.pick_pose = self.ready_pose[:]
                self.flag = False
            


if __name__=='__main__':
        Grasp()
        rospy.spin()
