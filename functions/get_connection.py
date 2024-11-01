from serial.tools import list_ports
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


