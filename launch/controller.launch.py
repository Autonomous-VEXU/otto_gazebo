import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch_ros.actions import Node

def generate_launch_description():
    joy_dev = launch.substitutions.LaunchConfiguration('joy_dev')
    publish_stamped_twist = launch.substitutions.LaunchConfiguration('publish_stamped_twist')

    config_path = os.path.join(
        get_package_share_directory('robot_gazebo'),
        'config',
        'xbox_controller.yaml'
    )

    joy_node = Node(
        package='joy', 
        executable='joy_node', 
        name='joy_node',
        parameters=[{'device_id': joy_dev, 'deadzone': 0.3, 'autorepeat_rate': 20.0,}, 
                    config_path]
    )

    teleop_node = Node(
        package='teleop_twist_joy', 
        executable='teleop_node',
        name='teleop_twist_joy_node',
        parameters=[config_path, 
                    {'publish_stamped_twist': publish_stamped_twist}, 
                    {'require_enable_button': False}],
        remappings={('/cmd_vel', '/omni_wheel_drive_controller/cmd_vel')}
    )

    return launch.LaunchDescription([
        # args
        launch.actions.DeclareLaunchArgument('joy_dev', default_value='0'),
        launch.actions.DeclareLaunchArgument('publish_stamped_twist', default_value='true'),

        # nodes
        joy_node,
        teleop_node
    ])