import threading
import time
from pcComm import *
import struct
from PIL import Image
from androidComm import *
from stmComm import *
from picamera import PiCamera


class RPI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        #Define subsystem objects
        self.pc_obj = pc()
        self.android_obj = android()
        #self.STM_obj = STM()
        
        #Establish connection to all the subsystem
        self.pc_obj.connect()
        self.android_obj.connect()
        #self.STM_obj.connect()
        
        # save camera to class
        self.camera = None
        self.imgCount = 0
        self.conversion = {'1_blue': "11",'2_green': "12", '3_red':"13", '4_white':"14", '5_yellow':"15", '6_blue':"16", 
        '7_green':"17", '8_red':"18", '9_white':"19", 'a_red':"20", 'b_green':"21", 'c_white':"22",
        'd_blue':"23",  'e_yellow':"24", 'f_red':"25",  'g_green':"26",'h_white':"27",  's_blue':"28", 't_yellow':"29", 'u_red':"30", 
        'v_green':"31", 'w_white':"32", 'x_blue':"33", 'y_yellow':"34", 'z_red':"35",'up_arrow_white':"36", 
        'down_arrow_red':"37",'right_arrow_green':"38",'left_arrow_blue':"39", 'circle_yellow':"40"}
        
    #Function to receive from PC (images)    
    def readFromPC(self):
        print("in readFromPC function...")
        while True:
            msg = self.pc_obj.readImg()  
            if(msg):
                msg = str(msg)
                print("Message received from PC is: " + str(msg))
                '''if (msg == "RESEND"):
                    self.imgCount-=1
                    self.sendToPC()
                elif (msg[0:7]=="TARGET"):
                    self.sendToAndroid(msg)'''
                
    #Function to send to PC
    def sendToPC(self):
        stream = self.takePic()
        print("in sendToPC function...")
        if(stream):
            self.imgCount+=1
            self.pc_obj.sendImg(stream, self.imgCount)
            #self.sendToSTM("DONE")
            

    def readFromAlgo(self):
        #print("in readFromAlgo function...")
        while True:
            msg = self.pc_obj.readAlgo()  
            if(msg):
                print("Message received from Algo is: " + str(msg))
                '''msg = str(msg)
                if(msg == "TAKE"): #add obstacleid
                    self.sendToSTM(msg)
                elif(msg[0:4] == "MOVE"): #“MOVE, FORWARD” “MOVE, LEFT BACKWARD”
                    self.sendToSTM(msg)'''
    
    def sendToAlgo(self):
        algomsg = input("msg: ")
        for i in algomsg:
            #print("in sendToAlgo function...")
            self.pc_obj.sendAlgo(i)
            print("Message send to Algo is " + i)

    #Send function to android
    def sendToAndroid(self):
        while True:
            msgToAndroid = input("msg:")
            if (msgToAndroid):
                self.android_obj.send(msgToAndroid)
                print("Message send to Android is " + msgToAndroid)

    #Function to receive from Android
    def readFromAndroid(self):
        while True:
            androidmsg = self.android_obj.read()
            if(androidmsg):
                androidmsg = str(androidmsg)
                print("Message received from android is: " + androidmsg)
                '''               
                if(androidmsg == "forward"):
                    self.sendToSTM("F---")
                elif(androidmsg == "reverse"):
                    self.sendToSTM("B---")
                elif(androidmsg == "left"):
                    self.sendToSTM("L---")
                elif(androidmsg == "right"):
                    self.sendToSTM("R---")
                elif(androidmsg [0:11] == "ADDOBSTACLE"):
                    self.sendToAlgo(androidmsg)
                    print("sent to algo")'''

    #Send Function to STM 
    def sendToSTM(self, msgToSTM):
        if(msgToSTM):
            self.STM_obj.send(str(msgToSTM))
            print("Message sent to STM is " + msgToSTM)
    
    #Function to receive from STM
    def readFromSTM(self):
        while True:
            STMmsg = self.STM_obj.read()      
            if(STMmsg):
                STMmsg = str(STMmsg)
                print("Message received from STM is: " + STMmsg)
                '''if (STMmsg == "REACH"):
                    self.sendToPC()'''
    
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
        #pc_read_thread = threading.Thread(target=self.readFromPC, args=(), name="pc_read")
        algo_read_thread = threading.Thread(target=self.readFromAlgo, args=(), name="algo_read")
        #STM_read_thread = threading.Thread(target=self.readFromSTM, args=(), name="STM_read")
        android_read_thread = threading.Thread(target=self.readFromAndroid, args=(), name="android_read")

        #set as daemon 
        #pc_send_thread.daemon = True
        #algo_send_thread.daemon = True
        #pc_read_thread.daemon = True
        #algo_read_thread.daemon = True
        #STM_send_thread.daemon = True
        #STM_read_thread.daemon = True
        #android_send_thread.daemon = True
        android_read_thread.daemon = True

        #start threads -> dont start send threads!
        #pc_read_thread.start()
        algo_read_thread.start()
        #pc_send_thread.start()
        #algo_send_thread.start()
        #STM_read_thread.start()
        #STM_send_thread.start()
        android_read_thread.start()
        #android_send_thread.start()

    def closeAll(self): #disconnect everything
        self.pc_obj.disconnect()
        self.android_obj.close()
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