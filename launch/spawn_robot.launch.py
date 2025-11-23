#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ros_gz_bridge.actions import RosGzBridge
import xacro

def generate_launch_description():
   
    ## ============= URDF Path + Conversion ============== ##
    urdf_path = os.path.join(
        get_package_share_directory('robot_gazebo'),
        'robot',
        'x_drive.urdf.xacro'
    )

    urdf = xacro.process_file(urdf_path).toxml()
    
    ## ============= X and Y Spawn Position ============== ##
    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', 
        default_value='0.0',
        description='X position of the robot'
    )

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', 
        default_value='2.0',
        description='Y position of the robot'
    ) 

    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')

    ## ============= Robot State Publisher ============== ##
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': urdf},
            {'use_sim_time': True}
        ]
    ) 

    ## ============= Gazebo <--> ROS Bridge ============== ##
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',  # make sure this is a [ not an @
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    tf_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V'
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )   
    
    sensor_msg_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan_1@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/scan_2@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

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

    image_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cam1/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/cam1/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/cam2/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/cam2/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/cam3/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/cam3/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/cam4/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/cam4/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo'
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # bridge_name = LaunchConfiguration('bridge_name')
    # config_file = LaunchConfiguration('config_file')

    # declare_bridge_name_cmd = DeclareLaunchArgument(
    #     'bridge_name', description='Name of ros_gz_bridge node'
    # )

    # declare_config_file_cmd = DeclareLaunchArgument(
    #     'config_file', description='YAML config file'
    # )

    # # Create the launch description and populate

    # gazebo_bridge = RosGzBridge(
    #     bridge_name=LaunchConfiguration('bridge_name'),
    #     config_file=LaunchConfiguration('config_file'),
    # )

    ## ============= Gazebo Sim ============== ##
    start_gazebo_ros_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'vex_robot',
            '-topic', '/robot_description',
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01'
        ],
        parameters=[{'use_sim_time': True}],
        output='screen',

    )

    ## ============= Controller Managers ============== ##
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
        clock_bridge,
        robot_state_publisher_node,
        start_gazebo_ros_spawner_cmd,
        tf_bridge,
        tf_st_bridge,
        sensor_msg_bridge,
        image_bridge,
        joint_state_broadcaster_spawner,
        omni_controller_spawner
    ])