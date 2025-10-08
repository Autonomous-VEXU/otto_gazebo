# robot_gazebo
Simulated x-drive robot using Gazebo Harmonic + ROS2 Jazzy Jalisco

## Required Packages
- ros_gz_sim
- ros2_control
- turtlebot3_navigation2
- teleop_twist_joy
- robot_description * 
- robot_bringup *

> \* = package located in the `Autonomous-VEXU/vex_robot` repository

## File Structure + Organization:
```
robot_gazebo/
├── config/
│   ├── nav2.yaml
│   ├── omni_wheel_params.yaml
│   ├── x_drive_bridge.yaml
│   └── xbox_controller.yaml
├── launch/
│   ├── controller.launch.py
│   ├── nav2_test_world.launch.py
│   ├── nav2.launch.py
│   └── spawn_robot.launch.py
├── models/
│   └── x_drive.urdf.xacro
├── CMakeLists.txt
└── package.xml
```
<!-- ## Launch Files
Here are descriptions for each launch file found in `robot_gazebo`.  -->

<!-- ## controller.launch.py
_Starts tele-op control for a already spawned in robot by publishing messages to `/cmd_vel`</br>_
```yaml
controller_name: 'xbox_controller.yaml' # name of the config file you want to use
joy_dev: 0 # Device and/or controller ID
publish_twist_stamped: true # Toggle for publishing Twist vs TwistStamped messages
``` -->

<!-- ### `nav2_test_world.launch.py`
Launches the demo world from the `turtlebot3_gazebo` package. -->

<!-- ### `nav_2.launch.py` -->

<!-- ### `spawn_robot.launch.py`
Spawns the robot into a pre-existing Gazebo Sim session</br>
`x_pose`: x coordinate will the robot will spawn</br>
`y_pose`: y coordinate will the robot will spawn</br> -->

<!-- > **NB:** Do not forget to build the workspace by running `colcon build --symlink-install` and then `source install/setup.bash` inside of the workspace directory -->

## ROS2 Resources:
[ROS2 Documentation (Jazzy Jalisco)](https://docs.ros.org/en/jazzy/index.html)</br>
[Nav2 Documentation](https://docs.nav2.org)</br>
[Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic/getstarted)</br>
[Open Robotics Discourse](https://discourse.openrobotics.org)</br>
[Robotics Stack Exchange](https://robotics.stackexchange.com)

## Other Resources and Links:
Inertia Matrix Calculators:</br>
[cylinder/wheels](https://amesweb.info/inertia/mass-moment-of-inertia-cylinder.aspx)</br>
[rectangle/chassis](https://amesweb.info/inertia/moment-of-inertia-of-rectangular-plate.aspx)
