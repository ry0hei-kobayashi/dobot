import os
import cv2

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class Msg2Video(Node):
    def __init__(self):
        super().__init__('msg_to_mp4')
        
        self.subscription = self.create_subscription(
            Image,
            '/camera/rgb/image_raw',
            self.image_callback,
            10)
        
        self.bridge = CvBridge()
        
        #self.output_file = './videos/output.mp4'
        self.output_file = self.set_output_filename('./videos/output.mp4')
        print('output_filename is ', self.output_file)
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None
        self.frame_width = None
        self.frame_height = None
        self.fps = 30  

    def set_output_filename(self, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while os.path.exists(new_filename):
            new_filename = f"{base}{counter}{ext}"
            counter += 1

        return new_filename

        
    def image_callback(self, msg):
        print("recording...")
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        if self.out is None:
            self.frame_height, self.frame_width = frame.shape[:2]
            self.out = cv2.VideoWriter(self.output_file, self.fourcc, self.fps, (self.frame_width, self.frame_height))
        
        self.out.write(frame)
    
    def destroy_node(self):
        print("finalizing...\n")
        if self.out:
            self.out.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = Msg2Video()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

