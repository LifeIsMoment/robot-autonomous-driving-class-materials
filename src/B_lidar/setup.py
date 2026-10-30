from setuptools import find_packages, setup

package_name = 'B_lidar'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            ['launch/gazebo_rviz_auto.launch.py']),
        ('share/' + package_name + '/rviz',
            ['rviz/tb3_gazebo_slow_view.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='edu19',
    maintainer_email='edu19@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'simple_oa = B_lidar.simple_oa:main',
            'corner_escape_oa = B_lidar.corner_escape_oa:main',
        ],
    },
)
