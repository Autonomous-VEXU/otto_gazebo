#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    otto_nav = get_package_share_directory('otto_navigation')

    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='toggle using the Gz Sim clock or PC clock'
    )

    ko_map_name = LaunchConfiguration('ko_map_name')
    ko_map_name_cmd = DeclareLaunchArgument(
        'ko_map_name',
        default_value='keepout_full_goal.yaml',
        description='keepout map file name from otto_navigation/maps directory'
    ) 

    keepout_mask_file = PathJoinSubstitution([otto_nav, 'maps', ko_map_name])

    keepout_info_params = {
        'use_sim_time': use_sim_time,
        'type': 0,
        'filter_info_topic': '/costmap_filter_info',
        'mask_topic': '/keepout_filter_mask',
        'base': 0.0,
        'multiplier': 1.0
    }

    keepout_mask_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='keepout_filter_mask_server',
        parameters=[{
            'use_sim_time': use_sim_time,
            'yaml_filename': keepout_mask_file,
            'topic_name': 'keepout_filter_mask',
            'frame_id': 'map'
        }],
        output='screen'
    )

    keepout_info_server = Node(
        package='nav2_map_server',
        executable='costmap_filter_info_server',
        name='keepout_costmap_filter_info_server',
        parameters=[keepout_info_params],
        output='screen'
    )

    keepout_lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_costmap_filters',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart': True,
            'node_names': ['keepout_filter_mask_server', 'keepout_costmap_filter_info_server']
        }]
    )

    return LaunchDescription([
        ko_map_name_cmd,
        use_sim_time_cmd,
        keepout_mask_server,
        keepout_info_server,
        keepout_lifecycle_manager,
    ])