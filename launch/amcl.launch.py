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

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    pkg_directory = get_package_share_directory('robot_gazebo')

    map_file = LaunchConfiguration( 'map', default=os.path.join( 
            get_package_share_directory('turtlebot3_navigation2'),
            'map',
            'map.yaml')
    )

    param_file = LaunchConfiguration('params_file', default=os.path.join( pkg_directory, 'config', 'amcl.yaml'))

    robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_directory, 'launch', 'nav2_test_world.launch.py')
        )
    )

    # amcl params
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'yaml_filename': map_file}]
    )

    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[param_file]
        # remappings=[('scan', '/scan')]
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time,
                    'autostart': True,
                    'node_names': ['map_server', 'amcl']}]
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        robot,
        map_server,
        amcl,
        lifecycle_manager,
        rviz2
    ])