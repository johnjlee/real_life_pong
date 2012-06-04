import socket
import time

port = 10002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", port))

s.send("0")

response = s.recv(1024)
print "CHEATER: got ", response, " from server"

while True:
    obs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obs.settimeout(1)
    # 10009 is the default port for observers
    obs.sendto("1", ("localhost", 10009))
    try:
        (response, address) = obs.recvfrom(1024)
        if len(response) > 0:
            lst = map(float, response.split(', '))
            s.send(str(lst[3]))
            s.send('\n')
        obs.close()
    except (socket.timeout):
        obs.close()
    
    time.sleep(0.1)

