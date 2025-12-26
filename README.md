# otto_gazebo
This package simulates a x-drive robot (Otto) using Gazebo Harmonic + ROS2 Jazzy Jalisco. Also contains configuration files for tele-op controllers, the omni wheel drive controller, AMCL launch + parameter file, and Navigation2 parameters. Works together with the `otto_bringup` and `otto_description` packages, which can be found in the [`Autonomous-VEXU/otto_bringup`](https://github.com/Autonomous-VEXU/otto_bringup) and [`Autonomous-VEXU/otto_description`](https://github.com/Autonomous-VEXU/otto_description) repositories.

### Table of Contents:
- [ROS Package Dependencies](#ros-package-dependencies)
- [Demo Instructions](#demo-instructions)
- [File Structure + Organization](#file-structure--organization)
- [Launch Files](#launch-files)
    - [`nav2_test_world.launch.py`](#nav2_test_worldlaunchpy)
    - [`nav2.launch.py`](#nav2launchpy)
    - [`spawn_robot.launch.py`](#spawn_robotlaunchpy)
    - [`localization.launch.py`](#localizationlaunchpy)
- [Nodes](#nodes)
    - [`localize.py`](#localizepy)
- [Resources + Docs](#resources--documentation)

## Demo Instructions
Example of things that can be done with the launch files in this package:
### **Nav2 in the base turtlebot3_world:** </br>
Terminal 1: `ros2 launch otto_gazebo nav2_test_world.launch.py`</br>
Terminal 2: `ros2 launch otto_gazebo nav2.launch.py`</br>

### **Tele-op Control:**</br>
Terminal 1: `ros2 launch pushback_sim world_select.launch.py world:=<world_name>`</br>
Terminal 2: `ros2 launch otto_gazebo spawn_robot.launch.py`</br>
Terminal 3: `ros2 launch otto_bringup controller.launch.py`</br>

### **Localizing with AMCL on the VEX field:** </br>
Terminal 1: `ros2 launch pushback_sim world_select.launch.py world:=<world_name>`</br>
Terminal 2: `ros2 launch otto_gazebo localization.launch.py`</br>

> **Note:** Do not forget to build the workspace by running `colcon build --symlink-install` and then `source install/setup.bash` inside of the workspace directory</br>

## File Structure + Organization:
```
otto_gazebo/
├── config/
│   ├── amcl.yaml
│   ├── nav2.yaml
│   ├── omni_wheel_params.yaml
│   ├── robot_bridge.yaml
│   └── robot_lite_bridge.yaml
├── launch/
│   ├── controller.launch.py
│   ├── nav2_test_world.launch.py
│   ├── nav2.launch.py
│   └── spawn_robot.launch.py
├── robot/
│   ├── otto_lite.urdf.xacro
│   └── otto.urdf.xacro
├── rviz/
│   └── amcl_test.rviz
├── src/
│   └── localize.py
├── CMakeLists.txt
└── package.xml
```

## Launch Files 
Moderately detailed descriptions about what each launch file does and its arguments plus which outside packages it references/uses. </br>

## nav2_test_world.launch.py
_Launches the demo world from the `turtlebot3_gazebo` package with Otto spawned in at x = 0.5, y = 0.5. </br>_
> There are no launch arguments for this launch file!

## nav2.launch.py
_Launches the main bringup node + Rviz for Navigation 2, should be used with `nav2_test_world.launch.py`_
```yaml
map: `package://turtlebot3_navigation2/map/map.yaml' # map file path for the world that is being used
params_file: `package://otto_gazebo/config/nav2.yaml' # params file that should be used
use_sim_time: true # toggle for using sim time (gz sim /clock) or not
```

## spawn_robot.launch.py
_Spawns the robot into a pre-existing Gazebo Sim world</br>_
```yaml
x_pose: 0 # x coordinate will the robot will spawn
y_pose: 0 # y coordinate will the robot will spawn
robot_lite: True # if true, will spawn the URDF model that has a better RTK
```

## localization.launch.py
_Starts AMCL + map server components of Nav2, also launches localize.py node to make the robot spin in place_
```yaml
use_sim_time: True # toggle for using sim time (gz sim /clock) or not
map: 'pushback_sim/maps/vax_field_map.yaml' # the file path to the map the map_server will use
amcl_config: 'otto_gazebo/config/amcl.yaml' # configuration file to use for amcl node
rviz_config: 'otto_gazebo/config/amcl_test.yaml' # configuration file to use for Rviz2 node
```

## Nodes
A few helper nodes that make testing more efficient.

## localize.py
_A python node that simply spins the robot in place, calls the two main AMCL services `/request_nomotion_update` and `/reinitalize_global_localization`, while publishing the average covariance from topic `/amcl_pose` in a more readable format_
> this node can be found in the `localization.launch.py` launch file

## Resources + Documentation:
Various links to docs that I thought were useful. YouTube is also a pretty good resource as there are a lot of robotics channels that cover ROS2 concepts and have Gazebo Sim tutorials.

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
