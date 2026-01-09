import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException
from cv_bridge import CvBridge
from image_transport_py import ImageTransport

from pal.products.qarm import QArmRealSense

class QArmCamera(Node):
    def __init__(self):
        super().__init__('qarm_camera')
        
        # Declare camera parameters
        self.declare_parameter('color_width', 640)
        self.declare_parameter('color_height', 480)
        self.declare_parameter('depth_width', 640)
        self.declare_parameter('depth_height', 480)
        self.declare_parameter('fps', 30.0)

        # Set up camera
        self.color_width = self.get_parameter('color_width').get_parameter_value().integer_value
        self.color_height = self.get_parameter('color_height').get_parameter_value().integer_value
        self.depth_width = self.get_parameter('depth_width').get_parameter_value().integer_value
        self.depth_height = self.get_parameter('depth_height').get_parameter_value().integer_value
        self.fps = self.get_parameter('fps').get_parameter_value().double_value
        self.camera = QArmRealSense(            
            hardware = 1,
            mode='RGB&DEPTH',
            frameWidthRGB=self.color_width,
            frameHeightRGB=self.color_height,
            frameRateRGB=self.fps,
            frameWidthDepth=self.depth_width,
            frameHeightDepth=self.depth_height,
            frameRateDepth=self.fps,
            )
        
        self.bridge = CvBridge()
        self.image_transport = ImageTransport('imagetransport_pub')
        qos = QoSProfile(depth=10)
        
        # Publishers
        self.color_pub = self.image_transport.advertise('qarm_camera/color',10)
        self.depth_pub = self.image_transport.advertise('qarm_camera/depth',10)
        
        # Timer
        period = 1.0 / self.fps
        self.timer = self.create_timer(
            period, 
            self.camera_publish_cb, 
            callback_group=ReentrantCallbackGroup())
        
        self.get_logger().info("RGBD camera initialized")

    def camera_publish_cb(self):
        new = self.camera.read_RGB()
        if new == -1:
            self.get_logger().warn("Failed to capture color frame")
            return
        new = self.camera.read_depth(dataMode='M')
        if new == -1:
            self.get_logger().warn("Failed to capture depth frame")
            return
        stamp = self.get_clock().now().to_msg()
        color_msg = self.bridge.cv2_to_imgmsg(self.camera.imageBufferRGB,"bgr8")
        color_msg.header.stamp = stamp
        color_msg.header.frame_id = 'camera_color'
        self.color_pub.publish(color_msg)
        depth_msg = self.bridge.cv2_to_imgmsg(self.camera.imageBufferDepthM,'32FC1')
        depth_msg.header.stamp = stamp
        depth_msg.header.frame_id = 'camera_depth'
        self.depth_pub.publish(depth_msg)
    
    def destroy_node(self):
        self.camera.terminate()
        super().destroy_node()

def main(args=None):
    try:
        with rclpy.init(args=args):
            node = QArmCamera()
            rclpy.spin(node)

    except (KeyboardInterrupt,ExternalShutdownException):
        pass

    finally:
        node.destroy_node()
        
if __name__ == '__main__':
    main()
