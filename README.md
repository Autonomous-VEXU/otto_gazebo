# robot_gazebo
Gazebo Harmonic implementation of an x drive holonomic robot.

Package File Tree:
```
/robot_gazebo
├── /config
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

Inertia Matrix Calculators:</br>
[cylinder/wheels](https://amesweb.info/inertia/mass-moment-of-inertia-cylinder.aspx)</br>
[rectangle/chassis](https://amesweb.info/inertia/moment-of-inertia-of-rectangular-plate.aspx)
