# setup.sample.py

from setuptools import find_packages, setup

package_name = '패키지 이름'   # 자동 수정

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/폴더1',            # 수정
            ['폴더1/파일1']),                             # 수정
        ('share/' + package_name + '/폴더2',            # 수정
            ['폴더2/파일1']),                             # 수정
        ('share/' + package_name + '/폴더3',            # 수정
            ['폴더3/파일1',                               # 수정
             '폴더3/파일2',                               # 수정
             '폴더3/파일3',]),                            # 수정
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kyu',
    maintainer_email='kkr.kyurae.kim@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher = a_pubsub.publisher:main',
            'processor = a_pubsub.processor:main',
            'subscriber = a_pubsub.subscriber:main',
        ],
    },
)