from glob import glob
import os

from setuptools import setup


package_name = 'F_sensor_fusion'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    package_dir={package_name: package_name},
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
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='edu19',
    maintainer_email='edu19@todo.todo',
    description='EKF sensor fusion and SLAM launch for TurtleBot3',
    license='TODO: License declaration',
)
