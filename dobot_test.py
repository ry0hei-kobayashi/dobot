
import time
from serial.tools import list_ports
import cv2

import pydobot


# Define the VID and PID for the Silicon Labs CP210x UART Bridge Automatically
def get_connection():

    # CP210x
    TARGET_VID = '10c4'
    TARGET_PID = 'ea60'

    # List available ports and filter for the target device
    available_ports = list_ports.comports()
    target_ports = [p.device for p in available_ports if p.vid == int(TARGET_VID, 16) and p.pid == int(TARGET_PID, 16)] #CP210x

    if target_ports:
        port = target_ports[0] 
        print(f'Current selecteCurrent selectedd port: {port}')
        
    else:
        print("Target device not found. Please check the connection.")

    device = pydobot.Dobot(port=port, verbose=True)

    return device



device = get_connection()

device.speed(velocity=100, acceleration=100)


#addr=
#device.get_eio(addr)
#device.set_eio(addr)

# current joints
(x, y, z, r, j1, j2, j3, j4) = device.pose()
print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')

device.move_to(x + 20, y, z, r, wait=False)
device.move_to(x, y, z, r, wait=True)  # Wait for the movement to finish

# suction
device.suck(True)
time.sleep(10)
device.suck(False)

# grip
#device.grip(True)
#time.sleep(10)
#device.grip(False)

device.close()
