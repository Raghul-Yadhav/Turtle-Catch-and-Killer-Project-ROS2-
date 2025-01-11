![Banner](https://github.com/Raghul-Yadhav/Turtle-Catch-and-Killer-Project-ROS2-/blob/main/banners/Your%20paragraph%20text.gif?raw=true)

# **Turtle Catch and Kill with ROS 2**

This project implements a multi-turtle management system using the `turtlesim` package in ROS 2. The main goal is to dynamically spawn multiple turtles in random co ordinates, monitor their positions, and control a primary turtle (`turtle1`) to navigate, "catch," and "remove" each target turtle from the simulation.

---

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Launch File](#launch-file)
- [Output Video](#output-video)
- [Future Improvements](#future-improvements)

---

## **Overview**

This project consists of a ROS 2 package that spawns multiple turtles in the `turtlesim` simulation environment and manages their interaction. The main functionalities include:
1. Spawning turtles dynamically.
2. Tracking and targeting turtles based on proximity.
3. Controlling `turtle1` to navigate to and "catch" (remove) the target turtle.
4. Killing the target turtle upon contact using a custom ROS 2 service.

---

## **Features**

- Dynamically spawns turtles in `turtlesim` using a timed spawning mechanism.
- Implements logic to find and target the closest turtle to `turtle1`.
- Allows toggling between "catch closest" or "catch first" modes.
- Includes a custom service (`catch_turtle`) to remove a target turtle.
- Demonstrates key ROS 2 concepts:
  - Custom messages and services.
  - Timers, publishers, and subscribers.
  - Integration of mathematical calculations for navigation.
- Includes a launch file to start the entire system seamlessly.

---

## **System Architecture**

This project uses a **ROS 2-based architecture** with the following key components:

1. **TurtleSpawnerNode**:
   - Periodically spawns turtles in random locations.
   - Publishes the list of active turtles (name, position) to the `/turtle_alive` topic.

2. **ControlTurtleNode**:
   - Tracks the position of `turtle1` and dynamically selects a target turtle based on the mode (`catch_closest_turtle`).
   - Sends velocity commands (`/turtle1/cmd_vel`) to control `turtle1`.
   - Uses the `/turtle1/pose` topic to monitor `turtle1`'s current position and orientation.
   - Calls the `catch_turtle` service to remove a turtle after reaching it.

3. **Custom ROS 2 Interfaces**:
   - Message: `ArrayTurtle` (list of active turtles with names and positions).
   - Service: `TurtleServer` (handles removal of turtles).

---

## **Installation**

Follow these steps to set up the project on your system:

### **Prerequisites**
- ROS 2 Humble installed (or another compatible version).
- `turtlesim` package.
- Python 3 and necessary dependencies installed.

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/<your_username>/turtlesim-multi-turtle-catcher.git
   cd turtlesim-multi-turtle-catcher
   ```
2. Build the workspace:
   ```bash
   colcon build
   ```
3. Source the workspace:
   ```bash
   source install/setup.bash
   ```
4. Launch the entire system:
   ```bash
   ros2 launch my_robot_bringup Turtle_Catch_and_Kill_app.launch.py
   ```

---

## **Usage**

### **Spawning Turtles**
The `TurtleSpawnerNode` spawns turtles at random positions at regular intervals.

### **Catching Turtles**
The `ControlTurtleNode`:
- Moves `turtle1` toward the target turtle.
- Automatically catches and removes the turtle upon contact.
- Publishes real-time velocity commands to `/turtle1/cmd_vel`.

---

## **Configuration**

### **Parameters**
Modify parameters directly in the code or create a configuration file:
- **`catch_closest_turtle`**:
  - Type: Boolean.
  - Description: If `True`, `turtle1` will target the closest turtle. Otherwise, it will target the first turtle in the list.
- **Spawning Interval**:
  - Adjust the timer period in the `TurtleSpawnerNode`.

---



## **Launch File**

The `turtle_catcher.launch.py` file simplifies the process of starting the project by launching:
1. The `turtlesim` node.
2. The `TurtleSpawnerNode` for spawning turtles.
3. The `ControlTurtleNode` for navigation and catching.

To run the launch file:
```bash
ros2 launch my_robot_bringup Turtle_Catch_and_Kill_app.launch.py
```

### **Example Launch File**

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld=LaunchDescription()
    Turtlesim_node = Node(
        package="turtlesim",
        executable="turtlesim_node"
    )
    
    turtle_controller_node = Node(
        package="turtle_catcher",
        executable="control_turtle",
        parameters = [
            {"Closest_turtle_first" : False}
        ]
    )
    
    turtle_spawner_node = Node(
        package="turtle_catcher",
        executable="spawn_turtle",
        parameters = [
            {"TimeInterval" : 1.0}
        ]
    )
    
    ld.add_action(Turtlesim_node)
    ld.add_action(turtle_controller_node)
    ld.add_action(turtle_spawner_node)
    return ld
```

---

## **Output Video**

The following video demonstrates the project in action. It shows:
1. Multiple turtles being spawned dynamically.
2. `turtle1` navigating toward and "catching" the turtles one by one.
3. Real-time turtle movements and interactions.

![Turtle Catch and Kill Demo](https://github.com/Raghul-Yadhav/Turtle-Catch-and-Killer-Project-ROS2-/blob/main/banners/Media2-ezgif.com-video-to-gif-converter.gif?raw=true)


---

## **Future Improvements**

- Add more complex navigation with obstacle avoidance.
- Visualize turtle tracking in RViz.
- Implement logging or debugging tools for real-time monitoring.
- Introduce new modes (e.g., prioritize specific turtles).


