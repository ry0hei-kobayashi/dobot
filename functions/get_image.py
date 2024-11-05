###before install openni2_ros_docker to your env

import rclpy
from openni2_interfaces.srv import GetXtionImage

import cv2
from cv_bridge import CvBridge
cv_bridge = CvBridge()

def get_xtion_image():
    rclpy.init()
    node = rclpy.create_node('image_service_client')
    
    client = node.create_client(GetXtionImage, 'xtion_rgb_image')

    if not client.wait_for_service(timeout_sec=10.0):
        node.get_logger().error('could not get the image')
        node.destroy_node()
        rclpy.shutdown()
        return None

    request = GetXtionImage.Request()
    future = client.call_async(request)
    
    rclpy.spin_until_future_complete(node, future)
    
    rgb_image = None

    if future.result() is not None:
        response = future.result()
        if response.rgb_image:
            node.get_logger().info('success to get the image')
            rgb_image = response.rgb_image
        else:
            node.get_logger().warning('cannot get the image')
    else:
        node.get_logger().error('failure to call the service')

    node.destroy_node()
    rclpy.shutdown()
    return rgb_image  

if __name__ == '__main__':

    image = get_xtion_image()
    cv_image = cv_bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
    cv2.imshow("xtion_image", cv_image)
    cv2.waitKey(10)

