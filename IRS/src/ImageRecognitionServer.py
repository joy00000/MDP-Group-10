'''
ImageRecognitionServer - Server that receives and stores images from RPi
@author Lim Rui An, Ryan
@version 1.3
@since 2022-02-10
@modified 2022-03-01
'''
# Required dependencies
from SymbolRecognizer import SymbolRecognizer as SymRec
import socket
import time
import os
# Pil for drawing on images
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math

# Constant PATH variables
WEIGHT_PATH = "../weights/"
YOLO_PATH = "../yolov5"
RECEIVER_PATH = "../receivedimg/"
RECEIVER_FILE_PATH = RECEIVER_PATH + 'out.jpg'

# Other Constants
ANNOTATION_CLASSES = ['1_blue', '2_green', '3_red', '4_white', '5_yellow', '6_blue', '7_green', '8_red', '9_white', 'a_red', 'b_green', 'bullseye', 'c_white', 'circle_yellow', 'd_blue', 'down_arrow_red', 'e_yellow', 'f_red', 'g_green', 'h_white', 'left_arrow_blue', 'right_arrow_green', 's_blue', 't_yellow', 'u_red', 'up_arrow_white', 'v_green', 'w_white', 'x_blue', 'y_yellow', 'z_red']
NUM_CLASSES = len(ANNOTATION_CLASSES)

ANNOTATION_ID = {'1_blue': "11", '2_green': "12", '3_red':"13", '4_white':"14", '5_yellow':"15", '6_blue':"16", '7_green':"17", '8_red':"18", '9_white':"19", 'a_red':"20", 'b_green':"21", 'c_white':"22", 'd_blue':"23",  'e_yellow':"24", 'f_red':"25",  'g_green':"26",'h_white':"27",  's_blue':"28", 't_yellow':"29", 'u_red':"30", 'v_green':"31", 'w_white':"32", 'x_blue':"33", 'y_yellow':"34", 'z_red':"35",'up_arrow_white':"36", 'down_arrow_red':"37",'right_arrow_green':"38",'left_arrow_blue':"39", 'circle_yellow':"40", 'bullseye' : "0"}

WEIGHTS = ['e40b16v8best.pt', 'E30_B16_TSv1.pt']

# System Settings
CONNECTION_RETRY_TIMEOUT = 0.5      # How long to timeout in seconds
WEIGHT_SELECTION = 1                # Which weights file to load, refer to list above @ WEIGHTS
COLLAGE_PATH = '../collage/'        # Path of the saved collage
SAVE_RESULTS = True                 # Save result images in listed SAVE_PATH
SAVE_PATH = '../inferences/'        # Location to save images to
USE_GPU = False                     # Allow IRS to use GPU or CPU

# DEBUG Parameters
DEBUG_MODE_ON = False               # For local testing purposes, set to False for real use
DEBUG_IMAGE = "1_5 - Copy.jpg"
IMAGE_PATH = "../testimg/" + DEBUG_IMAGE

# Global Parameters
SymbolRec = None                    # Symbol Recognizer
RPisock = None                      # Socket of RPi

# Main runtime
def main():
    # Initialize Global Recognizer used for all images
    global SymbolRec
    SymbolRec = SymRec(WEIGHT_PATH + WEIGHTS[WEIGHT_SELECTION], ANNOTATION_CLASSES, ANNOTATION_ID, NUM_CLASSES, USE_GPU)

    if DEBUG_MODE_ON:
        startTime = time.time()
        msg, detectionString = SymbolRec.ProcessSourceImages(IMAGE_PATH, SAVE_PATH, SAVE_RESULTS)
        print("Detected: " + detectionString + " | Time taken: " + "{:.2f}s".format(time.time() - startTime))
        modifyInferenceImage(SAVE_PATH, DEBUG_IMAGE, detectionString)
        createInferenceCollage(SAVE_PATH)
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
        fileName = None
        try: # Try to receive image
            fileName = receiveImageDetails(RPisock)
            if fileName == "STOP":
                break
            receiveImage(RPisock, fileName)
            processFlag = True
        except (ValueError, Exception):
            processFlag = False
            print("No image to receive")
            time.sleep(CONNECTION_RETRY_TIMEOUT)
        try: # Try to process image
            if processFlag:
                modifyInferenceImage(SAVE_PATH, fileName + '.jpg', processReceivedImage())
                # break # TEMP: For A2 single process
        except (ValueError, Exception):
            print("Error processing image")
            time.sleep(CONNECTION_RETRY_TIMEOUT)

    # Close the socket when we're done
    RPisock.close()
    # Generate the inference collage
    createInferenceCollage(SAVE_PATH)

def receiveImageDetails(sock):
    print("\n> Get Image Details from Server")
    # Get image file name from RPi over socket connection
    RPiMessage = sock.recv(1024).decode('utf-8')
    print("RPI MESSAGE: " + RPiMessage)
    return RPiMessage

def receiveImage(sock, RPiMessage):
    global RECEIVER_FILE_PATH
    print("\n> Get Image from Server")
    RECEIVER_FILE_PATH = RECEIVER_PATH + RPiMessage + '.jpg'
    print("File Path Set: " + RECEIVER_FILE_PATH)
    # Get image file from RPi over socket connection
    getFileFromRPi(sock, RECEIVER_FILE_PATH)

def processReceivedImage():
    global SymbolRec
    # Get result from processed image
    msg, detectionString = SymbolRec.ProcessSourceImages(RECEIVER_FILE_PATH, SAVE_PATH, SAVE_RESULTS)
    print("TARGET," + msg)
    # Send results to RPi
    RPisock.send(bytes(msg, 'utf-8'))
    return detectionString

def modifyInferenceImage(SAVE_PATH, ImageName, ResultString, FontSize = 25):
    print("\n> Setting Up Image for Collage Later")
    print("Opening Image")
    img = Image.open(SAVE_PATH + ImageName)
    draw = ImageDraw.Draw(img)
    font =  ImageFont.truetype("arial.ttf", FontSize)
    # Drop shadow
    print("Drawing on Image")
    draw.text((7, 7), ResultString, (0,0,0), font = font)
    # Print Text
    draw.text((5, 5), ResultString, (255,255,255), font = font)
    print("Image Modified")
    img.save(SAVE_PATH + ImageName)

def createInferenceCollage(PATH, MaxCols = 4, ImgResolution = 416):
    try: # Obtain files from directory
        files = os.listdir(PATH)
    except (ValueError, Exception):
        print("Error opening inference collage path")
        return
    print("\n> Generating Inference Collage")
    # Set up the image to be used for the collage
    file_count = len(files)
    MaxRows = math.ceil(file_count / MaxCols)
    if MaxCols > file_count:
        MaxCols = file_count
    collage = Image.new('RGB', (MaxCols * ImgResolution, MaxRows * ImgResolution)) # Cols, Rows
    # Iterators for collaging
    i,j = 0,0
    # For each file in the inference folder
    for f in files:
        if f == None:
            continue
        if i == MaxCols:
            i = 0
            j += 1
        im = Image.open(PATH + f)
        im = im.resize((ImgResolution, ImgResolution), resample = Image.ANTIALIAS)
        collage.paste(im, (i * im.size[0], j * im.size[0])) # Insert the resized image into the collage
        i += 1
    # Save the results of the collage
    collage.save(COLLAGE_PATH + "collage.jpg","JPEG")
    print("Collage generated at location: " + COLLAGE_PATH + "collage.jpg")
    collage.show()

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
    sock.setblocking(1) # Make socket blocking once more before returning
    return total_data # Returns a list of bytes

if __name__ == "__main__":
    main()
