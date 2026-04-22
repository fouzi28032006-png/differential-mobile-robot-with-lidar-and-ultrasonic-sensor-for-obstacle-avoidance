import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32

class UltrasonicConverter(Node):
    def __init__(self):
        super().__init__('ultrasonic_converter')

        self.sub = self.create_subscription(
            LaserScan,
            '/ultrasonic_raw',
            self.callback,
            10)

        self.pub = self.create_publisher(
            Float32,
            '/ultrasonic',
            10)

        self.get_logger().info('Ultrasonic converter started!')

    def callback(self, msg):
        distance = Float32()
        # Get the first valid range reading
        if msg.ranges:
            valid = [r for r in msg.ranges if r > 0.01]
            distance.data = min(valid) if valid else 999.0
        else:
            distance.data = 999.0
        self.pub.publish(distance)

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicConverter()
    rclpy.spin(node)
    rclpy.shutdown()