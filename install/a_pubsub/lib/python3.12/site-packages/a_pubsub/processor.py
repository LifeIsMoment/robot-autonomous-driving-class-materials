import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray, String


DIRECTION_DELTAS = {
    'w': (0, 1),
    's': (0, -1),
    'a': (-1, 0),
    'd': (1, 0),
}


def update_location(x: int, y: int, direction: str) -> tuple[int, int]:
    dx, dy = DIRECTION_DELTAS.get(direction.lower(), (0, 0))
    return x + dx, y + dy


class LocationProcessor(Node):
    def __init__(self):
        super().__init__('calc_loc')

        self.x = 0
        self.y = 0

        self.pub = self.create_publisher(Int16MultiArray, '/location', 10)
        self.sub = self.create_subscription(String, '/direction', self.callback, 10)

        self.timer = self.create_timer(0.5, self.publish_location)

    def callback(self, msg):
        self.get_logger().info(f'RECEIVED: {msg.data}')
        self.x, self.y = update_location(self.x, self.y, msg.data)
        self.get_logger().info(f'Updated loc: ({self.x}, {self.y})')

    def publish_location(self):
        msg = Int16MultiArray()
        msg.data = [self.x, self.y]

        self.pub.publish(msg)


def main():
    rclpy.init()
    node = LocationProcessor()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
