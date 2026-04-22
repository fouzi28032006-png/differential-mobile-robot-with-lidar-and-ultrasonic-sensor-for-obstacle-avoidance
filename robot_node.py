import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time

# --- NEW PARAMETERS ---
SAFE_DISTANCE = 0.8    # Start avoiding at 0.8m
CLEAR_DISTANCE = 1.2   # Distance needed to feel "safe" again
FORWARD_SPEED = 0.3
TURN_SPEED = 0.8       # Faster turn
TURN_DURATION = 2.0    # Turn for exactly 2 seconds

class DiffRobotNode(Node):
    def __init__(self):
        super().__init__('diff_robot_node')

        self.obstacle_detected = False
        self.distance = 999.0
        
        # Track when we started turning
        self.turn_start_time = 0.0
        self.is_turning = False

        # Subscribe directly to raw ultrasonic topic
        self.ultrasonic_sub = self.create_subscription(
            LaserScan,
            '/ultrasonic_raw',
            self.ultrasonic_callback,
            10)

        # Publisher for robot movement
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.timer = self.create_timer(0.1, self.move)
        self.get_logger().info('Differential robot node started with enhanced parameters!')

    def ultrasonic_callback(self, msg):
        if msg.ranges:
            valid = [r for r in msg.ranges if r > 0.01 and r < 4.0]
            self.distance = min(valid) if valid else 999.0
        else:
            self.distance = 999.0

        # Logic for detecting obstacles
        if self.distance < SAFE_DISTANCE:
            self.obstacle_detected = True
        elif self.distance > CLEAR_DISTANCE:
            self.obstacle_detected = False

        self.get_logger().info(f'Distance: {self.distance:.2f}m — Obstacle: {self.obstacle_detected}')

    def move(self):
        cmd = Twist()
        current_time = time.time()

        # If we are currently in a mandatory turn period
        if self.is_turning:
            if (current_time - self.turn_start_time) < TURN_DURATION:
                cmd.linear.x = 0.0
                cmd.angular.z = TURN_SPEED
                self.get_logger().info('Executing 2s escape turn...')
            else:
                self.is_turning = False # Turn finished
        
        # Normal behavior logic
        else:
            if not self.obstacle_detected:
                cmd.linear.x = FORWARD_SPEED
                cmd.angular.z = 0.0
                self.get_logger().info('Moving forward')
            else:
                # Start a new turn
                self.is_turning = True
                self.turn_start_time = current_time
                self.get_logger().info(f'Obstacle at {self.distance:.2f}m — starting turn!')

        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = DiffRobotNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()