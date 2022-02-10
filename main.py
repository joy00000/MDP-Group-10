import threading
import time
from pcComm import *
import struct
from PIL import Image
from androidComm import *
from stmComm import *
#from imageComm import *
from picamera import PiCamera


class RPI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        #Define subsystem objects
        self.pc_obj = pc()
        #self.android_obj = android()
        #self.STM_obj = STM()
        #self.image_obj = imageComm()
        
        #Establish connection to all the subsystem
        self.pc_obj.connect()
        #self.android_obj.connect()
        #self.STM_obj.connect()
        
        # save camera to class
        self.camera = None

    #Function to receive from PC (images)    
    def readFromPC(self):
        print("in readFromPC function...")
        while True:
            msg = self.pc_obj.readImg()  
            if(msg):
                print("Message received from PC is: " + str(msg))
    
        '''
        if(str(msg) == "CAPTURE IMAGE"):
            self.sendToPC()
        elif(str(msg)[0] == "MOVE"): #“MOVE, FORWARD” “MOVE, LEFT BACKWARD”
            self.sendToSTM(str(msg))
        '''  
    def readFromAlgo(self):
        print("in readFromPC function...")
        while True:
            msg = self.pc_obj.readAlgo()  
            if(msg):
                print("Message received from PC is: " + str(msg))
    
    #Function to send to PC
    def sendToPC(self):
        
        '''self.camera = PiCamera()
        self.camera.resolution = (640, 640)
        self.camera.start_preview()
        # Camera warm-up time
        time.sleep(1)
        stream = io.BytesIO()
        
        self.camera.capture(stream, 'jpeg')
        stream.seek(0)
        stream = stream.read()'''
        stream = self.takePic()

        if(stream):
            #print(stream)
            self.pc_obj.send(stream)
            #print("Message send to PC is " + msgToPC)
    
    def sendToAlgo(self, msgToAlgo):
        if(msgToAlgo):
            self.pc_obj.send(msgToAlgo)
            print("Message send to Algo is " + msgToAlgo)

    #Send function to android
    def sendToAndroid(self, msgToAndroid):
        if(msgToAndroid):
            self.android_obj.send(msgToAndroid)
            print("Message send to Android is " + msgToAndroid)

    #Function to receive from Android
    def readFromAndroid(self):
        while True:
            androidmsg = str(self.android_obj.read())
            print("Message received from android is: %s" %androidmsg)

            if(androidmsg):
                self.sendToAlgo(androidmsg)
                print("sent to algo")

    #Send Function to STM -> need to amend!
    def sendToSTM(self, msgToSTM):
        while True: 
            #msgToSTM = input("Type message:")
            if(msgToSTM):
                self.STM_obj.send(str(msgToSTM))
                print("Message sent to STM is " + msgToSTM)
    
    #Function to receive from STM
    def readFromSTM(self):
        while True:
            STMmsg = str(self.STM_obj.read())         
            #y for sensor value, f for feedback
            if(STMmsg != '\n'):
                print("Message received from STM is: " + STMmsg)
    
    def takePic(self):
        self.camera.start_preview()
        # Camera warm-up time
        time.sleep(1)
        stream = io.BytesIO()
        
        self.camera.capture(stream, 'jpeg')
        stream.seek(0)
        stream = stream.read()
        
        return stream
        
    def start_threads(self):
        #send/write threads for pc, STM and android
        #pc_send_thread = threading.Thread(target=self.sendToPC, args=(), name="pc_send")
        #algo_send_thread = threading.Thread(target=self.sendToAlgo, args=(), name="algo_send")
        #STM_send_thread = threading.Thread(target=self.sendToSTM, args=(), name="STM_send")
        #android_send_thread = threading.Thread(target=self.sendToAndroid, args=(), name="android_send")
        
        #read threads for pc, STM and android
        pc_read_thread = threading.Thread(target=self.readFromPC, args=(), name="pc_read")
        algo_read_thread = threading.Thread(target=self.readFromAlgo, args=(), name="algo_read")
        #STM_read_thread = threading.Thread(target=self.readFromSTM, args=(), name="STM_read")
        #android_read_thread = threading.Thread(target=self.readFromAndroid, args=(), name="android_read")

        #set as daemon (all threads)
        #pc_send_thread.daemon = True
        #algo_send_thread.daemon = True
        pc_read_thread.daemon = True
        algo_read_thread.daemon = True
        #STM_send_thread.daemon = True
        #STM_read_thread.daemon = True
        #android_send_thread.daemon = True
        #android_read_thread.daemon = True

        #start threads -> dont start send threads!
        pc_read_thread.start()
        algo_read_thread.start()
        #pc_send_thread.start()
        #algo_send_thread.start()
        #STM_read_thread.start()
        #STM_send_thread.start()
        #android_read_thread.start()
        #android_send_thread.start()

    def closeAll(self): #disconnect everything
        self.pc_obj.disconnect()
        #self.android_obj.close()
        #self.STM_obj.close()



if __name__ == "__main__":
    main = RPI()
    try:
        main.camera = PiCamera()
        main.camera.resolution = (640, 640)
        main.start_threads()
        while True:
            pass
    except KeyboardInterrupt:
        main.closeAll()