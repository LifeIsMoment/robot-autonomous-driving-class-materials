from glob import glob
import os

from setuptools import setup


package_name = 'G_custom_config'

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
            glob('launch/*.py'),
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml'),
        ),
        (
            os.path.join(
                'share',
                package_name,
                'models',
                'turtlebot3_burger',
            ),
            glob('models/turtlebot3_burger/*'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='edu19',
    maintainer_email='edu19@todo.todo',
    description='Custom EKF and SLAM configurations for TurtleBot3',
    license='TODO: License declaration',
)
