#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # package directories
    pkg_directory = get_package_share_directory('otto_gazebo')
    map_dir = get_package_share_directory('pushback_sim')

    # default file paths
    default_map = os.path.join(map_dir, 'maps', 'vex_field_map.yaml')
    default_amcl_config = os.path.join(pkg_directory, 'config', 'amcl.yaml')
    default_rviz_config = os.path.join(pkg_directory, 'rviz', 'amcl_test.rviz')
    default_rl_config = os.path.join(pkg_directory, 'config', 'robot_ekf.yaml')

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

    # AMCL parameter file launch argument
    amcl_config = LaunchConfiguration('amcl_config')
    amcl_config_cmd = DeclareLaunchArgument(
        'amcl_config',
        default_value=default_amcl_config,
        description='Nav2 amcl config file path'
    )

    # Rviz2 configuration file
    rviz_config = LaunchConfiguration('rviz_config')
    rviz_config_cmd = DeclareLaunchArgument(
        'rviz_config',
        default_value=default_rviz_config,
        description='Rviz2 configuration file'
    )

    # robot_localization configuration file
    rl_config = LaunchConfiguration('rl_config')
    rl_config_cmd = DeclareLaunchArgument(
        'rl_config',
        default_value=default_rl_config,
        description='config file path for robot_localization package'
    )

    # map server
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time, 'yaml_filename': map_file}]
    )

    # amcl node
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[amcl_config]
        # remappings=[('scan', '/scan')]
    )

    # lifecycle manager for Nav2 (amcl + map server nodes)
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time,
            'autostart': True,
            'node_names': ['map_server', 'amcl']}]
    )

    # Rviz
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-d', rviz_config],
        output='screen'
    )

    # robot_localization package (unused right now)
    robot_localization = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[rl_config],
    )
    
    return LaunchDescription([
        use_sim_time_cmd,
        map_file_cmd,
        rviz_config_cmd,
        amcl_config_cmd,
        rl_config_cmd,
        map_server,
        amcl,
        lifecycle_manager,
        rviz2,
    ])