from setuptools import setup


package_name = 'a_pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    package_dir={package_name: 'A_pubsub'},
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
        (
            'share/' + package_name + '/launch',
            ['launch/pubsub.launch.py'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='edu19',
    maintainer_email='edu19@todo.todo',
    description='Keyboard-driven ROS 2 position publisher and subscriber',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = a_pubsub.talker:main',
            'listener = a_pubsub.listener:main',
            'publisher = a_pubsub.publisher:main',
            'processor = a_pubsub.processor:main',
            'subscriber = a_pubsub.subscriber:main',
        ],
    },
)
