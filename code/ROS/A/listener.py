import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription_ = self.create_subscription(String, '/demo_topic', self.callback, 10)
        self.subscription_

    def callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')

def main():
    rclpy.init()
    node = Listener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()