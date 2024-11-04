import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class ImageToMp4(Node):
    def __init__(self):
        super().__init__('image_to_mp4')
        
        self.subscription = self.create_subscription(
            Image,
            '/camera/rgb/image_raw',
            self.image_callback,
            10)
        
        self.bridge = CvBridge()
        
        self.output_file = './videos/output.mp4'
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        self.frame_width = None
        self.frame_height = None
        self.fps = 30  
        
    def image_callback(self, msg):
        print("recording...")
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        if self.out is None:
            self.frame_height, self.frame_width = frame.shape[:2]
            self.out = cv2.VideoWriter(self.output_file, self.fourcc, self.fps, (self.frame_width, self.frame_height))
        
        self.out.write(frame)
    
    def destroy_node(self):
        print("finaliztig...")
        if self.out:
            self.out.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ImageToMp4()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

