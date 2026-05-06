# 🤖 Differential Drive Robot with LiDAR & Ultrasonic Sensor
### ROS 2 Jazzy | Gazebo Harmonic | Python

![ROS2](https://img.shields.io/badge/ROS2-Jazzy-blue)
![Gazebo](https://img.shields.io/badge/Gazebo-Harmonic-orange)
![Python](https://img.shields.io/badge/Python-3.12-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Description

A fully simulated differential drive robot in **Gazebo Harmonic** with autonomous obstacle avoidance using a **LiDAR sensor** and **Ultrasonic sensor**. The robot uses a state machine to navigate, back up, and turn away from obstacles. Includes a **GUI control panel** and **RViz visualization**.

---

## 🎯 Features

- ✅ Differential drive robot simulation in Gazebo Harmonic
- ✅ 360° LiDAR sensor for full obstacle detection
- ✅ Ultrasonic sensor for close-range front detection
- ✅ Smart 4-state avoidance (Forward → Backup → Turn → Clear)
- ✅ GUI control panel with live sensor data
- ✅ Keyboard control (arrow keys)
- ✅ RViz visualization (3D view + sensor data)
- ✅ 7 colored obstacles + surrounding walls

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| ROS 2 | Jazzy | Robot operating system |
| Gazebo | Harmonic 8.11 | 3D physics simulation |
| Python | 3.12 | Robot logic & GUI |
| Ubuntu | 24.04 | Operating system |
| Tkinter | Built-in | GUI control panel |
| RViz2 | Jazzy | 3D visualization |

---

## 📁 Project Structure

```
ros2_ws/
└── src/
    └── diff_robot/
        ├── diff_robot/
        │   ├── __init__.py
        │   ├── robot_node.py          ← Main avoidance logic
        │   ├── ultrasonic_converter.py ← Sensor data converter
        │   └── gui_control.py         ← GUI + keyboard control
        ├── launch/
        │   └── robot.launch.py        ← Launch everything
        ├── worlds/
        │   └── robot_world.sdf        ← Gazebo world + robot
        ├── urdf/
        │   └── robot.urdf.xacro       ← Robot 3D model
        ├── package.xml
        └── setup.py
```

---

## ⚙️ Prerequisites

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic

---

## 🚀 Installation

**1 — Clone the repository:**
```bash
cd ~/ros2_ws/src
git clone https://github.com/YOUR_USERNAME/diff_robot.git
```

**2 — Install dependencies:**
```bash
sudo apt install ros-jazzy-ros-gz
sudo apt install ros-jazzy-xacro
sudo apt install ros-jazzy-robot-state-publisher
sudo apt install ros-jazzy-ros-gz-bridge
sudo apt install ros-jazzy-ros-gz-sim
sudo apt install ros-jazzy-rviz2
sudo apt install ros-jazzy-teleop-twist-keyboard
sudo apt install python3-tk
```

**3 — Build the package:**
```bash
cd ~/ros2_ws
colcon build --packages-select diff_robot
source install/setup.bash
```

---

## 🎮 Usage

**Launch the full simulation:**
```bash
ros2 launch diff_robot robot.launch.py
```

This opens:
- 🟦 **Gazebo** — 3D simulation world
- 📊 **RViz** — sensor visualization
- 🎮 **GUI Panel** — control buttons + live data

---

## 🕹️ Controls

| Key | Action |
|---|---|
| `↑` Arrow Up | Move Forward |
| `↓` Arrow Down | Move Backward |
| `←` Arrow Left | Turn Left |
| `→` Arrow Right | Turn Right |
| `Space` | Stop |

Or use the **GUI buttons** in the control panel.

---

## 🤖 Robot Specifications

| Component | Details |
|---|---|
| Body | 0.3 × 0.2 × 0.1 m blue box |
| Drive wheels | 2 × cylinder (r=0.04m) |
| Caster wheel | 1 × sphere (r=0.02m) |
| LiDAR | 360° scan, 0.12–10m range |
| Ultrasonic | Front only, 0.02–4m range |
| Max speed | 0.3 m/s forward |
| Turn speed | 0.8 rad/s |

---

## 🧠 Avoidance Logic

```
FORWARD → obstacle detected → BACKUP (2s) → TURNING → CLEAR → FORWARD
```

| State | Behavior |
|---|---|
| FORWARD | Move at 0.3 m/s until obstacle < 0.8m |
| BACKUP | Reverse at 0.2 m/s for 2 seconds |
| TURNING | Turn left at 0.8 rad/s until path clear |
| CLEAR | Wait 0.5s to confirm path is clear |

---

## 📡 ROS 2 Topics

| Topic | Type | Description |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/Twist` | Robot movement commands |
| `/scan` | `sensor_msgs/LaserScan` | LiDAR 360° data |
| `/ultrasonic_raw` | `sensor_msgs/LaserScan` | Ultrasonic sensor data |
| `/odom` | `nav_msgs/Odometry` | Robot position |

---

## 👤 Author

**Ahmed**
- Machine: HP Z230 Tower Workstation
- OS: Ubuntu 24.04

---

## 📄 License

This project is licensed under the MIT License.
