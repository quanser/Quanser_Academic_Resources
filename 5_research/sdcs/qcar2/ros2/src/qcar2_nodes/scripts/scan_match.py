#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from rclpy.executors import ExternalShutdownException
from rclpy.time import Time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseStamped,PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from tf_transformations import quaternion_from_euler
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

import os
import numpy as np  
from quanser.image_processing import Lidar2DMatchScansGrid

class ScanMatchNode(Node):
    def __init__(self):
        super().__init__('scan_match_node')
        self.get_logger().info('Starting Scan Match Node...')

        self.declare_parameter('init_pose', [0.0, 0.0, 0.0])
        self.init_pose = self.get_parameter('init_pose').get_parameter_value().double_array_value
        self.declare_parameter('calibrate', False)
        self.calibrate_flag = self.get_parameter('calibrate').get_parameter_value().bool_value
        self.declare_parameter('odom_pub', False)
        self.odom_pub_flag = self.get_parameter('odom_pub').get_parameter_value().bool_value
        self.declare_parameter('tf_pub', False)
        self.tf_pub_flag = self.get_parameter('tf_pub').get_parameter_value().bool_value

        if self.calibrate_flag:
            self.get_logger().info(f'Creating reference scan at pose {self.init_pose.tolist()}...')
        self.reference_scan_init()
        self.scan_matcher = Lidar2DMatchScansGrid(resolution=33, max_range=10.0)
        # self.scan_matcher = Lidar2DMatchScansGrid()


        qos_profile = QoSProfile(depth=10)
        # init_qos_profile = QoSProfile(
        #     depth=1,
        #     reliability=ReliabilityPolicy.RELIABLE,
        #     durability=DurabilityPolicy.TRANSIENT_LOCAL
        # )
        self.start_time = self.get_clock().now()
        # self.initialized3d = False
        self.latest_scan = None
        self.pose = np.array([0.0,0.0,0.0],dtype=np.float32)
        self.score = np.array([0.0],dtype=np.float32)
        self.covariance = np.eye(3,dtype=np.float32)

        self.timer = self.create_timer(1/15, self.timer_callback)
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            qos_profile)
        self.pose_pub_ = self.create_publisher(
            PoseStamped,
            'pose_estimate',
            qos_profile)
        if self.odom_pub_flag:
            self.odom_pub_ = self.create_publisher(
                Odometry,
                'odom',
                qos_profile)
        self.init_pose_pub_ = self.create_publisher(
            PoseWithCovarianceStamped,
            '/init_pose',
            qos_profile)
        if self.tf_pub_flag:
            self.tf_broadcaster = TransformBroadcaster(self)
        
    def calibrate(self, msg: LaserScan):
        angle_range = msg.angle_max - msg.angle_min
        num_points = len(msg.ranges)
        if num_points>300 and angle_range > 355/360*np.pi \
            and msg.header.stamp.sec - self.start_time.seconds_nanoseconds()[0] > 3:
            
            angles = np.arange(msg.angle_min, msg.angle_max, msg.angle_increment, dtype=np.float32)
            angles = angles - np.pi
            ranges = np.array(msg.ranges,dtype=np.float32)
            reference_scan = np.vstack((angles[:num_points:3], ranges[:num_points:3]))
            # print(reference_scan.shape)
            np.save(self.ref_scan_path, reference_scan)
            self.get_logger().info('Calibration complete.')
            self.calibrate_flag = False
    
    def reference_scan_init(self):
        file_path = os.path.abspath(__file__)
        self.ref_scan_path = os.path.join(
            os.path.dirname(file_path),
            'reference_scan.npy')
        self.reference_scan = None
        if not os.path.exists(self.ref_scan_path) or self.calibrate_flag:
            return
        self.reference_scan = np.load(self.ref_scan_path)
        self.get_logger().info('Reference scan loaded.')

    def scan_callback(self, msg: LaserScan):
        self.latest_scan = msg
        # Publish initial pose once
        # if not self.initialized3d:
        init_pose_msg = PoseWithCovarianceStamped()
        init_pose_msg.header.stamp = self.get_clock().now().to_msg()
        init_pose_msg.header.frame_id = "odom"; 

        init_pose_msg.pose.pose.position.x = self.init_pose [0]
        init_pose_msg.pose.pose.position.y = self.init_pose [1]
        init_pose_msg.pose.pose.position.z = 0.0

        qx, qy, qz, qw = quaternion_from_euler(0.0, 0.0, self.init_pose [2])
        init_pose_msg.pose.pose.orientation.x = qx
        init_pose_msg.pose.pose.orientation.y = qy
        init_pose_msg.pose.pose.orientation.z = qz
        init_pose_msg.pose.pose.orientation.w = qw

        # Fill covariance (36 entries)
        for i in range(36):
            init_pose_msg.pose.covariance[i] = 0.0
        # Example: small covariance values in x, y, yaw
        init_pose_msg.pose.covariance[0] = 1.0
        init_pose_msg.pose.covariance[7] = 1.0
        init_pose_msg.pose.covariance[14] = 0.01
        init_pose_msg.pose.covariance[21] = 0.01
        init_pose_msg.pose.covariance[28] = 0.01
        init_pose_msg.pose.covariance[35] = 0.2
        self.init_pose_pub_.publish(init_pose_msg)
        # self.initialized3d = True

    def timer_callback(self):
        if self.latest_scan is None:
            return
        msg = self.latest_scan

        if self.reference_scan is None:
            if self.calibrate_flag:
                self.calibrate(msg)
                self.reference_scan_init()
            else:
                self.get_logger().error('Reference scan not available. Please set -calibrate True to create it first.')
                raise RuntimeError('Reference scan not available. Cannot perform scan matching.')
        else:
            # Perform scan matching
            self.match_scan(msg)
            estimated_pose = self.pose.tolist()
            # Publish the estimated pose
            pose_msg = PoseStamped()
            pose_msg.header = msg.header
            pose_msg.pose.position.x = estimated_pose[0] - 0.118*np.cos(estimated_pose[2]) # base link centered on back axle
            pose_msg.pose.position.y = estimated_pose[1] - 0.118*np.sin(estimated_pose[2])
            q = quaternion_from_euler(0, 0, estimated_pose[2])
            pose_msg.pose.orientation.x = q[0]
            pose_msg.pose.orientation.y = q[1]
            pose_msg.pose.orientation.z = q[2]
            pose_msg.pose.orientation.w = q[3]

            self.pose_pub_.publish(pose_msg)

            if self.odom_pub_flag:
                odom_msg = Odometry()
                # odom_msg.header = msg.header
                odom_msg.header.stamp = msg.header.stamp
                odom_msg.header.frame_id = "odom"
                odom_msg.child_frame_id = "base_link"
                odom_msg.pose.pose.position.x = estimated_pose[0]
                odom_msg.pose.pose.position.y = estimated_pose[1]
                odom_msg.pose.pose.position.z = 0.0
                odom_msg.pose.pose.orientation.x = q[0]
                odom_msg.pose.pose.orientation.y = q[1]
                odom_msg.pose.pose.orientation.z = q[2]
                odom_msg.pose.pose.orientation.w = q[3]
                self.odom_pub_.publish(odom_msg)
            
            if self.tf_pub_flag:
                t = TransformStamped()
                t.header.stamp = msg.header.stamp
                t.header.frame_id = "odom"
                t.child_frame_id = "base_link"
                t.transform.translation.x = estimated_pose[0]
                t.transform.translation.y = estimated_pose[1]
                t.transform.translation.z = 0.0
                t.transform.rotation.x = q[0]
                t.transform.rotation.y = q[1]
                t.transform.rotation.z = q[2]
                t.transform.rotation.w = q[3]
                self.tf_broadcaster.sendTransform(t)


    def match_scan(self, scan: LaserScan):
        self.init_search = np.array([0,0,0],dtype=np.float32)       
        num_points,curr_angle,curr_range = self.preprocess_(scan)
        ref_angles = self.reference_scan[0]
        ref_ranges = self.reference_scan[1]
        trans_search = np.array([3,3],dtype=np.float32)
        rot_search = np.pi/4
        if self.get_clock().now().seconds_nanoseconds()[0] - self.start_time.seconds_nanoseconds()[0] >1:
            trans_search = np.array([7.5,7.5],dtype=np.float32)
            rot_search = np.pi*3/2
        # self.scan_matcher.open(50.0,10.0)
        self.scan_matcher.match(
                ref_angles=ref_angles,
                ref_ranges=ref_ranges,
                num_ref_points=ref_ranges.shape[0],
                angles=curr_angle,
                ranges=curr_range,
                num_points=num_points,
                initial_pose =self.init_search,
                translation_search_range = trans_search,
                rotation_search_range = rot_search,
                pose = self.pose,
                score = self.score,
                covariance = self.covariance
        )
        self.init_search[:] = self.pose[:]
        # self.scan_matcher.close()
    def preprocess_(self,scan):
        angles = np.arange(scan.angle_min, scan.angle_max, scan.angle_increment, dtype=np.float32)
        angles = angles - np.pi
        # ranges = np.array(scan.ranges)
        # old implementation
        num_points = len(scan.ranges)
        current_angle = np.array(angles[:num_points:3], dtype=np.float32)
        current_range = np.array(scan.ranges[:num_points:3], dtype=np.float32)
        new_num_points = current_angle.shape[0]
        # # end of old
        new_point_index = np.where(current_range<10.0)
        current_angle = current_angle[new_point_index]
        current_range = current_range[new_point_index]
        new_num_points = current_angle.shape[0]
        # self.get_logger().info(f'current scan points {new_num_points}')
        return new_num_points,current_angle,current_range


    def terminate(self):
        self.get_logger().info('Terminating Scan Match Node...')
        self.scan_matcher.close()
    
def main(args=None):
    rclpy.init(args=args)
    scan_match_node = ScanMatchNode()

    try:
        rclpy.spin(scan_match_node)
    except (ExternalShutdownException, KeyboardInterrupt):
        scan_match_node.terminate()
    finally:
        # scan_match_node.terminate()
        scan_match_node.destroy_node()
        rclpy.shutdown()    

if __name__ == '__main__':
    main()