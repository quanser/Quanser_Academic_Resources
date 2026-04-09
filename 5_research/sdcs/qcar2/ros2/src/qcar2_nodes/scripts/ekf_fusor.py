#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile,ReliabilityPolicy, DurabilityPolicy
from rclpy.executors import ExternalShutdownException
from rclpy.time import Time
from geometry_msgs.msg import PoseStamped,PoseWithCovarianceStamped
from sensor_msgs.msg import Imu, JointState
from qcar2_interfaces.msg import MotorCommands
from tf_transformations import euler_from_quaternion, quaternion_from_euler
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

import os
import numpy as np  
from hal.content.qcar_functions import QCarEKF

class EKFFusorNode(Node):
    def __init__(self):
        super().__init__('ekf_fusor_node')
        self.get_logger().info('Starting EKF Fusor Node...')
        self.declare_parameter('tf_pub', True)
        self.tf_pub_flag = self.get_parameter('tf_pub').get_parameter_value().bool_value

        self.inital_pose_received = False
        self.new_pose_est_received = False
        self.imu_received = False
        self.joint_received = False
        self.steer_received = False
        self.imu_buffer = []
        self.wheel_buffer = []
        self.steer_buffer = []
        self.latest_steer = 0.0
        self.latest_pose_est = None
        self.ekf = None
        self.gyro_z_bias =  0.011
        self.CPS_TO_MPS = (1/(720.0*4) # motor-speed unit conversion
                    * (13.0*19.0) / (70.0*37.0) * 2*np.pi * 0.066/2)
        self.start_time = self.get_clock().now()
        self.now = 0

        qos_profile = QoSProfile(depth=10)
        # init_qos_profile = QoSProfile(
        #     depth=1,
        #     reliability=ReliabilityPolicy.RELIABLE,
        #     durability=DurabilityPolicy.TRANSIENT_LOCAL
        # )
        self.imu_sub_ = self.create_subscription(
            Imu,
            '/qcar2_imu',
            self.imu_cb,
            qos_profile)
        self.wheel_sub_ = self.create_subscription(
            JointState,
            '/qcar2_joint',
            self.wheel_cb,
            qos_profile)
        self.steer_sub_ = self.create_subscription(
            MotorCommands,
            '/qcar2_motor_speed_cmd',
            self.steer_cb,
            qos_profile)
        self.init_pose_sub_ = self.create_subscription(
            PoseWithCovarianceStamped,
            'init_pose',
            self.init_pose_cb,
            qos_profile)
        self.pose_est_sub_ = self.create_subscription(
            PoseStamped,
            'pose_estimate',
            self.pose_est_cb,
            qos_profile)

        self.pose_pub_ = self.create_publisher(
            PoseStamped,
            'ekf_pose_estimate',
            qos_profile)
        self.odom_pub_ = self.create_publisher(
            Odometry,
            'ekf_odom',
            qos_profile)
        if self.tf_pub_flag:
            self.tf_broadcaster = TransformBroadcaster(self)
            self.get_logger().info('ekf publishing tf')
        
        self.timer = self.create_timer(0.05, self.timer_cb)

    def init_pose_cb(self, msg: PoseWithCovarianceStamped):
        if not self.inital_pose_received:
            x = msg.pose.pose.position.x
            y = msg.pose.pose.position.y
            orientation = msg.pose.pose.orientation
            _, _, theta = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
            self.ekf = QCarEKF(
                x_0=[x, y, theta],
                # Q_kf=np.diagflat([1e-05, 0.01]), #optimized for best smoothness, incuded massive delay
                # R_kf=np.diagflat([0.02993309]),   
                # Q_ekf=np.diagflat([0.20112168363722577, 0.0020110574452548457, 0.01]),
                # R_ekf=np.diagflat([10, 10, 0.01992466739602556])
                Q_kf=np.diagflat([0.0001, 0.001]), #OG parameters
                R_kf=np.diagflat([.001]),
                Q_ekf=np.diagflat([0.01, 0.01, 0.01]),
                R_ekf=np.diagflat([0.01, 0.01, 0.001])
                )
            self.inital_pose_received = True
            self.get_logger().info(f'Initialized EKF with pose: x={x}, y={y}, theta={theta}')

    def pose_est_cb(self, msg: PoseStamped):
        x = msg.pose.position.x
        y = msg.pose.position.y
        orientation = msg.pose.orientation
        _, _, theta = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        self.latest_pose_est = np.array([x, y, theta], dtype=np.float32)
        self.new_pose_est_received = True
        
    def imu_cb(self, msg: Imu):
        self.imu_buffer.append(msg.angular_velocity.z - self.gyro_z_bias)
        self.imu_received = True

    def wheel_cb(self, msg: JointState):
        speed = msg.velocity[0] * self.CPS_TO_MPS
        self.wheel_buffer.append(speed)
        self.joint_received = True

    def steer_cb(self, msg: MotorCommands):
        steer = msg.values[0]
        self.steer_buffer.append(steer)
        self.steer_received = True
        
    def timer_cb(self):
        if self.ekf is None:
            return
        if not (self.imu_received and self.joint_received):
            return
        if len(self.imu_buffer) == 0 or len(self.wheel_buffer) == 0:
            return
        
        self.previous = self.now
        now = self.get_clock().now()
        self.now = now.seconds_nanoseconds()[0] - self.start_time.seconds_nanoseconds()[0] + \
              (now.seconds_nanoseconds()[1] - self.start_time.seconds_nanoseconds()[1]) * 1e-9
        dt = self.now - self.previous
        
        # Use the average of buffered IMU and wheel data
        avg_gyro_z = sum(self.imu_buffer) / len(self.imu_buffer)
        self.imu_buffer.clear()
        avg_wheel_speed = sum(self.wheel_buffer) / len(self.wheel_buffer)
        self.wheel_buffer.clear()
        if self.steer_received:
            if len(self.steer_buffer) > 0:
                self.latest_steer = sum(self.steer_buffer) / len(self.steer_buffer)
                self.steer_buffer.clear()

        if self.new_pose_est_received:
            # self.get_logger().info(f"speed:{avg_wheel_speed:.2f},steer:{self.latest_steer:.2f},gyro:{avg_gyro_z:.2f},pose x:{self.latest_pose_est[0]:.2f},pose y:{self.latest_pose_est[1]:.2f},pose th:{self.latest_pose_est[2]:.2f}")
            self.ekf.update(
                [avg_wheel_speed,self.latest_steer],
                dt,
                self.latest_pose_est,
                avg_gyro_z,
            )
            self.new_pose_est_received=False
        else:
            self.ekf.update(
                [avg_wheel_speed,self.latest_steer],
                dt,
                None,
                avg_gyro_z,
            )

        x = self.ekf.x_hat[0,0]
        y = self.ekf.x_hat[1,0]
        th = self.ekf.x_hat[2,0]
        
        pose_msg = PoseStamped()
        pose_msg.header.stamp = now.to_msg()
        # pose_msg.header.stamp = self.scan_time
        pose_msg.header.frame_id = "map"
        pose_msg.pose.position.x = x
        pose_msg.pose.position.y = y
        pose_msg.pose.position.z = 0.0
        q = quaternion_from_euler(0.0, 0.0, th)
        pose_msg.pose.orientation.x = q[0]
        pose_msg.pose.orientation.y = q[1]
        pose_msg.pose.orientation.z = q[2]
        pose_msg.pose.orientation.w = q[3]
        self.pose_pub_.publish(pose_msg)
 
        odom_msg = Odometry()
        # odom_msg.header = msg.header
        odom_msg.header.stamp = now.to_msg()
        # odom_msg.header.stamp = self.scan_time
        odom_msg.header.frame_id = "odom"
        odom_msg.child_frame_id = "base_link"
        odom_msg.pose.pose.position.x = x
        odom_msg.pose.pose.position.y = y
        odom_msg.pose.pose.position.z = 0.0
        odom_msg.pose.pose.orientation.x = q[0]
        odom_msg.pose.pose.orientation.y = q[1]
        odom_msg.pose.pose.orientation.z = q[2]
        odom_msg.pose.pose.orientation.w = q[3]
        self.odom_pub_.publish(odom_msg)
        
        if self.tf_pub_flag:
            t = TransformStamped()
            t.header.stamp = now.to_msg()
            # t.header.stamp = self.scan_time
            t.header.frame_id = "odom"
            t.child_frame_id = "base_link"
            t.transform.translation.x = x
            t.transform.translation.y = y
            t.transform.translation.z = 0.0
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]
            self.tf_broadcaster.sendTransform(t)
        # self.get_logger().info(f'Published Pose: x={pose_msg.x}, y={pose_msg.y}, theta={pose_msg.theta}')

def main(args=None):
    rclpy.init(args=args)
    ekf_fusor_node = EKFFusorNode()

    try:
        rclpy.spin(ekf_fusor_node)
    except (ExternalShutdownException, KeyboardInterrupt):
        pass
    finally:
        ekf_fusor_node.destroy_node()
        rclpy.shutdown()    

if __name__ == '__main__':
    main()