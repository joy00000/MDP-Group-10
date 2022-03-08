import threading
import time
from pcComm import *
from PIL import Image
from androidComm import *
from stmComm import *
from picamera import PiCamera
from collage import makeCollage


class RPI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        #Define subsystem objects
        self.pc_obj = pc()
        self.android_obj = android()
        self.STM_obj = STM()
        
        #Establish connection to all the subsystem
        self.pc_obj.connect()
        self.android_obj.connect()
        self.STM_obj.connect()
        
        # save camera to class
        self.camera = None
        self.imgCount = 0
        self.conversion = {'1_blue': "11",'2_green': "12", '3_red':"13", '4_white':"14", '5_yellow':"15", '6_blue':"16", 
        '7_green':"17", '8_red':"18", '9_white':"19", 'a_red':"20", 'b_green':"21", 'c_white':"22",
        'd_blue':"23",  'e_yellow':"24", 'f_red':"25",  'g_green':"26",'h_white':"27",  's_blue':"28", 't_yellow':"29", 'u_red':"30", 
        'v_green':"31", 'w_white':"32", 'x_blue':"33", 'y_yellow':"34", 'z_red':"35",'up_arrow_white':"36", 
        'down_arrow_red':"37",'right_arrow_green':"38",'left_arrow_blue':"39", 'circle_yellow':"40"}

        self.currId = []
        self.algoList = []
        self.posList = []
        self.retryCount = 0
        self.prevPos = ""
        
    #Function to receive from PC (images)    
    def readFromPC(self):
        print("in readFromPC function...")
        while True:
            msg = self.pc_obj.readImg()  
            if(msg):
                msg = str(msg)
                print("Message received from PC is: " + str(msg))

                if (msg == "IRS Pinging RPi"):
                    continue
                elif (msg == "Nothing"):
                    print("msg from image rec: " + msg)
                    if self.retryCount < 2:
                        self.sendToSTM("REDO")
                        self.retryCount += 1
                        self.imgCount-=1
                    else:
                        self.sendToSTM("DONE")
                elif msg[:8] == "bullseye":
                    msg = msg.split(',')
                    img, offset = msg[0], msg[1]
                    print("OFFSET: " + offset)
                    '''sign = offset[0]
                    offset = float(offset[1:])
                    offset = offset*100
                    if offset >= 10:
                        offset = str(offset)
                        self.sendToSTM(sign + offset[:3])'''
                    if self.retryCount < 2:
                        self.sendToSTM("REDO")
                        self.retryCount += 1
                        self.imgCount-=1
                    else:
                        self.sendToSTM("DONE")             
                else:
                    self.sendToSTM("DONE")
                    print("msg from image rec: " + msg)
                    msg = msg.split(',')
                    print(msg)
                    img, offset = msg[0], msg[1]
                    print("TARGET,"+ str(self.currId[0]) + ',' + self.conversion[img])
                    print("OFFSET: " + offset)
                    sign = offset[0]
                    offset = float(offset[1:])
                    offset = offset*100
                    if offset >= 10:
                        offset = str(offset)
                        #self.sendToSTM(sign + offset[:3])
                    self.sendToAndroid("TARGET,"+ str(self.currId[0]) + ',' + self.conversion[img])
                    self.currId = self.currId[1:]
                    self.retryCount = 0
                
                
    #Function to send to PC
    def sendToPC(self, msg):
        if msg == "TAKE":
            stream = self.takePic()
            print("in sendToPC function...")
            if(stream):
                #self.sendToSTM("DONE")
                self.imgCount+=1
                self.pc_obj.sendImg(stream, self.imgCount)
        elif msg == "STOP":
            self.pc_obj.sendStr(msg)
            
            

    def readFromAlgo(self):
        print("in readFromAlgo function...")
        while True:
            algoMsg = self.pc_obj.readAlgo()
            if(algoMsg):
                    algoMsg = str(algoMsg)
                    print("Message received from Algo is: " + algoMsg)
                    algoMsg = algoMsg.splitlines()
                    self.algoList += algoMsg
                    print(self.algoList)

                    while self.algoList:
                        msg = self.algoList[0] 
                        self.algoList = self.algoList[1:]
            
                        if(msg[0:4] == "MOVE"): 
                            self.currId.append(msg[-1])
                            msg = msg[5:-2]
                            print("sliced:" + msg)
                            for i in range(0, len(msg), 5):
                                currMsg = msg[i:i+4]
                                print("current msg:" + currMsg)
                                self.sendToSTM(currMsg)
                                
                                if currMsg == "OSRT" or currMsg == "OSLT":
                                    print(self.posList)
                                    #print(self.posList[0])
                                    time.sleep(6)
                                    if len(self.posList) == 0:
                                        self.sendToAndroid("ROBOTPOSITION,"+self.prevPos)
                                    self.sendToAndroid("ROBOTPOSITION,"+self.posList[0])
                                    self.prevPos = self.posList[0]
                                    self.posList = self.posList[1:]
                                elif currMsg == "TAKE":
                                    time.sleep(8)
                                else:
                                    print(self.posList)
                                    print(self.posList[0])
                                    dist = currMsg[-2:]
                                    total = int(dist)/2
                                    time.sleep(int(total))
                                    self.sendToAndroid("ROBOTPOSITION,"+self.posList[0])
                                    self.posList = self.posList[1:]
                        
                        elif(msg[0:4] == "COOR"):
                            msg = msg[5:]
                            print(msg)
                            currPos = msg.split('|')
                            print(currPos)
                            self.posList += currPos
                            print(self.posList[0])
                        
                        elif(msg == "LAST"):
                            self.sendToSTM(msg)

                                  
    def sendToAlgo(self, algoMsg):
        print("in sendToAlgo function...")
        self.pc_obj.sendAlgo(algoMsg+'\n')
        print("Message send to Algo is " + algoMsg)

    #Send function to android
    def sendToAndroid(self, msgToAndroid):
        if (msgToAndroid):
            self.android_obj.send(msgToAndroid)
            print("Message send to Android is " + msgToAndroid)

    #Function to receive from Android
    def readFromAndroid(self):
        while True:
            androidmsg = self.android_obj.read()
            if(androidmsg):
                print("Message received from android is: " + str(androidmsg))
                androidmsg = str(androidmsg)
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
                    print("sent to algo")
                else:
                    print("stops here:" +  androidmsg)

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
                if (STMmsg == "R"):
                    self.sendToPC("TAKE")
                    #self.sendToSTM("DONE")
                elif (STMmsg == "D"):
                    print("STOP: END")
                    self.sendToPC("STOP")
                    
    
    def takePic(self):
        self.camera.start_preview()
        # Camera warm-up time
        time.sleep(1)
        stream = io.BytesIO()
        
        self.camera.capture(stream, 'jpeg')
        stream.seek(0)
        stream = stream.read()
        self.camera.stop_preview()
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
        STM_read_thread = threading.Thread(target=self.readFromSTM, args=(), name="STM_read")
        android_read_thread = threading.Thread(target=self.readFromAndroid, args=(), name="android_read")

        #set as daemon 
        #pc_send_thread.daemon = True
        #algo_send_thread.daemon = True
        pc_read_thread.daemon = True
        algo_read_thread.daemon = True
        #STM_send_thread.daemon = True
        STM_read_thread.daemon = True
        #android_send_thread.daemon = True
        android_read_thread.daemon = True

        #start threads -> dont start send threads!
        pc_read_thread.start()
        algo_read_thread.start()
        #pc_send_thread.start()
        #algo_send_thread.start()
        STM_read_thread.start()
        #STM_send_thread.start()
        android_read_thread.start()
        #android_send_thread.start()

    def closeAll(self): #disconnect everything
        self.pc_obj.disconnect()
        self.android_obj.close()
        self.STM_obj.close()



if __name__ == "__main__":
    main = RPI()
    try:
        main.camera = PiCamera()
        main.camera.resolution = (480, 480)
        #main.camera.brightness = 60
        main.start_threads()
        while True:
            pass
    except KeyboardInterrupt:
        main.closeAll()