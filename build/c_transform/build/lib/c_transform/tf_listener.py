import rclpy
from rclpy.node import Node
from tf2_geometry_msgs import PointStamped
import tf2_ros

class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.timer = self.create_timer(0.5, self.lookup_tf)

    def lookup_tf(self):
        point = PointStamped()
        point.header.frame_id = 'hello_base_link'
        # point.header.frame_id = 'hello_laser'
        point.header.stamp = rclpy.time.Time()
        point.point.x = 0.0
        point.point.y = 0.0
        point.point.z = 0.0

        try:
            transformed = self.tf_buffer.transform(point, 'hello_laser')
            # transformed = self.tf_buffer.transform(point, 'hello_base_link')
            # transformed = self.tf_buffer.transform(point, 'hello_odom')

            self.get_logger().info(
                f"TF point: x={transformed.point.x:.2f}, y={transformed.point.y:.2f}, z={transformed.point.z:.2f}"
            )

        except Exception as e:
            self.get_logger().warn(f"TF not ready: {e}")

def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()