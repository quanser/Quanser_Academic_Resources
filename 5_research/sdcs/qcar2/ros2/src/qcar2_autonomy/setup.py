from setuptools import find_packages, setup
import os 
from glob import glob

package_name = 'qcar2_autonomy'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name,'launch'), glob('launch/*.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu2404',
    maintainer_email='ubuntu2404@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'path_follower = autonomy.nav_to_pose:main',
            'traffic_system_detector=autonomy.traffic_system_detector:main',
            'lane_detector=autonomy.lane_detector:main',
            'yolo_detector=autonomy.yolo_detector:main',
            'trip_planner=autonomy.trip_planner:main'
        ],
    },
)
