from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'diff_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmed',
    maintainer_email='ahmed@todo.todo',
    description='Differential drive robot with ultrasonic sensor',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
       'console_scripts': [
    'robot_node = diff_robot.robot_node:main',
    'ultrasonic_converter = diff_robot.ultrasonic_converter:main',
    'gui_control = diff_robot.gui_control:main',
],
    },
)