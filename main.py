#!/bin/python3
#common libraries
import time
import cv2
import base64
from cv_bridge import CvBridge
cv_bridge = CvBridge()

#get_connection
from functions.get_connection import get_connection

#get_image
from functions.get_image import get_xtion_image


#get_number
from functions.number_recog_gpt import ask_chatgpt_question, parse_response_to_grid

#ブロックパズルの解法
from functions.resolution_puzzleblock import resolution_puzzleblock

##grid_cordinate
distance = 51 # ブロック間距離

home_x, home_y = 200, -150

x, y = [190, -50] # 0-0の座標

grid_pos = [[[x + i*distance, y + j*distance] for j in range(3)] for i in range(3)]

##z_cordinate
high_z = 15
low_z = -40

##get_connection
dobot = get_connection()

##movetoHOME
dobot.move_to(x=home_x, y=home_y, z=high_z, r=0, wait=True)

##get_image
#if image is not None:
while True:
    image = get_xtion_image()

    if image is not None: 
        cv_image = cv_bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
        save_image = cv2.imwrite('./images/img.jpg', cv_image)
        #cv2.imshow("xtion_image", cv_image)
        #cv2.waitKey(10)
        break

    else:
        print("Image from the xtion is not available")

print("before gpt")
response = ask_chatgpt_question()
print("Response from ChatGPT:", response)

initial_position = parse_response_to_grid(response)

# sample value
#initial_position = [
#    [4,3,7],
#    [0,6,2],
#    [5,1,8]
#]

print("3x3 array:\n", initial_position)


##get_resolution
solution_path = resolution_puzzleblock(initial_position)

# sample value
#solution_path = [[1, 1], [0, 1], [0, 2], [1, 2], [1, 1], [0, 1], [0, 0]]

#get_0.position
for i in range(len(initial_position)):
    for j in range(len(initial_position[i])):
        if initial_position[i][j] == 0:
            position_0_i = i
            position_0_j = j
            break

#TODO 腕をどける

#block_movement
print("move robot")
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
    dobot.move_to(x=manip_posx, y=manip_posy, z=high_z, r=0, wait=True)  # Wait for the movement to finish
    time.sleep(0.2)
    dobot.move_to(x=manip_posx, y=manip_posy, z=low_z, r=0, wait=True)
    time.sleep(0.2)
    dobot.suck(True)
    time.sleep(0.2)
    dobot.move_to(x=manip_posx, y=manip_posy, z=high_z, r=0, wait=True)
    time.sleep(0.2)
    dobot.move_to(x=put_posx, y=put_posy, z=high_z, r=0, wait=True)
    time.sleep(0.2)
    dobot.move_to(x=put_posx, y=put_posy, z=low_z, r=0,  wait=True)
    time.sleep(0.2)
    dobot.suck(False)
    time.sleep(0.2)
    dobot.move_to(x=put_posx, y=put_posy, z=high_z, r=0,  wait=True)

    position_0_i = x
    position_0_j = y
    
##movetoHOME
dobot.move_to(x=home_x, y=home_y, z=high_z, r=0, wait=True)

