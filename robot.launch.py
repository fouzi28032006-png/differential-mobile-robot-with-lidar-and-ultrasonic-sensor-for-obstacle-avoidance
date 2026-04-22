import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('diff_robot')
    world = os.path.join(pkg, 'worlds', 'robot_world.sdf')
    urdf = os.path.join(pkg, 'urdf', 'robot.urdf.xacro')

    # Process xacro
    robot_description = xacro.process_file(urdf).toxml()

    return LaunchDescription([

        # Start Gazebo Harmonic
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world],
            output='screen'),

        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'),

        # Spawn robot - delayed to wait for Gazebo
        TimerAction(
            period=3.0,
            actions=[
                Node(
                    package='ros_gz_sim',
                    executable='create',
                    arguments=[
                        '-topic', 'robot_description',
                        '-entity', 'diff_robot',
                        '-x', '0.0',
                        '-y', '0.0',
                        '-z', '0.1'],
                    output='screen'),
            ]),

        # Bridge topics between Gazebo and ROS 2
        TimerAction(
            period=4.0,
            actions=[
                Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                    arguments=[
                        '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                        '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
                        '/ultrasonic_raw@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                    ],
                    output='screen'),
            ]),

        # Ultrasonic converter node
        Node(
            package='diff_robot',
            executable='robot_node',
            name='robot_node',
            output='screen'),
            
        # Ultrasonic converter
        Node(
            package='diff_robot',
            executable='ultrasonic_converter',
            name='ultrasonic_converter',
            output='screen'),    
     
    ])