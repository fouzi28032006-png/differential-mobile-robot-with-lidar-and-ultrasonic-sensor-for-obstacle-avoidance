import xacro
import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory('diff_robot')
    world = os.path.join(pkg, 'worlds', 'robot_world.sdf')

    return LaunchDescription([

        # Start Gazebo
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world],
            output='screen'),
        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': xacro.process_file(
                    os.path.join(
                        get_package_share_directory('diff_robot'),
                        'urdf', 'robot.urdf.xacro'
                    )
                ).toxml(),
                'use_sim_time': True
            }],
            output='screen'),

        # Bridge topics after 5 seconds
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                  arguments=[
                        '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                        '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
                        '/ultrasonic_raw@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                        '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                        '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
                        '/tf_static@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
                    ],
                    output='screen'),
            ]),

        # Robot node after 6 seconds
        TimerAction(
            period=6.0,
            actions=[
                Node(
                    package='diff_robot',
                    executable='robot_node',
                    name='robot_node',
                    output='screen'),
            ]),

        # RViz after 6 seconds
        TimerAction(
            period=6.0,
            actions=[
                Node(
                    package='rviz2',
                    executable='rviz2',
                    name='rviz2',
                    output='screen'),
            ]),

        # GUI Control panel after 6 seconds
        TimerAction(
            period=6.0,
            actions=[
                Node(
                    package='diff_robot',
                    executable='gui_control',
                    name='gui_control',
                    output='screen'),
            ]),
    ])