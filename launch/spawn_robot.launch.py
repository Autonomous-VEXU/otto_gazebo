#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression, PathJoinSubstitution, Command
from launch_ros.actions import Node
from ros_gz_bridge.actions import RosGzBridge

def generate_launch_description():

    # directory paths
    this_pkg = get_package_share_directory('otto_gazebo')
    scan_merger_pkg = get_package_share_directory('laser_scan_merger')

    # robot x pose argument
    x_pose = LaunchConfiguration('x_pose')
    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', 
        default_value='0.5',
        description='X position of the robot'
    )

    # robot y pose argument
    y_pose = LaunchConfiguration('y_pose')
    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', 
        default_value='1.0',
        description='Y position of the robot'
    ) 

    # urdf selection argument
    urdf_lite = LaunchConfiguration('robot_lite')
    declare_urdf_lite_cmd = DeclareLaunchArgument(
        'robot_lite',
        default_value='true',
        description='boolean to determine which urdf file to use (true = otto_lite.urdf.xacro)'
    )

    # conditionally select URDF file
    urdf_file_name = PythonExpression([
        "'otto.urdf.xacro' if '",
        urdf_lite,
        "' == 'false' else 'otto_lite.urdf.xacro'"
    ])

    # generate urdf file path
    urdf_path = PathJoinSubstitution([this_pkg, 'robot', urdf_file_name])
    
    # convert urdf (process at launch time)
    urdf = Command(['xacro ', urdf_path])

    # conditionally set gz_ros_bridge config file
    gz_bridge_config_name = PythonExpression([
        "'robot_bridge.yaml' if '",
        urdf_lite,
        "' == 'false' else 'robot_lite_bridge.yaml'"
    ])

    # gazebo --> ros bridge config file path
    topic_bridge_config = PathJoinSubstitution([this_pkg, 'config', gz_bridge_config_name])

    # Gazebo Sim --> ROS topic bridge
    gazebo_bridge = RosGzBridge(
        bridge_name='otto_ros_bridge',
        config_file=topic_bridge_config
    )

    # specific QoS for tf_static parameter bridge
    tf_st_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/tf_static@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V'
        ],
        parameters=[{'use_sim_time': True},
            {'qos_overrides./tf_static.publisher.reliability': 'reliable'},
            {'qos_overrides./tf_static.publisher.durability': 'transient_local'},
            {'qos_overrides./tf_static.publisher.history': 'keep_last'},
            {'qos_overrides./tf_static.publisher.depth': 1}
        ],
        output='screen'
    ) 

    # robot state publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': urdf},
            {'use_sim_time': True}
        ]
    ) 

    # laser_scan_merger launch file
    scan_merger = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(scan_merger_pkg, 'launch', 'start.launch.py')
        ),
        launch_arguments={'robotname':'otto'}.items()
    )

    # Gazebo Sim entity spawner
    start_gazebo_ros_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'Otto',
            '-topic', '/robot_description',
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01'
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # joint state broadcaster (controller_manager node)
    joint_state_broadcaster_spawner = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
                parameters=[{'use_sim_time': True}],
                output='screen'
            )
        ]
    )

    # omni controller spawner (controller_manager node)
    omni_controller_spawner = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['omni_wheel_drive_controller', '--controller-manager', '/controller_manager','--controller-ros-args','-r /omni_wheel_drive_controller/odom:=/odom',
                           '--controller-ros-args','-r /omni_wheel_drive_controller/cmd_vel:=/cmd_vel'],
                parameters=[{'use_sim_time': True}],
                remappings=[
                ('cmd_vel', '/cmd_vel'), 
                ('odom', '/odom'), 
                ],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        declare_urdf_lite_cmd,
        declare_x_position_cmd,
        declare_y_position_cmd,
        gazebo_bridge,
        tf_st_bridge,
        robot_state_publisher_node,
        start_gazebo_ros_spawner_cmd,
        scan_merger,
        joint_state_broadcaster_spawner,
        omni_controller_spawner
    ])
