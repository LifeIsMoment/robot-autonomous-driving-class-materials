import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher_ = self.create_publisher(String, '/demo_topic', 10)
        self.start_time = time.time()
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        elapsed = int(time.time() - self.start_time)
        msg = String()
        msg.data = f"Hello ROS2: {elapsed}"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')

def main():
    rclpy.init()
    node = Talker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()