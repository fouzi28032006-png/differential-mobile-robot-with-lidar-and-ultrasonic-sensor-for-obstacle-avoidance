import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan
import tkinter as tk
import threading

LINEAR_SPEED  = 0.3
ANGULAR_SPEED = 0.8

class GUIControl(Node):
    def __init__(self):
        super().__init__('gui_control')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.lidar_dist     = 999.0
        self.ultrasonic_dist = 999.0
        self.current_state  = 'MANUAL'

        self.lidar_sub = self.create_subscription(
            LaserScan, '/scan', self.lidar_callback, 10)
        self.ultra_sub = self.create_subscription(
            LaserScan, '/ultrasonic_raw', self.ultra_callback, 10)

        self.get_logger().info('GUI Control node started!')

    def lidar_callback(self, msg):
        if msg.ranges:
            front = [r for r in list(msg.ranges[0:30]) + list(msg.ranges[330:])
                     if 0.1 < r < 10.0]
            self.lidar_dist = min(front) if front else 999.0

    def ultra_callback(self, msg):
        if msg.ranges:
            valid = [r for r in msg.ranges if 0.01 < r < 4.0]
            self.ultrasonic_dist = min(valid) if valid else 999.0

    def send_cmd(self, linear, angular):
        cmd = Twist()
        cmd.linear.x  = linear
        cmd.angular.z = angular
        self.cmd_pub.publish(cmd)

    def stop(self):
        self.send_cmd(0.0, 0.0)


class RobotGUI:
    def __init__(self, node):
        self.node = node
        self.root = tk.Tk()
        self.root.title('Robot Control Panel')
        self.root.geometry('400x550')
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(False, False)

        self.build_ui()
        self.update_display()

    def build_ui(self):
        # Title
        tk.Label(
            self.root, text='🤖 Robot Control Panel',
            font=('Arial', 16, 'bold'),
            bg='#1e1e1e', fg='white').pack(pady=10)

        # Status frame
        status_frame = tk.Frame(self.root, bg='#2d2d2d', relief='raised', bd=2)
        status_frame.pack(fill='x', padx=20, pady=5)

        tk.Label(status_frame, text='SENSOR DATA',
                 font=('Arial', 10, 'bold'),
                 bg='#2d2d2d', fg='#00ff00').pack(pady=5)

        self.lidar_label = tk.Label(
            status_frame, text='LiDAR Front: -- m',
            font=('Arial', 11), bg='#2d2d2d', fg='white')
        self.lidar_label.pack()

        self.ultra_label = tk.Label(
            status_frame, text='Ultrasonic: -- m',
            font=('Arial', 11), bg='#2d2d2d', fg='white')
        self.ultra_label.pack()

        self.status_label = tk.Label(
            status_frame, text='Status: READY',
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d', fg='#00ff00')
        self.status_label.pack(pady=5)

        # Control buttons frame
        ctrl_frame = tk.Frame(self.root, bg='#1e1e1e')
        ctrl_frame.pack(pady=15)

        tk.Label(ctrl_frame, text='NAVIGATION',
                 font=('Arial', 10, 'bold'),
                 bg='#1e1e1e', fg='#888888').grid(
                     row=0, column=0, columnspan=3, pady=5)

        btn_style = {
            'width': 8, 'height': 2,
            'font': ('Arial', 12, 'bold'),
            'relief': 'raised', 'bd': 3
        }

        # Forward
        tk.Button(ctrl_frame, text='▲\nFORWARD',
                  bg='#4CAF50', fg='white',
                  command=self.forward, **btn_style).grid(
                      row=1, column=1, padx=5, pady=5)

        # Left
        tk.Button(ctrl_frame, text='◄\nLEFT',
                  bg='#2196F3', fg='white',
                  command=self.left, **btn_style).grid(
                      row=2, column=0, padx=5, pady=5)

        # Stop
        tk.Button(ctrl_frame, text='■\nSTOP',
                  bg='#f44336', fg='white',
                  command=self.stop, **btn_style).grid(
                      row=2, column=1, padx=5, pady=5)

        # Right
        tk.Button(ctrl_frame, text='►\nRIGHT',
                  bg='#2196F3', fg='white',
                  command=self.right, **btn_style).grid(
                      row=2, column=2, padx=5, pady=5)

        # Backward
        tk.Button(ctrl_frame, text='▼\nBACK',
                  bg='#FF9800', fg='white',
                  command=self.backward, **btn_style).grid(
                      row=3, column=1, padx=5, pady=5)

        # Speed control
        speed_frame = tk.Frame(self.root, bg='#2d2d2d', relief='raised', bd=2)
        speed_frame.pack(fill='x', padx=20, pady=5)

        tk.Label(speed_frame, text='SPEED CONTROL',
                 font=('Arial', 10, 'bold'),
                 bg='#2d2d2d', fg='#00ff00').pack(pady=5)

        self.speed_var = tk.DoubleVar(value=0.3)
        tk.Scale(
            speed_frame,
            from_=0.1, to=1.0,
            resolution=0.1,
            orient='horizontal',
            variable=self.speed_var,
            label='Linear Speed (m/s)',
            bg='#2d2d2d', fg='white',
            highlightbackground='#2d2d2d',
            length=300).pack(pady=5)

        # Keyboard hints
        hint_frame = tk.Frame(self.root, bg='#2d2d2d', relief='raised', bd=2)
        hint_frame.pack(fill='x', padx=20, pady=5)

        tk.Label(hint_frame, text='KEYBOARD SHORTCUTS',
                 font=('Arial', 10, 'bold'),
                 bg='#2d2d2d', fg='#00ff00').pack(pady=3)
        tk.Label(hint_frame,
                 text='↑ Forward  ↓ Backward  ← Left  → Right  Space: Stop',
                 font=('Arial', 9),
                 bg='#2d2d2d', fg='#aaaaaa').pack(pady=3)

        # Bind keyboard
        self.root.bind('<Up>',    lambda e: self.forward())
        self.root.bind('<Down>',  lambda e: self.backward())
        self.root.bind('<Left>',  lambda e: self.left())
        self.root.bind('<Right>', lambda e: self.right())
        self.root.bind('<space>', lambda e: self.stop())
        self.root.bind('<KeyRelease>', lambda e: self.stop())

    def forward(self):
        speed = self.speed_var.get()
        self.node.send_cmd(speed, 0.0)
        self.status_label.config(text='Status: MOVING FORWARD', fg='#00ff00')

    def backward(self):
        speed = self.speed_var.get()
        self.node.send_cmd(-speed, 0.0)
        self.status_label.config(text='Status: MOVING BACKWARD', fg='#FF9800')

    def left(self):
        self.node.send_cmd(0.0, ANGULAR_SPEED)
        self.status_label.config(text='Status: TURNING LEFT', fg='#2196F3')

    def right(self):
        self.node.send_cmd(0.0, -ANGULAR_SPEED)
        self.status_label.config(text='Status: TURNING RIGHT', fg='#2196F3')

    def stop(self):
        self.node.stop()
        self.status_label.config(text='Status: STOPPED', fg='#f44336')

    def update_display(self):
        # Update sensor displays
        lidar = self.node.lidar_dist
        ultra = self.node.ultrasonic_dist

        lidar_text = f'LiDAR Front: {lidar:.2f} m'
        ultra_text = f'Ultrasonic:  {ultra:.2f} m'

        lidar_color = '#f44336' if lidar < 0.8 else '#00ff00'
        ultra_color = '#f44336' if ultra < 0.8 else '#00ff00'

        self.lidar_label.config(text=lidar_text, fg=lidar_color)
        self.ultra_label.config(text=ultra_text, fg=ultra_color)

        self.root.after(100, self.update_display)

    def run(self):
        self.root.mainloop()


def ros_spin(node):
    rclpy.spin(node)

def main(args=None):
    rclpy.init(args=args)
    node = GUIControl()

    # Run ROS in background thread
    thread = threading.Thread(target=ros_spin, args=(node,), daemon=True)
    thread.start()

    # Run GUI in main thread
    gui = RobotGUI(node)
    gui.run()

    node.destroy_node()
    rclpy.shutdown()