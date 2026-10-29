from setuptools import find_packages, setup
from glob import glob

package_name = 'G_custom_config'

setup(
    ...


    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            glob('launch/*.launch.py')),
        ('share/' + package_name + '/config',
            glob('config/*.yaml')),
        ('share/' + package_name + '/models/turtlebot3_burger',
            glob('models/turtlebot3_burger/*')),
    ],


...