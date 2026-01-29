import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pb_sim = get_package_share_directory('pushback_sim')
    otto_gz = get_package_share_directory('otto_gazebo')

    vex_map_file = os.path.join(pb_sim, 'maps', 'vex_field_map.yaml')
    keepout_mask_file = os.path.join(pb_sim, 'maps', 'keepout_full_goal.yaml')

    keepout_info_params = {
        'use_sim_time': True,
        'type': 0,
        'filter_info_topic': '/costmap_filter_info',
        'mask_topic': '/keepout_filter_mask',
        'base': 0.0,
        'multiplier': 1.0
    }

    world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pb_sim, 'launch', 'world_select.launch.py')),
        launch_arguments={'world': 'empty_field'}.items()
    )

    otto = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(otto_gz, 'launch', 'spawn_robot.launch.py')),
        launch_arguments={'x_pose': '0.5','y_pose':'0.5'}.items()
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(otto_gz, 'launch', 'nav2.launch.py')),
        launch_arguments={'map': vex_map_file}.items()
    )

    keepout_mask_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='keepout_filter_mask_server',
        parameters=[{
            'use_sim_time': True,
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
            'use_sim_time': True,
            'autostart': True,
            'node_names': ['keepout_filter_mask_server', 'keepout_costmap_filter_info_server']
        }]
    )

    nav2_delay = TimerAction(
        period=3.0,
        actions=[nav2]
    )

    return LaunchDescription([
        world,
        otto,
        keepout_mask_server,
        keepout_info_server,
        keepout_lifecycle_manager,
        nav2_delay
    ])