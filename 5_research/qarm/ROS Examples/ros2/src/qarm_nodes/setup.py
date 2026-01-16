from setuptools import setup
import os
from glob import glob

package_name = 'qarm_nodes'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Your Name',
    author_email='you@example.com',
    description='QArm nodes package',
    license='Apache-2.0',
    data_files=[
        # this is the package marker so ROS 2 can index the package
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        # include package.xml in the install
        ('share/' + package_name, ['package.xml']),
        # if you have launch files, you can install them too
        # (uncomment if applicable)
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*.py'))),
    ],
    entry_points={
        'console_scripts': [
            'qarm_hardware = qarm_nodes.qarm_hardware:main',
            'move_qarm_server=qarm_nodes.move_qarm_server:main',
            'move_qarm_client=qarm_nodes.move_qarm_client:main',
            'rgbd=qarm_nodes.rgbd:main',
        ],
    },
)