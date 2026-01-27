#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # package directories
    
    map_dir = get_package_share_directory('pushback_sim')

    # default file paths
    default_map = os.path.join(map_dir, 'maps', 'vex_field_map.yaml')
   
    # use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time', 
        default_value='true', 
        description='toggle for using the gazebo clock'
    )

    # map file launch argument
    map_file = LaunchConfiguration('map')
    map_file_cmd = DeclareLaunchArgument( 
        'map', 
        default_value=default_map, 
        description='map server map file path'
    )

    # map server
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'yaml_filename': map_file}]
    )

    # lifecycle manager for Nav2 (amcl + map server nodes)
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time,
            'autostart': True,
            'node_names': ['map_server']}]
    )
    
    return LaunchDescription([
        use_sim_time_cmd,
        map_file_cmd,
        map_server,
        lifecycle_manager
    ])