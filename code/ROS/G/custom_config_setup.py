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
            ['launch/custom_ekf_slam.launch.py',
             'launch/my_world_edit.launch.py',
             'launch/online_async_custom.launch.py',
             'launch/spawn_my_burger.launch.py',]),
        ('share/' + package_name + '/config',
            ['config/ekf.yaml',
             'config/mapper_params_online_async.yaml',
             'config/turtlebot3_burger_bridge.yaml',]),
        ('share/' + package_name + '/models/turtlebot3_burger',
            ['models/turtlebot3_burger/model-1_4.sdf',
             'models/turtlebot3_burger/model.config',
             'models/turtlebot3_burger/model.sdf',]),
    ],


...