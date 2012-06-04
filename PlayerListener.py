import socket
import string
import threading
from Constants import *

class PlayerListener (threading.Thread):
    def __init__(self, port, player, server):
        self.listen_port = port
        self.player = player
        self.server = server
        self.recieving_data = False
        self.client = None
        self.sock = None
        self.exit_flag = False
        threading.Thread.__init__(self)

    def stop(self):
        if (self.sock != None):
            self.sock.close()
        if (self.client != None):
            self.client.close()
        self.exit_flag = True
            
    def run(self):
        while True:
            if (self.exit_flag):
                return
            
            # If a client has not connected yet, wait for one to connect:
            if (not self.recieving_data):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind(("0.0.0.0", self.listen_port))
                self.sock.listen(1)
                (client, address) = self.sock.accept()
                
                self.client = client
                recieved = client.recv(1024)
                command = string.atoi(recieved)

                # If the player slot is open, then we can play.
                if (command == ServerConstants.MSG_REGISTER_CLIENT):
                    self.client.send(str(ServerConstants.MSG_CLIENT_OK))
                    self.recieving_data = True
                    self.sock.close()
                else:
                    self.client.send(str(ServerConstants.MSG_CLIENT_ERROR))
                    self.client.close()

            # Otherwise, if we're already connected:
            else:
                recieved = self.client.recv(1024)

                # If we've lost the connection, start listening again
                if (len(recieved) == 0):
                    self.recieving_data = False
                    self.sock.close()
                    self.client.close()
                # Otherwise, update the game server with the new data
                else:
                    value = recieved.split('\n')
                    for val in value:
                        if (len(val) > 0):
                            last_value = string.atof(val)
                            self.server.SetPosition(self.player, last_value)
