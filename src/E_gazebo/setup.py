from glob import glob
import os

from setuptools import setup


package_name = 'E_gazebo'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    package_dir={package_name: 'E_gazebo'},
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py'),
        ),
        (
            os.path.join('share', package_name, 'map'),
            glob('map/*'),
        ),
        (
            os.path.join('share', package_name, 'worlds'),
            glob('worlds/*'),
        ),
        (
            os.path.join('share', package_name, 'rviz'),
            glob('rviz/*'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='edu19',
    maintainer_email='edu19@todo.todo',
    description='Custom TurtleBot3 Gazebo worlds and maps',
    license='TODO: License declaration',
)
