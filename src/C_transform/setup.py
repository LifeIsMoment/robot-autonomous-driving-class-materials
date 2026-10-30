from setuptools import setup


package_name = 'c_transform'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    package_dir={package_name: '.'},
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='edu19',
    maintainer_email='edu19@todo.todo',
    description='ROS 2 dynamic and static transform examples',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'tf_dynamic = c_transform.tf_dynamic:main',
            'tf_listener = c_transform.tf_listener:main',
            'tf_listener_laser = c_transform.tf_listener_laser:main',
            'tf_static = c_transform.tf_static:main',
        ],
    },
)
