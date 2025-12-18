#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    ## ============= Launch Configs ============== ##
    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')
    rviz_config_dir = os.path.join(get_package_share_directory('turtlebot3_navigation2'),'rviz','tb3_navigation2.rviz')

    map_dir = LaunchConfiguration(
        'map',
        default=os.path.join(
            get_package_share_directory('turtlebot3_navigation2'),
            'map',
            'map.yaml')
    )

    param_dir = LaunchConfiguration(
        'params_file',
        default=os.path.join(
            get_package_share_directory('otto_gazebo'),
            'config',
            'nav2.yaml')
    )
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    ## ============= Launch Arguments ============== ##
    map_launch_arg = DeclareLaunchArgument(
        'map',
        default_value=map_dir,
        description='Full path to map file to load'
    )
    
    config_launch_arg = DeclareLaunchArgument(
        'params_file',
        default_value=param_dir,
        description='Full path to param file to load'
    )

    sim_time_launch_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    
    ## ============= Nav2 Launch File ============== ##
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
        launch_arguments={
            'map': map_dir,
            'use_sim_time': use_sim_time,
            'params_file': param_dir}.items()
    )

    ## ============= Rviz Node ============== ##
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        map_launch_arg,
        config_launch_arg,
        sim_time_launch_arg,
        nav2_launch,
        rviz2
    ])