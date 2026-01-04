#!/usr/bin/env python3

import rclpy
import subprocess
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped, PoseWithCovarianceStamped

class Localize(Node):
    def __init__(self):
        super().__init__("localize")

        self.log = self.get_logger().info

        # publishers and subscribers
        self.cmd_vel = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.amcl_pose = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.calc_covariance, 10)

        # self.average_cov = self.create_publisher(Float64, '/avg_covariance')

        # self.timer = self.create_timer(3.0, self.robot_actions)

        self.localized = False
        # self.avg_covariance = None
        self.est_pose = None

        # initial service call to start localizing
        self.reinitialize_global_localization()

    def calc_covariance(self, amcl:PoseWithCovarianceStamped):
        '''calculate average covariance and use result to change spinning vs. no spinning'''
        covariance = amcl.pose.covariance
        vals = []

        for value in covariance:
            if value > 0.0:
                vals.append(value)
        
        avg_covariance = sum(vals) / len(vals)
        self.est_pose = amcl.pose.pose.position
        self.log(f"Average Covariance: {avg_covariance}")

    def publish_spin(self, spin_speed:float):
        '''controls the speed of the robot spinning'''
        robot = TwistStamped()
        robot.twist.angular.z = spin_speed
        self.cmd_vel.publish(robot)

    def reinitialize_global_localization(self):
        '''call the reinitialize service service'''
        subprocess.run(['ros2', 'service', 'call', '/reinitialize_global_localization', 'std_srvs/srv/Empty','"{}"'])

    def nomotion_update(self):
        '''call nomotion_update service on a timer?'''
        subprocess.run(['ros2', 'service', 'call', '/request_nomotion_update', 'std_srvs/srv/Empty','"{}"'])
        
    def robot_actions(self):
        self.publish_spin(0.5)
        # self.get_logger().info(f'Average Covariance: {avg_covariance}')

def main(args=None):
    rclpy.init(args=args)
    node = Localize()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()