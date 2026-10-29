import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from tf2_geometry_msgs import PointStamped
from visualization_msgs.msg import Marker, MarkerArray
import tf2_ros
from rclpy.duration import Duration
import math


class LidarMapper(Node):
    def __init__(self):
        super().__init__('lidar_mapper')

        self.sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/lidar_points', 10)

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.points = []
        self.id_counter = 0

    def scan_callback(self, msg: LaserScan):
        angle = msg.angle_min

        for distance in msg.ranges:
            if not math.isfinite(distance):
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
                map_point = self.tf_buffer.transform(point, 'odom', timeout=Duration(seconds=0.1))
                self.points.append(map_point.point)

            except Exception as e:
                continue

            angle += msg.angle_increment

        self.publish_markers()

    def publish_markers(self):
        marker_array = MarkerArray()

        for i, p in enumerate(self.points[-2000:]):

            marker = Marker()
            marker.header.frame_id = "odom"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "lidar_points"
            marker.id = i
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD

            marker.pose.position.x = p.x
            marker.pose.position.y = p.y
            marker.pose.position.z = 0.0

            marker.scale.x = 0.05
            marker.scale.y = 0.05
            marker.scale.z = 0.05

            marker.color.a = 1.0
            marker.color.r = 1.0
            marker.color.g = 0.2
            marker.color.b = 0.2

            marker_array.markers.append(marker)

        self.marker_pub.publish(marker_array)


def main():
    rclpy.init()
    node = LidarMapper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()