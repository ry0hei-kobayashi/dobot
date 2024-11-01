#!/bin/python3
#common libraries
import time
import cv2
from cv_bridge import CvBridge
cv_bridge = CvBridge()
#get_connection
from functions.get_connection import get_connection

#get_image
from functions.get_image import get_xtion_image
#get_number
from functions.number_recog_gpt import ask_chatgpt_question, parse_response_to_grid
#ブロックパズルの解法
from functions.resolution_puzzleblock import resolution_blockpazzle

##grid_cordinate
distance = 54 # ブロック間距離
x, y = [200, -50] # 0-0の座標

grid_pos = [[[x + i*distance, y + j*distance] for j in range(3)] for i in range(3)]

##z_cordinate
high_z = 15
low_z = -38

##get_connection
dobot = get_connection()

##get_image
image = get_xtion_image()
if image is not None:
    cv_image = cv_bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
    cv2.imshow("xtion_image", cv_image)
    cv2.waitKey(10)

##get_blocknumber
# とりあえずの値
initial_position = [
    [4,3,7],
    [0,6,2],
    [5,1,8]
]
##get_resolution
solution_path = resolution_blockpazzle(initial_position)
# とりあえずの値
solution_path = [[1, 1], [0, 1], [0, 2], [1, 2], [1, 1], [0, 1], [0, 0]]

##get_0.position
for i in range(len(initial_position)):
    for j in range(len(initial_position[i])):
        if initial_position[i][j] == 0:
            position_0_i = i
            position_0_j = j
            break

##block_movement
for i in solution_path:
    # 0の3×3における位置取得
    if i[0] == position_0_i:
        x = position_0_i
    else:
        x = position_0_i + (1 if i[0] > position_0_i else -1)

    if i[1] == position_0_j:
        y = position_0_j
    else:
        y = position_0_j + (1 if i[1] > position_0_j else -1)
    manip_posx, manip_posy = grid_pos[x][y] #動かす物体の座標
    put_posx, put_posy = grid_pos[position_0_i][position_0_j] #0の座標
    dobot.move_to(x=manip_posx, y=manip_posy, z=high_z, wait=True)  # Wait for the movement to finish
    time.sleep(10)
    dobot.move_to(z=low_z, wait=True)
    time.sleep(10)
    dobot.suck(True)
    time.sleep(10)
    dobot.move_to(z=high_z, wait=True)
    time.sleep(10)
    dobot.move_to(x=put_posx, y=put_posy, z=high_z, wait=True)
    time.sleep(10)
    dobot.move_to(z=low_z, wait=True)
    time.sleep(10)
    dobot.suck(False)
    time.sleep(10)
    dobot.move_to(z=high_z)

    position_0_i = x
    position_0_j = y






        
        
    


    











