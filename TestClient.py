import socket
import time

port = 10001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", port))

s.send("0")

response = s.recv(1024)
print "CLIENT: got ", response, " from server"


blah = 0
for x in range(0,5):
    blah += 0.1
    print "CLIENT: sending position ", str(blah)
    s.send(str(blah))
    s.send('\n');
    time.sleep(7)

