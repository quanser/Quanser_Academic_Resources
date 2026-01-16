#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from qarm_interfaces.action import MoveQArm

class QArmActionClient(Node):

    def __init__(self, name):
        super().__init__(name)
        self.move_qarm_client_ = ActionClient(self,MoveQArm,name)
        self.declare_parameter(
            'goal_pose',
            [0.0,0.0,0.5,0.0])
        # print(self.get_parameter('goal_pose').get_parameter_value())
        self.goal_pose = self.get_parameter(
            'goal_pose').get_parameter_value().double_array_value
    
    def send_goal(self,goal_pose):
        # Wait for the server
        self.move_qarm_client_.wait_for_server()

        # Construct goal msg
        goal_msg = MoveQArm.Goal()
        goal_msg.task_space_pose=goal_pose

        # Send the goal
        self.get_logger().info(f'Sending goal {goal_pose}')
        self.send_goal_future_ = self.move_qarm_client_.send_goal_async(
            goal_msg,
            feedback_callback = self.feedback_cb)
        self.send_goal_future_.add_done_callback(self.goal_response_cb)

    def goal_response_cb(self,future):
        self.goal_handle_ = future.result()
        if self.goal_handle_.accepted:
            self.goal_handle_.get_result_async().add_done_callback(
                self.result_cb)

    def result_cb(self,future):
        result = future.result().result
        self.get_logger().info(result.message)
    
    def feedback_cb(self, feedback):
        self.get_logger().info (f'Distance to goal:{feedback.feedback.position_error_norm:.3f}, orientation difference:{feedback.feedback.orientation_error:.3f}')

    def cancel(self):
        self.goal_handle_.cancel_goal_async().add_done_callback(self.cancel_cb)

    def cancel_cb(self, future):
        cancel_response = future.result()
        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info('Goal successfully canceled')
        else:
            self.get_logger().info('Goal failed to cancel')

def main(args=None):
    try:
        with rclpy.init(args=args):
            qarm_action_client = QArmActionClient('move_qarm')
            goal_pose = list(qarm_action_client.goal_pose)
            qarm_action_client.get_logger().info(f'Goal pose parameter: {goal_pose}')
            qarm_action_client.send_goal(goal_pose)
            rclpy.spin(qarm_action_client)

    except (KeyboardInterrupt, ExternalShutdownException):
        qarm_action_client.cancel()

    finally:
        qarm_action_client.destroy_node()


if __name__ == '__main__':
    main()