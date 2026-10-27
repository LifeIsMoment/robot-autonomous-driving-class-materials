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
            '터미널에서_사용할_실행_명령_이름 = 패키지이름.파일이름:함수이름',   # 수정
            '터미널에서_사용할_실행_명령_이름 = 패키지이름.파일이름:함수이름',   # 수정
            '터미널에서_사용할_실행_명령_이름 = 패키지이름.파일이름:함수이름',   # 수정
        ],
    },
)