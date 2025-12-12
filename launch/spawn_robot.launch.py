#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
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

    no_cams_urdf =  os.path.join(
        get_package_share_directory('robot_gazebo'),
        'robot',
        'robot_lite.urdf.xacro'
    )
    
    urdf = xacro.process_file(no_cams_urdf).toxml()

    topic_bridge_config = os.path.join(
        get_package_share_directory('robot_gazebo'),'config','robot_lite_bridge.yaml'
    )
    
    ## ============= X and Y Spawn Position ============== ##
    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', 
        default_value='0.5',
        description='X position of the robot'
    )

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', 
        default_value='1.0',
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
   
    declare_bridge_name_cmd = DeclareLaunchArgument(
        'bridge_name', default_value="ros_bridge", description='Name of ros_gz_bridge node'
    )

    declare_config_file_cmd = DeclareLaunchArgument(
        'config_file', default_value=topic_bridge_config, description='YAML config file'
    )

    gazebo_bridge = RosGzBridge(
        bridge_name=LaunchConfiguration('bridge_name'),
        config_file=LaunchConfiguration('config_file'),
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

    ## ============= LiDAR Specific ============== ##
    lidar_scan_toggle = Node(
            package='topic_tools',
            executable='mux',
            name='mux_laser_scan', 
            arguments=[
                'scan',
                'scan_1',
                'scan_2'
            ],
            output='screen'
    )

    scan_merger_pkg = get_package_share_directory('laser_scan_merger')

    scan_merger = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(scan_merger_pkg, 'launch', 'start.launch.py')
        ),
        launch_arguments={'robotname':'x_drive'}.items()
    )

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
        output='screen'
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
        declare_config_file_cmd,
        declare_bridge_name_cmd,
        gazebo_bridge,
        tf_st_bridge,
        robot_state_publisher_node,
        start_gazebo_ros_spawner_cmd,
        lidar_scan_toggle,
        # scan_merger,
        joint_state_broadcaster_spawner,
        omni_controller_spawner
    ])
