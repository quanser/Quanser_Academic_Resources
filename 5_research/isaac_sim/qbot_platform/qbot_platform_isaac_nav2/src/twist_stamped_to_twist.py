#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped

class TwistStampedToTwist(Node):
    """
    Converts TwistStamped messages (Nav2 output) to plain Twist (Isaac Sim input)
    """
    def __init__(self):
        super().__init__('twist_stamped_to_twist')

        # Subscribe to Nav2's cmd_vel (TwistStamped)
        self.sub = self.create_subscription(
            TwistStamped,
            '/cmd_vel_nav',            # Nav2 publishes here by default
            self.callback,
            10
        )

        # Publish to Isaac Sim /cmd_vel (Twist)
        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel_twist',      # Isaac Sim should subscribe here
            10
        )

        self.get_logger().info("TwistStamped → Twist bridge running.")

    def callback(self, msg: TwistStamped):
        # Copy linear & angular velocities
        t = Twist()
        t.linear = msg.twist.linear
        t.angular = msg.twist.angular

        # Publish to Isaac Sim
        self.pub.publish(t)

def main(args=None):
    rclpy.init(args=args)
    node = TwistStampedToTwist()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
