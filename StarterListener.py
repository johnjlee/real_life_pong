import socket
import string
import threading
from Constants import *

class StarterListener (threading.Thread):
    def __init__(self, port, server):
        self.listen_port = port
        self.server = server
        self.sock = None
        self.exit_flag = False
        threading.Thread.__init__(self)

    def stop(self):
        if (self.sock != None):
            self.sock.close()
        self.exit_flag = True
            
    def run(self):
        while True:
            if (self.exit_flag):
                return

            # Uses UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("0.0.0.0", self.listen_port))
                
            (recieved, address) = sock.recvfrom(1024)
            command = string.atoi(recieved)
            
            if (command == ServerConstants.MSG_START_GAME):
                if self.server.IsGameStarted() == True:
                    sock.sendto(str(ServerConstants.MSG_START_INPROGRESS),
                                address)
                else:
                    self.server.StartGame()
                    sock.sendto(str(ServerConstants.MSG_START_OK), address)
                    
            sock.close()

