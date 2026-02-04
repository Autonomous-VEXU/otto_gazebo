#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition

def generate_launch_description():

    # this package
    pkg_dir = get_package_share_directory('otto_gazebo')

    # parameter files for different bridges
    logical_cam_params = os.path.join(pkg_dir, 'config', 'logical_camera_bridge.yaml')
    cam_params = os.path.join(pkg_dir, 'config', 'camera_bridge.yaml')
    ground_truth = os.path.join(pkg_dir, 'config', 'ground_truth_pose.yaml')

    # launch args for the bridges
    lc_bridge = LaunchConfiguration('logical_cams')
    lc_bridge_cmd = DeclareLaunchArgument(
        'logical_cams', 
        default_value='false',
        description='launches the logical camera bridge node'
    )

    c_bridge = LaunchConfiguration('cams')
    c_bridge_cmd = DeclareLaunchArgument(
        'cams', 
        default_value='false',
        description='launches the camera bridge node'
    )

    ground_truth = LaunchConfiguration('ground_truth')
    gt_bridge_cmd = DeclareLaunchArgument(
        'ground_truth', 
        default_value='false',
        description='launches the ground truth bridge node'
    )

    logical_cam_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[logical_cam_params],
        name='logical_cam_bridge',
        condition=IfCondition(lc_bridge)
    )

    cams_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[cam_params],
        name='cams_bridge',
        condition=IfCondition(c_bridge)
    )

    ground_truth_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[ground_truth],
        name='robot_ground_truth',
        condition=IfCondition(ground_truth)
    )

    return LaunchDescription([
        lc_bridge_cmd,
        c_bridge_cmd,
        gt_bridge_cmd,
        logical_cam_bridge,
        cams_bridge,
        ground_truth_bridge
    ])