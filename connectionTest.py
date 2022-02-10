#Code for to test all communications

from asyncio.windows_utils import BUFSIZE
from base64 import encode
from pcComm import *
from androidComm import *
import struct
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from tqdm import tqdm

#-------------------------------------PC test-----------------------------------
def main():
    pc_obj = pc()
    pc_obj.connect()
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(("192.168.10.10", 3333))
    
    #send
    
    while True:
        msg = input("Enter message: ")
        msg = msg + "\n"
        sock.send(bytes(msg, 'utf-8'))
    
    sock.close()
    
    '''
    #receive
    progress = tqdm(range(100), unit = 'B', unit_scale = True, unit_divisor=1024)

    with open('out.jpg', "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)  
            bytes_read = sock.recv(1024) #experiment with this to get fastest time!!
            if not bytes_read:
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            progress.update(len(bytes_read))
    print("received")
    '''

    
    

#-------------------------------------Android test-----------------------------------

'''def main():

    bt_test = android()
     
    #Establish connection
    bt_test.connect()
     
    #Receive from Android
    #andrmsg = bt_test.read()
    #print(andrmsg)
    
    #Send to Android
    #andrmsg = bt_test.read()
    msg = input("Enter message: ")
    bt_test.send(msg)

    #Terminate connection
    bt_test.close()'''
    

if __name__ == "__main__":
    main()