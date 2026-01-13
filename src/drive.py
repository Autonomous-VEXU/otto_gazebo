
import rclpy
from rclpy.node import Node


class PathFollower(Node):
    def __init__(self, max_linear_speed, max_angular_speed):
        super().__init__('drive')

        # subscribe to robot pose for driving path
        # publish to cmd_vel

        # global variables for max linear and angular speed

    def robot_position(self, msg):
        '''callback to update the robot's position'''
        pass

    def publish_speed(self, linear:float, angular:float):
        '''publish speed to /cmd_vel topic'''
        pass

    def drive(self, meters):
        '''function for driving a certain distance forwards'''
    
    def turn(self, angle):
        '''turn the robot a specific number of deg'''
        pass

    def drive_path(self, path):
        '''path to drive'''
