from setuptools import setup


package_name = 'D_motion'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    package_dir={package_name: 'D_motion'},
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
        (
            'share/' + package_name + '/launch',
            ['launch/slam.launch.py'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='edu19',
    maintainer_email='edu19@todo.todo',
    description='Motion and SLAM examples for TurtleBot3',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'random_motion = D_motion.random_motion:main',
        ],
    },
)
