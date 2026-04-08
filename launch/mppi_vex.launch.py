import os

from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # file + directory paths
    pb_sim = get_package_share_directory('pushback_sim')
    otto_gz = get_package_share_directory('otto_gazebo')
    otto_nav = get_package_share_directory('otto_navigation')

    vex_map_file = os.path.join(otto_nav, 'maps', 'vex_field_map.yaml')

    # world launch file
    world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pb_sim, 'launch', 'world_select.launch.py')),
        launch_arguments={'world': 'empty_field'}.items()
    )

    # spawn robot
    otto = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(otto_gz, 'launch', 'spawn_robot.launch.py')),
        launch_arguments={'x_pose': '0.5','y_pose':'0.5'}.items()
    )

    # nav2
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(otto_gz, 'launch', 'nav2.launch.py')),
        launch_arguments={'map': vex_map_file}.items()
    )

    nav2_delay = TimerAction(
        period=3.0,
        actions=[nav2]
    )

    return LaunchDescription([
        world,
        otto,
        nav2_delay
    ])