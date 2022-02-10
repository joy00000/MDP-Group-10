#Code for RPi and PC communication 

import socket
import io
from sqlite3 import connect
#import picamera
#from PIL import Image
import time
from _thread import *

class pc():
    def __init__(self):
        self.IP_ADDRESS = "192.168.10.10"
        self.PORT = 3333
        self.isConnected = False
        self.serverSocket = None
        self.pcClient = None
        self.pcClientIP = None
        self.connectionCount = 0

        self.algoClient = None
        self.algoClientIP = None
    
    def connect(self):
        try: 
            if (self.isConnected == False):
                self.serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                print('Socket created')

                #prevent error if address is being used
                self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.serverSocket.bind((self.IP_ADDRESS, self.PORT))
                print('Socket binded')

                self.serverSocket.listen(2)
                print('Start listening for PC')
                
                #connect to image rec server
                self.pcClient, self.pcClientIP = self.serverSocket.accept()
                self.isConnected = True
                print('RPi connected with PC from ' + str(self.pcClient))
                self.connectionCount+=1
                print('Connection: ' + str(self.connectionCount))
                
                #connect to algo server
                self.algoClient, self.algoClientIP = self.serverSocket.accept()
                print('RPi connected with PC from ' + str(self.algoClient))
                self.connectionCount+=1
                print('Connection: ' + str(self.connectionCount))

        except Exception as e:
            print('Connection Error: ' + str(e))
    
    def readImg(self):
        try:
            msg = self.pcClient.recv(1024).decode('utf-8')
            #print("Message: " + msg) 
            return msg
        
        except Exception as err:
            print(err)
            self.connect()
            self.read() 

    def readAlgo(self):
        try:
            msg = self.pcClient1.recv(1024).decode('utf-8')
            #print("Message: " + msg) 
            return msg
        
        except Exception as err:
            print(err)
            self.connect()
            self.read()  
    
    def send(self, im):
        try:
            if(im != ""):
                if (self.isConnected == True):
                    self.pcClient.sendall(im)
                    return True
                else:
                    if (self.isConnected != True):
                        self.connect()
                    return False
            

        except Exception as e:
            print('Sending pic error: ' + str(e))
            self.connect()
            self.send(im)

    def disconnect(self):
        try:
            if self.serverSocket:
                self.serverSocket.close()
                print('RPi socket closed')
        except Exception as e:
            print('Error closing PC connection: ' + str(e))







