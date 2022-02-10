#Code for RPi and Android communication 
import time
import bluetooth

class android():
    def __init__(self):
        self.rfcommchannel = 3
        #Placeholder for Bluetooth RFCOMM socket
        self.socket = None
        
        #Placeholder for client connection instance
        self.client = None
        
        #Placeholder for client address
        self.client_address = None
        
        #UUID for Serial Port Profile
        self.uuid = "00001101-0000-1000-8000-00805F9B34FB" 

    def connect(self):
        try: 
            #Create Bluetooth RFCOMM socket
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            print('Bluetooth socket created')
            
            #Bind socket to channel 3
            self.socket.bind(("", bluetooth.PORT_ANY))
            print('Bluetooth binding completed')
            
            #Listen to 1 bluetooth connection a
            self.socket.listen(1)
            time.sleep(2)

            #Broadcast Bluetooth service
            bluetooth.advertise_service(self.socket, "MDPGrp10", service_id = self.uuid,
                                        service_classes = [self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                        profiles = [bluetooth.SERIAL_PORT_PROFILE])
            print("Waiting for connection") #str(self.rfcommchannel)

            #Accept client request
            self.client, self.client_address = self.socket.accept()
            print("Client accepted as: " + str(self.client))
            print("Client address info: " + str(self.client_address))

        except Exception as e:
            print(e)
            self.close()
            
    def send(self, msg):
        try:
        #Send message
            self.client.send(msg)
        except Exception as e:
            ex = 'Bluetooth Write Error: ' + str(e)
            ex = ex +'\nRetry Connection\n'
            print(ex)
            #self.connect()
            
    def read(self):
        try:
        #Receive message of maximum 2048 characters, encoded in utf-8
            received = self.client.recv(2048).decode("utf-8")
            return received
        except Exception as e:
            ex = "\nBluetooth Read Error: " + str(e)
            ex = ex + '\nRetry Connection\n'
            print(ex)
            #self.connect()

    def close(self):
        try:
            #If client exists, close it
            if self.client:
                self.client.close()
            #If the socket is still open, close it
            if self.socket:
                self.socket.close()
            print("Bluetooth connection closed")
        except Exception as e:
            print("Error " + str(e))