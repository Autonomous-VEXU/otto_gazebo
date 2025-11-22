#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    ## ============= File + Directory Paths ============== ##
    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    sim_robot_dir = get_package_share_directory('robot_gazebo')

    world = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'worlds',
        'turtlebot3_world.world'
    )

    ## ============= Gazebo Sim ============== ##
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r -s -v2 ', world], 'on_exit_shutdown': 'true', 'use_sim_time': 'true'}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-g -v2 ', 'on_exit_shutdown': 'true','use_sim_time': 'true'}.items()
    )

    ## ============= Environment Variables ============== ##
    set_env_vars_resources = AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            os.path.join(
                get_package_share_directory('turtlebot3_gazebo'),
                'models'))
    
    robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(sim_robot_dir, 'launch', 'spawn_robot.launch.py')
        ),
        launch_arguments={'x_pose': '0.5','y_pose':'0.5'}.items(),
    )

    return LaunchDescription([
        gzserver_cmd,
        gzclient_cmd,
        set_env_vars_resources,
        robot
    ])