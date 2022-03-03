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
        
        self.STM_obj = STM()
        
        #Establish connection to all the subsystem
        
        self.STM_obj.connect()
        
        # save camera to class
        self.camera = None
        self.imgCount = 0
        self.conversion = {'1_blue': "11",'2_green': "12", '3_red':"13", '4_white':"14", '5_yellow':"15", '6_blue':"16", 
        '7_green':"17", '8_red':"18", '9_white':"19", 'a_red':"20", 'b_green':"21", 'c_white':"22",
        'd_blue':"23",  'e_yellow':"24", 'f_red':"25",  'g_green':"26",'h_white':"27",  's_blue':"28", 't_yellow':"29", 'u_red':"30", 
        'v_green':"31", 'w_white':"32", 'x_blue':"33", 'y_yellow':"34", 'z_red':"35",'up_arrow_white':"36", 
        'down_arrow_red':"37",'right_arrow_green':"38",'left_arrow_blue':"39", 'circle_yellow':"40"}

    #Send Function to STM 
    def sendToSTM(self, newmsg):
        #while True:
            #msg = input("type:")
            #msgToSTM = input("msg:" )
        for msg in newmsg:
            self.STM_obj.send(str(msg))
            print("Message sent to STM is " + msg)
            time.sleep(1)
    
    #Function to receive from STM
    def readFromSTM(self):
        print("in read stm")
        while True:
            STMmsg = self.STM_obj.read()      
            if STMmsg is not None and ord((STMmsg)[0]) != 0:
                STMmsg = str(STMmsg)
                print("Message received from STM is: " + STMmsg)
                if (STMmsg == "R"):
                   self.sendToSTM("DONE")
    
        
    def start_threads(self):
        
        STM_send_thread = threading.Thread(target=self.sendToSTM, args=(['OSLT','BW04','OSRT','FW04','OSRT','FW02','TAKE', 'OSLT','FW06','OSRT','FW03','OSLT','FW01','TAKE','OSLT','FW05','TAKE','BW02','OSLT','FW08'],), name="STM_send")
        
        STM_read_thread = threading.Thread(target=self.readFromSTM, args=(), name="STM_read")
    
        STM_read_thread.daemon = True

    
        STM_read_thread.start()
        STM_send_thread.start()

    def closeAll(self): #disconnect everything
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