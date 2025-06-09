import argparse
import sys
import os

from launch import LaunchDescription, LaunchService
from launch_ros.actions import Node


def main(args, csi_node_name = ['csi_right', 'csi_left', 'csi_front', 'csi_back'],rgbd_node_name =['rgbd_color', 'rgbd_depth'], is_python=False):
	_supported_nodes = ["command", "qcar", "csi", "rgbd", "lidar"]
	nodes = args.nodes
	
	#define parameters for all nodes here
	parameters = {
		"command": [],
		"qcar": [
			{'publishers': ['imu', 'battery', 'velocity']},
			{'imu_publish_frequency': 100},
			{'battery_publish_frequency': 1},
			{'velocity_publish_frequency': 10}
		],
		"csi": [
			{'publishers': csi_node_name}, #You can remove any topic that you don't need.   ['csi_right', 'csi_left', 'csi_front', 'csi_back']
			{'csi_right_resolution': [820, 410]},
			{'csi_left_resolution': [820, 410]},
			{'csi_front_resolution': [820, 410]},
			{'csi_back_resolution': [820, 410]},
			{'csi_right_freq': 120},
			{'csi_left_freq': 120},
			{'csi_front_freq': 120},
			{'csi_back_freq': 120}
		],
		"rgbd": [
			{'publishers': rgbd_node_name}, #You can remove any topic that you don't need. ['rgbd_color', 'rgbd_depth'] 
			{'rgbd_color_resolution': [640, 480]},
			{'rgbd_depth_resolution': [640, 480]},
			{'rgbd_color_freq': 60},
			{'rgbd_depth_freq': 60}
		],
		"lidar": [
			{'lidar_Number_Samples': 100}
		]
	}
	
	#create the launch desciption for passed nodes
	launch_description = [
		Node(
			package='qcar',
			node_executable=n,
			name=n,
			prefix=['stdbuf -o L'],
			output='screen',
			parameters=parameters.get(n, [])
		) for n in nodes if n in _supported_nodes
	]
	
	#if running from python, need to create a launch service, if running from ros2 launch, 
	#then this is already performed and we only need to get the launch description
	ld = LaunchDescription([launch_description])
	if is_python:
		ls = LaunchService()
		ls.include_launch_description(ld)
		return ls.run()
	else:
		return ld

#the following allows the launch file to be deployed directly from python using 'Python3 launch.py' or from ros ecosystem using 'ros2 launch launch.py'
parser = argparse.ArgumentParser(description="Qcar Launch Arguments")


if __name__ == "python_launch_file":
	args = parser.parse_args(sys.argv[4:])
	
	ld = main(args, is_python=False)
	def generate_launch_description():
		return ld

if __name__ == "__main__":
	
	# Specify which highlevel nodes you'd like to publish:
	print("Which nodes would you like to publish? Nodes: command, qcar, csi, rgbd, lidar ")
	topic_name = input("List nodes (separate with commas): ")
	topic_name = topic_name.split(",")
	parser.add_argument("--nodes", nargs="*", default=topic_name, type=str)
	args = parser.parse_args()
	print(args)



	# Section uniqute to CSI and RGBD topics:
	'''Code definitions:   
	- 0: Initialized 
	- 1: No error in user input 
	- 2: User did not define input correctly 
	'''
	CSI_error  = 0
	RGBD_error = 0

	if "csi" not in topic_name and "rgbd" not in topic_name: 
		sys.exit(main(args, is_python=True))

	elif "csi" in topic_name:
		print("list of valid csi nodes:['csi_right', 'csi_left', 'csi_front', 'csi_back'] ")
		csi_node_name = input("Please specify which csi node to publish (separate with commas):")
		csi_node_name =csi_node_name.split(",")
		CSI_error = 1
		if len(csi_node_name) > 4: 
			print(" Too many nodes specified!!")
			CSI_error =2 
			
	
	if "rgbd" in topic_name:
		print("list of valid rgbd nodes:['rgbd_color', 'rgbd_depth']")
		rgbd_node_name = input("Please specify which realsense node to publish (separate with commas):")
		rgbd_node_name =rgbd_node_name.split(",")
		RGBD_error =1
		if len(rgbd_node_name) > 2:
			print(" Too many nodes specified!!")
			RGBD_error =2

	# Error handling if nodes are not configured correctly:
	# Wrong inputs from User 
	if CSI_error == 2 and RGBD_error == 2:
		# Use default settings for all camera streams:
		sys.exit(main(args, is_python=True))		
	
	# Use only CSI
	elif CSI_error == 1 and RGBD_error == 0:
		sys.exit(main(args,csi_node_name, is_python=True))
	
	# Use only RGBD
	elif RGBD_error == 1 and CSI_error == 0:
		sys.exit(main(args,rgbd_node_name, is_python=True))
	
	# Use both CSI and RGBD
	elif CSI_error == 1 and RGBD_error == 1: 
		sys.exit(main(args,csi_node_name,rgbd_node_name, is_python=True))


	
	
