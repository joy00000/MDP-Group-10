#hardcode for week 9

import threading
from androidComm import *
from stmComm import *

class RPI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        #Define subsystem objects
        self.android_obj = android()
        self.STM_obj = STM()
        
        #Establish connection to all the subsystem
        self.android_obj.connect()
        self.STM_obj.connect()

        #distance to change
        self.distance = 200
        self.travelled = 0

    #Function to receive from Android
    def readFromAndroid(self):
        while True:
            androidmsg = self.android_obj.read()
            if(androidmsg):
                androidmsg = str(androidmsg)
                print("Message received from android is: " + str(androidmsg))
                if androidmsg == "START":
                    self.sendToSTM("MOVE")
                    
                
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
                    
        
    def start_threads(self):
        #send/write threads for pc, STM and android
        #STM_send_thread = threading.Thread(target=self.sendToSTM, args=(), name="STM_send")
        
        #read threads for pc, STM and android
        STM_read_thread = threading.Thread(target=self.readFromSTM, args=(), name="STM_read")
        android_read_thread = threading.Thread(target=self.readFromAndroid, args=(), name="android_read")

        #set as daemon 
        #STM_send_thread.daemon = True
        STM_read_thread.daemon = True
        android_read_thread.daemon = True

        #start threads -> dont start send threads!
        STM_read_thread.start()
        #STM_send_thread.start()
        android_read_thread.start()

    def closeAll(self): #disconnect everything
        self.android_obj.close()
        self.STM_obj.close()



if __name__ == "__main__":
    main = RPI()
    try:
        main.start_threads()
        while True:
            pass
    except KeyboardInterrupt:
        main.closeAll()