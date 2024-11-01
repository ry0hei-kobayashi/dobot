#!/bin/python3
#common libraries
import cv2
from cv_bridge import CvBridge
cv_bridge = CvBridge()
#get_connection
from functions.get_connection import get_connection

#get_image
from functions.get_image import get_xtion_image


##get_connection
dobot = get_connection()

##get_image
image = get_xtion_image()
if image is not None:
    cv_image = cv_bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
    cv2.imshow("xtion_image", cv_image)
    cv2.waitKey(10)



