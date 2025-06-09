import os
from glob import glob
from setuptools import setup

package_name = 'qcar'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']), #share package.xml, this is the min by default
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py'))), #share launch files
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.xacro'))), #share urdf
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.gazebo'))), #share gazebo
        (os.path.join('share', package_name, 'gazebo'), glob(os.path.join('gazebo', '*.xacro'))), #share gazebo folder
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*.stl'))), #share mesh stls
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*.dae'))), #share mesh daes
        (os.path.join('share', 'qcar_interface', 'srv'), glob(os.path.join('srv', '*.srv'))), #share service definitions
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nvidia',
    maintainer_email='john.pineros@quanser.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'command           = qcar.commandnode:main',
            'csi               = qcar.csinode:main',
            'rgbd              = qcar.rgbdnode:main',
            'lidar             = qcar.lidarnode:main',
            'qcar              = qcar.qcarnode:main',
            'imageviewer       = qcar.Imageviewer:main'
        ],
    },
)
