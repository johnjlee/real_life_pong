import socket
import time
import sys
import string
import threading

class CricketListener(threading.Thread):
    def __init__(self, beacons, host='localhost', port=2947):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.send('r')
        self.socket.recv(256)
        threading.Thread.__init__(self)
        self.beacons = beacons
        self.last_5_readings = [0,0,0,0,0]
        self.debug = False

    def EnableDebug(self):
        self.debug = True

    def DisableDebug(self):
        self.debug = False
        
    def GetLast5Readings(self):
        return self.last_5_readings;

    def GetAverageReading(self):
        avg = 0
        while (avg == 0):
            for value in self.last_5_readings:
                avg += value
                
        return avg / 5.0
        
    def run(self):
        while True:
            cricket_string = self.socket.recv(256)
            lines = cricket_string.split('\n')
            for line in lines:
                values = line.split(",")
                if (len(values) == 6):
                    (space, name) = values[2] .split("=")
                    if (name in self.beacons):
                        (dist, real_distance) = values[4].split("=")
                        distance = int(real_distance, 16)
                        if (distance > 0):
                            self.last_5_readings = self.last_5_readings[1:]
                            if (self.debug == True):
                                print "READING: %s, %f"%(name, distance)
                            self.last_5_readings.append(distance)
    


print "What is the IP address or hostname of the game server?"
game_host = sys.stdin.readline()
game_host = game_host.rstrip()

# pick player 1 or 2
player = 0
while (player != 1 and player != 2):
    print "Which player are you? (1 or 2)"
    line = sys.stdin.readline()
    player = string.atoi(line)


print "Which beacon(s) are you holding? (comma delimited)"
beacon_line = sys.stdin.readline()
beacon_line = beacon_line.rstrip()
beacons = beacon_line.split(",")

for beacon in beacons:
    print "Listening to ", beacon


listener = CricketListener(beacons)
listener.start()
time.sleep(1)

print "Please stand in the 0 position. Press enter when you are there."
listener.EnableDebug()
sys.stdin.readline()
listener.DisableDebug()
zero = listener.GetAverageReading()

print "Please stand in the 1 position. Press enter when you are there."
listener.EnableDebug()
sys.stdin.readline()
listener.DisableDebug()
one = listener.GetAverageReading()

print "DEBUG: zero=%f, one=%f"%(zero, one)

print "OK, connecting to game server %s."%(game_host)

# connect to game server
port = 10000 + player
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((game_host, port))
s.send("0")
response = s.recv(1024)
print "CLIENT: got ", response, " from server"


while True:
    values = listener.GetLast5Readings()
    distance = values[4]
    real_value = (distance - zero) / (one - zero)
#    print "DEBUG: got %f, sending %f"%(distance, real_value)
    s.send(str(real_value))
    s.send('\n')
