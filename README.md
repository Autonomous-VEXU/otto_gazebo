# robot_gazebo
Gazebo Harmonic implementation of an x drive holonomic robot.

## Required Packages
- ros_gz_sim
- ros2_control
- navigation2
- teleop_twist_joy
- robot_description
- robot_bringup


## ROS Resources:
[ROS2 Jazzy Jalisco Documentation](https://docs.ros.org/en/jazzy/index.html)</br>
[Nav2 Documentation](https://docs.nav2.org)</br>
[Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic/getstarted)</br>
[Open Robotics Discourse](https://discourse.openrobotics.org)</br>
[Robotics Stack Exchange](https://robotics.stackexchange.com)

## Package File Structure:
```
/robot_gazebo
├── /config
│   ├── nav2.yaml
│   ├── omni_wheel_params.yaml
│   ├── x_drive_bridge.yaml
│   └── xbox_controller.yaml
├── /launch
│   ├── controller.launch.py
│   ├── empty_world.launch.py
│   └── spawn_robot.launch.py
├── /models
│   └── x_drive.urdf.xacro
├── CMakeLists.txt
└── package.xml
```
## Instructions
To spawn the robot in a pre-existing Gazebo Sim session:</br>
`ros2 launch robot_gazebo spawn_robot.launch.py`</br>

To start tele-op mode after spawning the robot in: </br>
`ros2 launch robot_gazebo controller.launch.py`</br>

> NB: Do not forget to build the workspace by running `colcon build --symlink-install` and then `source install/setup.bash` inside of the workspace directory

## Other Resources and Links:
Inertia Matrix Calculators:</br>
[cylinder/wheels](https://amesweb.info/inertia/mass-moment-of-inertia-cylinder.aspx)</br>
[rectangle/chassis](https://amesweb.info/inertia/moment-of-inertia-of-rectangular-plate.aspx)
