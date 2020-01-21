#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import rtde
import rtde_config 
import xmlrpclib
import netifaces as ni
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import numpy as np
import socket
import time
import json


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    # Add these headers to all responses
    def end_headers(self):
        self.send_header("Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleXMLRPCRequestHandler.end_headers(self)
        

conf = rtde_config.ConfigFile("/home/administrator/husky_ws/src/ur_pick/node/ur5_interface_configuration.xml")
output_names, output_types = conf.get_recipe('out')
rtde_proxy = rtde.RTDE("192.168.1.20", 30004)
rtde_proxy.connect()
if not rtde_proxy.send_output_setup(output_names, output_types):
    print('wrong config file')
    exit()



def get_tcp_pose():
    rtde_proxy.send_start()
    state = rtde_proxy.receive()
    tcp_pose = state.actual_TCP_pose
    rtde_proxy.send_pause()
    print(tcp_pose)
    return tcp_pose

def get_joint_angles():
    rtde_proxy.send_start()
    state = rtde_proxy.receive()
    joint_angles = state.actual_q
    rtde_proxy.send_pause()
    return joint_angles

def get_tcp_force():
    rtde_proxy.send_start()
    state = rtde_proxy.receive()
    tcp_pose = state.actual_TCP_pose
    rtde_proxy.send_pause()
    return tcp_pose

def get_robot_status():
    rtde_proxy.send_start()
    state = rtde_proxy.receive()
    rtde_proxy.send_pause()
    bits = state.robot_status_bits
    return bits

def get_saftey_mode():
    rtde_proxy.send_start()
    state = rtde_proxy.receive()
    mode_dig = state.safety_status_bits
    rtde_proxy.send_pause()
    return "{:011b}".format(mode_dig)[::-1]

def get_digital_input_bits():
    rtde_proxy.send_start()
    state = rtde_proxy.receive()
    digital = state.actual_digital_input_bits
    rtde_proxy.send_pause()
    return "{:011b}".format(digital)[::-1]

server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_multicall_functions()
server.register_function(get_tcp_pose,"get_tcp_pose")
server.register_function(get_tcp_force,"get_tcp_force")
server.register_function(get_joint_angles,"get_joint_angles")
server.register_function(get_robot_status,"get_robot_status")
server.register_function(get_saftey_mode,"get_saftey_mode")
server.register_function(get_digital_input_bits,"get_digital_input_bits")


server.serve_forever()
