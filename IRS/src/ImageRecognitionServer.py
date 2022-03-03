'''
ImageRecognitionServer - Server that receives and stores images from RPi
@author Lim Rui An, Ryan
<<<<<<< HEAD
@version 1.3
@since 2022-02-10
@modified 2022-03-01
'''
# Required dependencies
=======
@version 1.2
@since 2022-02-10
@modified 2022-02-15
'''

>>>>>>> main
from SymbolRecognizer import SymbolRecognizer as SymRec
import socket
import time

# Constant PATH variables
WEIGHT_PATH = "../weights/"
YOLO_PATH = "../yolov5"
<<<<<<< HEAD
IMAGE_PATH = "../testimg/4170_fullbright.jpg"
=======
IMAGE_PATH = "../testimg/2173.jpg"
>>>>>>> main

RECEIVER_PATH = "../receivedimg/"
RECEIVER_FILE_PATH = RECEIVER_PATH + 'out.jpg'

# Other Constants
ANNOTATION_CLASSES = ['1_blue', '2_green', '3_red', '4_white', '5_yellow', '6_blue', '7_green', '8_red', '9_white', 'a_red', 'b_green', 'bullseye', 'c_white', 'circle_yellow', 'd_blue', 'down_arrow_red', 'e_yellow', 'f_red', 'g_green', 'h_white', 'left_arrow_blue', 'right_arrow_green', 's_blue', 't_yellow', 'u_red', 'up_arrow_white', 'v_green', 'w_white', 'x_blue', 'y_yellow', 'z_red']
<<<<<<< HEAD
NUM_CLASSES = len(ANNOTATION_CLASSES)
WEIGHTS = ['e40b16v8best.pt', 'E30_B16_TSv1.pt']

# System Settings
CONNECTION_RETRY_TIMEOUT = 0.5      # How long to timeout in seconds
WEIGHT_SELECTION = 0                # Which weights file to load, refer to list above @ WEIGHTS
SAVE_RESULTS = True                 # Save result images in listed SAVE_PATH
SAVE_PATH = '../inferences/'        # Location to save images to
USE_GPU = False                      # Allow IRS to use GPU or CPU

# DEBUG Parameters
DEBUG_MODE_ON = True                # For local testing purposes, set to False for real use
=======
NUM_CLASSES = 31

# System Settings
CONNECTION_RETRY_TIMEOUT = 1
SAVE_PATH = '../inferences/'
SAVE_RESULTS = True
USE_GPU = True
>>>>>>> main

# DEBUG Parameters
DEBUG_MODE_ON = False #False #True

# Global Parameters
<<<<<<< HEAD
SymbolRec = None                    # Symbol Recognizer
RPisock = None                      # Socket of RPi
=======
SymbolRec = None # Symbol Recognizer
RPisock = None # Socket of RPi
>>>>>>> main

# Main runtime
def main():
    # Initialize Global Recognizer used for all images
    global SymbolRec
    SymbolRec = SymRec(WEIGHT_PATH + WEIGHTS[WEIGHT_SELECTION], ANNOTATION_CLASSES, NUM_CLASSES, USE_GPU)

    if DEBUG_MODE_ON:
        startTime = time.time()
        msg = SymbolRec.ProcessSourceImages(IMAGE_PATH, SAVE_PATH, SAVE_RESULTS)
        print("Detected: " + msg + " | Time taken: " + "{:.2f}s".format(time.time() - startTime))
    else: serverProcess()

def serverProcess():
    # Trying to connect to RPi
    print("> Attempting Connection with RPi")
    global RPisock
    RPisock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    RPisock.connect(("192.168.10.10", 3333))

    # Ping the RPi to test connection
    RPisock.send(bytes("IRS Pinging RPi", 'utf-8'))

    # Ready to receive images
    while RPisock != None:
        print("> Checking for receivable image")
        try: # Try to receive image
            receiveImage(RPisock)
            processFlag = True
        except (ValueError, Exception):
            processFlag = False
            print("No image to receive")
            time.sleep(CONNECTION_RETRY_TIMEOUT)
        try: # Try to process image
            if processFlag:
                processReceivedImage()
                # break # TEMP: For A2 single process
        except (ValueError, Exception):
            print("Error processing image")
            time.sleep(CONNECTION_RETRY_TIMEOUT)

    # Close the socket when we're done
    RPisock.close()

def receiveImage(sock):
    global RECEIVER_FILE_PATH
    print("\n> Get Image Details from Server")
    # Get image file name from RPi over socket connection
    RPiMessage = sock.recv(1024).decode('utf-8')
    print("RPI MESSAGE: " + RPiMessage)
    RECEIVER_FILE_PATH = RECEIVER_PATH + RPiMessage + '.jpg'
    print("File Path Set: " + RECEIVER_FILE_PATH)
    # Get image file from RPi over socket connection
    getFileFromRPi(sock, RECEIVER_FILE_PATH)
    return RPiMessage

def processReceivedImage():
    global SymbolRec
    # Get result from processed image
    msg = SymbolRec.ProcessSourceImages(RECEIVER_FILE_PATH, SAVE_PATH, SAVE_RESULTS)
    print("TARGET," + msg)
    # Send results to RPi
    RPisock.send(bytes(msg, 'utf-8'))

def getFileFromRPi(sock, path):
    with open(path, "wb") as f:
        # read bytes from the socket (receive)
        print("Receiving data from RPi")
        bytes_read = recvWithTimeout(sock, CONNECTION_RETRY_TIMEOUT)
        print("Data received from RPi")
        # write to the file the bytes we just received
        for i in range(len(bytes_read)):
            f.write(bytes_read[i])
        print("Image file write completed")

def recvWithTimeout(sock, timeout = 1, enableIdleTimemout = True):
    # Make socket non-blocking
    sock.setblocking(0)
    # Data buffers
    total_data = [] # List of bytes
    data = ''
    # Track time for checking timeouts
    startTime = time.time()
    # Loop to grab data from stream
    while True:
        # If data has already been received, wait for timeout and break
        if total_data and time.time() - startTime > timeout:
            break
        # If no data has been received, wait a bit more before timing out
        elif enableIdleTimemout and time.time() - startTime > timeout * 2: # Used to prevent indefinite timeout
            break
        try: # Try to receive Data
            data = sock.recv(2048) # Byte buffer size
            if data: # Valid data attained
                total_data.append(data) #(data.decode('utf-8'))
                startTime = time.time() # Reset timeout start time
            else:
                time.sleep(0.1) # No valid data received, wait for a bit
        except:
            pass
<<<<<<< HEAD
    sock.setblocking(1) # Make socket blocking once more before returning
=======
    # Concatenate the received data and return it
    #return ''.join(total_data)
    # Make socket blocking once more before returning
    sock.setblocking(1)
>>>>>>> main
    return total_data # Returns a list of bytes

def data_to_str(data):
    str = ""
    for i in range(len(data)):
        str += data[i].decode('utf-8')
    return str

if __name__ == "__main__":
    main()
