import socket
import string
import threading
from Constants import *

class ObserverListener (threading.Thread):
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
            print address
            command = string.atoi(recieved)
            
            if (command == ServerConstants.MSG_GET_GAME_STATE):
                sock.sendto(self.server.GetGameState(), address)

            sock.close()

