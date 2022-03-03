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
        #self.android_obj = android()
        self.STM_obj = STM()
        
        #Establish connection to all the subsystem
        self.pc_obj.connect()
        #self.android_obj.connect()
        self.STM_obj.connect()
        
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
                if (msg == "bullseye" or msg == "Nothing"):
                    self.sendToSTM("DONE")
                elif (msg[0] == "I"):
                    continue
                else:
                    print("Object identified is " + msg + "ID is " + self.conversion[msg])
                    self.sendToSTM("STOP")
                    
                
    #Function to send to PC
    def sendToPC(self):
        stream = self.takePic()
        print("in sendToPC function...")
        if(stream):
            self.imgCount+=1
            self.pc_obj.sendImg(stream, str(self.imgCount))

    #Send Function to STM 
    def sendToSTM(self, msgToSTM):
        #msgToSTM = input("msg:" )
        self.STM_obj.send(str(msgToSTM))
        print("Message sent to STM is " + msgToSTM)
    
    #Function to receive from STM
    def readFromSTM(self):
        print("in read stm")
        while True:
            STMmsg = self.STM_obj.read()      
            if STMmsg is not None and ord((STMmsg)[0]) != 0:
                STMmsg = str(STMmsg)
                print("Message received from STM is: " + STMmsg)
                if (STMmsg == "R"):
                    self.sendToPC()
    
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
        STM_send_thread = threading.Thread(target=self.sendToSTM, args=("CHLT",), name="STM_send")
        
        #read threads for pc, STM and android
        pc_read_thread = threading.Thread(target=self.readFromPC, args=(), name="pc_read")
        STM_read_thread = threading.Thread(target=self.readFromSTM, args=(), name="STM_read")
    
        #set as daemon 
        #pc_send_thread.daemon = True
        pc_read_thread.daemon = True
        #STM_send_thread.daemon = True
        STM_read_thread.daemon = True

        #start threads -> dont start send threads!
        pc_read_thread.start()
        #pc_send_thread.start()
        STM_read_thread.start()
        STM_send_thread.start()

    def closeAll(self): #disconnect everything
        self.pc_obj.disconnect()
        self.STM_obj.close()



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