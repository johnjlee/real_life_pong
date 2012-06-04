import socket
import time

port = 10008
address = ("localhost", port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(1)

try:
    s.sendto("2", address)
    (response, address) = s.recvfrom(1024)
    print "RESPONSE: %s"%response
    s.close()
except(socket.timeout):
    print "EXCEPT"
    s.close()
    
        
