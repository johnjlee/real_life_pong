from socket import *
import time
import sys
import string
import threading
import bluetooth
from math import *
from newgps import *

class GPSListener(threading.Thread):
    def __init__(self):
        self.gps = my_gps()
        fix = self.gps.get_fix()
        threading.Thread.__init__(self)
        self.debug = False
        self.last_reading = (0,0)
        
    def EnableDebug(self):
        self.debug = True

    def DisableDebug(self):
        self.debug = False
        
    def GetLastReading(self):
        return self.last_reading

    def Calibrate(self, zero, one):
        self.zeroX = zero[0]
        self.zeroY = zero[1]
        self.oneX = one[0]
        self.oneY = one[1]

    def ConvertToDistance(self, pair):
        a = pair[0]
        b = pair[1]
        zeroX = self.zeroX
        zeroY = self.zeroY
        oneX = self.oneX
        oneY = self.oneY
        ynorm = sqrt( (a-zeroX)*(a-zeroX) + (b-zeroY)*(b-zeroY))
        yhat = ((a - zeroX)/ynorm, (b - zeroY)/ynorm)

        znorm = sqrt( (oneX-zeroX)*(oneX-zeroX) + (oneY-zeroY)*(oneY-zeroY))
        zhat = ((oneX-zeroX)/znorm, (oneY-zeroY)/znorm)

        distance = (yhat[0]*zhat[0] + yhat[1]*zhat[1]) * ynorm
        distance /= znorm
        return distance
    
    def run(self):
        while True:
            sentence = self.gps.get_sentence_slowly()
            if (self.gps.valid_sentence(sentence)):
                reading = self.gps.readings()
                self.last_reading = (reading[0], reading[1])
                print "Got reading %f %f" % (reading[0], reading[1])


print "What is the IP address or hostname of the game server?"
game_host = sys.stdin.readline()
game_host = game_host.rstrip()

# pick player 1 or 2
player = 0
while (player != 1 and player != 2):
    print "Which player are you? (1 or 2)"
    line = sys.stdin.readline()
    player = string.atoi(line)


listener = GPSListener()
listener.start()
time.sleep(1)

print "Please stand in the 0 position. Press enter when you are there."
listener.EnableDebug()
sys.stdin.readline()
listener.DisableDebug()
zero = listener.GetLastReading()

print "Please stand in the 1 position. Press enter when you are there."
listener.EnableDebug()
sys.stdin.readline()
listener.DisableDebug()
one = listener.GetLastReading()

listener.Calibrate(zero, one)

print "OK, connecting to game server %s."%(game_host)

# connect to game server
port = 10000 + player
s = socket(AF_INET, SOCK_STREAM)
s.connect((game_host, port))
s.send("0")
response = s.recv(1024)
print "CLIENT: got ", response, " from server"


while True:
    value = listener.GetLastReading()
    distance = listener.ConvertToDistance(value)
    print "DEBUG: sending %f"%(distance)
    s.send(str(distance))
    s.send('\n')
    time.sleep(0.1)
