#Code for RPi and STM communication 

import serial
import time
import os

class STM():
  def __init__(self):
    self.baud_rate = 115200
    self.port = '/dev/ttyUSB0'
    self.ser = None
  
  def connect(self):
    try:
        self.ser = serial.Serial(self.port, self.baud_rate)
        print('\nSerial connected/open at: ' + str(self.port))
    except Exception as err:
        print('\nSerial connection error: ' + str(err))
        self.connect()
        
  def send(self,Msg):
    try:
        #default encoding is utf8
        print('\nSending message: ' + str(Msg))
        self.ser.write(Msg.encode('utf-8')) 
    except Exception as err:
        print('\nSending message error')
        self.connect()
      
  def read(self):
    try:
        val = self.ser.read().decode('utf-8')
        return val
    except Exception as err:
        print('Reading in error' + str(err))
        self.connect()
                
  def close(self):
    try:
        #if serial is open, close it
        if self.ser:
            self.ser.close()
            print('\nSerial connection close')
    except Exception as err:
            print('\nError in closing serial connection ' + err)