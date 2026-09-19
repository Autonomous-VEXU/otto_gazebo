#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch.conditions import IfCondition
from ros_gz_bridge.actions import RosGzBridge

def generate_launch_description():

    # directory paths
    this_pkg = get_package_share_directory('otto_gazebo')
    #scan_merger_pkg = get_package_share_directory('laser_scan_merger')

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

    logical_cams = LaunchConfiguration('logical_cams')
    logical_cams_cmd = DeclareLaunchArgument(
        'logical_cams',
        default_value='false',
        description='launches the ros gz bridge for the logical cameras'
    ) 

    rendered_cams = LaunchConfiguration('cams')
    rendered_cams_cmd = DeclareLaunchArgument(
        'cams',
        default_value='false',
        description='launches the ros gz bridge for the logical cameras'
    ) 

    # generate urdf file path
    urdf_path = PathJoinSubstitution([this_pkg, 'robot', 'otto.urdf.xacro'])
    
    # convert urdf (process at launch time)
    urdf = Command(['xacro ', urdf_path,
                    ' l_cams:=', logical_cams,
                    ' cams:=', rendered_cams])

    # gazebo --> ros bridge config file paths
    topic_bridge_config = PathJoinSubstitution([this_pkg, 'config', 'robot_bridge.yaml'])
    l_cams_bridge_config = PathJoinSubstitution([this_pkg, 'config', 'logical_camera_bridge.yaml'])
    cams_bridge_config = PathJoinSubstitution([this_pkg, 'config', 'camera_bridge.yaml'])

    # Gazebo Sim --> ROS topic bridge
    gazebo_bridge = RosGzBridge(
        bridge_name='otto_ros_bridge',
        config_file=topic_bridge_config
    )

    gazebo_bridge_l_cams = RosGzBridge(
        bridge_name='logical_cams_ros_bridge',
        config_file=l_cams_bridge_config,
        condition=IfCondition(logical_cams)
    )

    gazebo_bridge_cams = RosGzBridge(
        bridge_name='cams_ros_bridge',
        config_file=cams_bridge_config,
        condition=IfCondition(rendered_cams)
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


#    scan_merger = IncludeLaunchDescription(
#        PythonLaunchDescriptionSource(
#            os.path.join(scan_merger_pkg, 'launch', 'start.launch.py')
#        ),
#        launch_arguments={'robotname':'otto'}.items()
#    )
    scan_merger_left = Node(
            package='topic_tools',
            executable='relay',
            name='left_lidar_relay_node',
            output='screen',
            parameters=[{
                'input_topic': '/left_lidar/scan',
                'output_topic': '/scan_merged'
            }]
    )

           
    scan_merger_right = Node(
            package='topic_tools',
            executable='relay',
            name='right_lidar_relay_node',
            output='screen',
            parameters=[{
                'input_topic': '/right_lidar/scan',
                'output_topic': '/scan_merged'
            }]
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
        declare_x_position_cmd,
        declare_y_position_cmd,
        rendered_cams_cmd,
        logical_cams_cmd,
        gazebo_bridge,
        gazebo_bridge_cams,
        gazebo_bridge_l_cams,
        tf_st_bridge,
        robot_state_publisher_node,
        start_gazebo_ros_spawner_cmd,
        scan_merger_left,
        scan_merger_right,
        joint_state_broadcaster_spawner,
        omni_controller_spawner
    ])
