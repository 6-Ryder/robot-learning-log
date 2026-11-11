import rclpy
from rclpy.node import Node


def main() -> None:
    rclpy.init()
    node = Node("hello_ros")
    node.get_logger().info("Hello from ROS 2 Humble")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()