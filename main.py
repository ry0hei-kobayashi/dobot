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
from functions.blockpuzzle_solver import blockpuzzle_solver
##proc_img
from functions.proc_img import proc_img



##grid_cordinate
distance = 51 # ブロック間距離

home_x, home_y = 200, -150

x, y = [190, -50] # 0-0の座標

grid_pos = [[[x + i*distance, y + j*distance] for j in range(3)] for i in range(3)]

##z_coordinate
high_z = 15
low_z = -40

##get_connection
dobot = get_connection()

##move2HOME
dobot.move_to(x=home_x, y=home_y, z=high_z, r=0, wait=True)

##get_image and solve loop
while True:
    # 初期位置で画像取得
    while True:
        image = get_xtion_image()

        if image is not None:
            cv_image = cv_bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
            cv_image = proc_img(cv_image)
            #save_image = cv2.imwrite('./images/img.jpg', cv_image)
            break
        else:
            print("Image from the xtion is not available")

    print("before gpt")
    response = ask_chatgpt_question()
    print("Response from ChatGPT:", response)

    # Initial positionの設定
    initial_position = parse_response_to_grid(response)
    print("3x3 array:\n", initial_position)

    # solution_pathの取得
    solution_path = blockpuzzle_solver(initial_position)

    # 初期の0の位置を取得
    for i in range(len(initial_position)):
        for j in range(len(initial_position[i])):
            if initial_position[i][j] == 0:
                position_0_i = i
                position_0_j = j
                break

    current_position = initial_position

    # 移動を開始
    for step, i in enumerate(solution_path):
        # 0の3×3における位置取得
        if i[0] == position_0_i:
            x = position_0_i
        else:
            x = position_0_i + (1 if i[0] > position_0_i else -1)

        if i[1] == position_0_j:
            y = position_0_j
        else:
            y = position_0_j + (1 if i[1] > position_0_j else -1)

        # current position of 0
        manip_posx, manip_posy = grid_pos[x][y]
        put_posx, put_posy = grid_pos[position_0_i][position_0_j]
        dobot.move_to(x=manip_posx, y=manip_posy, z=high_z, r=0, wait=True)
        time.sleep(0.2)
        dobot.move_to(x=manip_posx, y=manip_posy, z=low_z, r=0, wait=True)
        time.sleep(0.2)
        dobot.suck(True)
        time.sleep(0.2)
        dobot.move_to(x=manip_posx, y=manip_posy, z=high_z, r=0, wait=True)
        time.sleep(0.2)
        dobot.move_to(x=put_posx, y=put_posy, z=high_z, r=0, wait=True)
        time.sleep(0.2)
        dobot.move_to(x=put_posx, y=put_posy, z=low_z, r=0, wait=True)
        time.sleep(0.2)
        dobot.suck(False)
        time.sleep(0.2)
        dobot.move_to(x=put_posx, y=put_posy, z=high_z, r=0, wait=True)
        time.sleep(0.2)
        dobot.move_to(x=home_x, y=home_y, z=high_z, r=0, wait=True)

        # `current_position` の更新と表示
        current_position[position_0_i][position_0_j], current_position[x][y] = current_position[x][y], current_position[position_0_i][position_0_j]
        for row in current_position:
            print(row)

        # 各移動後の画像取得と処理
        while True:
            image = get_xtion_image()
            if image is not None:
                cv_image = cv_bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
                cv_image = proc_img(cv_image)
                break
            else:
                print("Image from the xtion is not available")

        print("before gpt")
        response = ask_chatgpt_question()
        print("Response from ChatGPT:", response)
        real_position = parse_response_to_grid(response)

        # 確認: current_positionとreal_positionが一致しない場合、最初のget_imageに戻る
        if current_position != real_position:
            print("Mismatch detected, returning to initial get_image step.")
            break  # 外側のwhileループに戻るためのbreak

        # 0の位置更新
        position_0_i = x
        position_0_j = y
    else:
        # solution_path を全て正しく完了した場合に終了
        print("Puzzle solved successfully.")
        break

##movetoHOME
dobot.move_to(x=home_x, y=home_y, z=high_z, r=0, wait=True)
