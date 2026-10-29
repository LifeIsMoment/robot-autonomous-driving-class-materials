import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from tf2_geometry_msgs import PointStamped
import tf2_ros
import math

class LaserTFListener(Node):
    def __init__(self):
        super().__init__('laser_tf')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

    def scan_callback(self, msg: LaserScan):
        i = 0
        angle = msg.angle_min

        for distance in msg.ranges:
            if distance == float('inf') or math.isnan(distance):
                angle += msg.angle_increment
                continue

            x = distance * math.cos(angle)
            y = distance * math.sin(angle)

            point = PointStamped()
            point.header = msg.header
            point.point.x = x
            point.point.y = y
            point.point.z = 0.0

            try:
                transformed = self.tf_buffer.transform(point, 'hello_base_link')
                self.get_logger().info(
                    f"[{i}] TF point: x={transformed.point.x:.2f}, y={transformed.point.y:.2f}, z={transformed.point.z:.2f}"
                )
                i += 1
            except Exception as e:
                self.get_logger().warn(f"TF not ready: {e}")

            angle += msg.angle_increment

def main():
    rclpy.init()
    node = LaserTFListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()