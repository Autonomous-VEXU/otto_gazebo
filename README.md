# robot_gazebo
This package simulates a x-drive robot using Gazebo Harmonic + ROS2 Jazzy Jalisco. Also contains configuration files for tele-op controllers, the omni wheel drive controller, AMCL launch + parameter file, and Navigation2 parameters. Works together with the `robot_bringup` and `robot_description` packages, which can be found in the [`Autonomous-VEXU/vex_robot`](https://github.com/Autonomous-VEXU/vex_robot) repository.

### Table of Contents:
- [Demo Instructions](#demo-instructions)
- [File Organization](#file-structure--organization)
- [Launch Files](#launch-files)
    - [`controller.launch.py`](#controllerlaunchpy)
    - [`nav2_test_world.launch.py`](#nav2_test_worldlaunchpy)
    - [`nav2.launch.py`](#nav_2launchpy)
    - [`spawn_robot.launch.py`](#spawn_robotlaunchpy)
    - [`localization.launch.py`]()
- Nodes
- [Resources + Docs](#resources--documentation)

<!-- ## Required Packages
- ros_gz_sim
- ros2_control
- turtlebot3_navigation2
- teleop_twist_joy
- robot_description * 
- robot_bringup *

> \* = package located in the `Autonomous-VEXU/vex_robot` repository -->

## Demo Instructions
Example of things that can be done with the launch files in this package:
### **Nav2 in the base turtlebot3_world:** </br>
Terminal 1: `ros2 launch robot_gazebo nav2_test_world.launch.py`</br>
Terminal 2: `ros2 launch robot_gazebo nav2.launch.py`</br>

### **Tele-op Control:**</br>
Terminal 1: `ros2 launch robot_gazebo nav2_test_world.launch.py`</br>
Terminal 2: `ros2 launch robot_gazebo spawn_robot.launch.py`</br>
Terminal 3: `ros2 launch robot_gazebo controller.launch.py`</br>

### **Localizing with AMCL on the VEX field:** </br>
Terminal 1: `ros2 launch pushback_sim world_select.launch.py world:=<world_name>`</br>
Terminal 2: `ros2 launch robot_gazebo localization.launch.py`</br>

> **Note:** Do not forget to build the workspace by running `colcon build --symlink-install` and then `source install/setup.bash` inside of the workspace directory</br>

> **Note 2:** Terminal 1 in the "Tele-op Control" demo instructions can be replaces with any world launch file given it launches Gazebo Sim. If you are using your own world launch file, disregard the `x_pose` and `y_pose` launch arguments or tweak them to work for your setup.

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
├── maps/
│   ├── vex_field.launch.py
│   └── spawn_robot.launch.py
├── robot/
│   ├── robot_lite.urdf.xacro
│   └── x_drive.urdf.xacro
├── rviz/
│   └── amcl_test.rviz
├── src/
│   └── localize.py
├── CMakeLists.txt
└── package.xml
```

## Launch Files 
Moderately detialed descriptions about what each launch file does and its arguments plus which outside packages it references/uses. </br>

Argument formatting for this `README.md` file:</br>
```yaml
launch_arg_name: 'default_value' # argument description
```

## controller.launch.py
_Allows for driving the robot with a game controller, does this by publishing messages to `/cmd_vel`</br>_
```yaml
controller_name: 'xbox_controller.yaml' # name of the config file you want to use
joy_dev: 0 # Device and/or controller ID
publish_twist_stamped: true # Toggle for publishing Twist vs TwistStamped messages
```
> Referenced Packages: `teleop_twist_joy`, `joy`

## nav2_test_world.launch.py
_Launches the demo world from the `turtlebot3_gazebo` package. </br>_
\*\* There are no launch arguments for this launch file!
> Referenced Packages: `turtlebot3_gazebo`, `ros_gz_sim`

## nav_2.launch.py
_Launches the main bringup node + Rviz for Navigation 2._
```yaml
map: `package://turtlebot3_navigation2/map/map.yaml' # map file path for the world that is being used
params_file: `package://robot_gazebo/config/nav2.yaml' # params file that should be used
use_sim_time: true # toggle for using sim time (gz sim clock) or not
```
> Referenced Packages: `turtlebot3_navigation2`, `nav2_bringup`

## spawn_robot.launch.py
_Spawns the robot into a pre-existing Gazebo Sim session</br>_
```yaml
x_pose: 0 # x coordinate will the robot will spawn
y_pose: 0 # y coordinate will the robot will spawn
```
> Referenced Packages: `robot_description`, `robot_state_publisher`,`ros_gz_bridge`,`ros_gz_sim`,`controller_manager`

## Resources + Documentation:
Various links to docs that I thouhgt were useful. YouTube is also a pretty good resource as there are a lot of robotics channels that cover ROS2 concepts and have Gazebo Sim tutorials.
### ROS2 Documentation + Resources:
[ROS2 Documentation (Jazzy Jalisco)](https://docs.ros.org/en/jazzy/index.html)</br>
[Open Robotics Discourse](https://discourse.openrobotics.org)</br>
[Robotics Stack Exchange](https://robotics.stackexchange.com) </br>

### Core Packages + Software Documentation
[Nav2 Documentation](https://docs.nav2.org)</br>
[Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic/getstarted)</br>

### Other Resources and Links:
[Inertia Matrix Calculator: cylinder/wheels](https://amesweb.info/inertia/mass-moment-of-inertia-cylinder.aspx)</br>
[Inertia Matrix Calculator: rectangle/chassis](https://amesweb.info/inertia/moment-of-inertia-of-rectangular-plate.aspx)
