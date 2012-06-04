import socket
import time
import wx
import threading
from Constants import *

class GamePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        wx.EVT_PAINT(self, self.OnPaint)
        self.ballX = 50
        self.ballY = 50
        self.player1 = 50
        self.player2 = 50
        self.score1 = 0
        self.score2 = 0
        self.halfwidth = ServerConstants.PADDLE_WIDTH * 50
        
    def SetGameState(self, p1, p2, bx, by, s1, s2):
        self.ballX = bx * 100
        self.ballY = by * 100
        self.player1 = p1 * 100
        self.player2 = p2 * 100
        self.score1 = s1
        self.score2 = s2
        self.Refresh(False)
        
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("BLACK"))
        dc.SetPen(wx.Pen("BLACK", 10))
        dc.SetBrush(wx.Brush("BLACK"))
        dc.Clear()

        dc.SetPen(wx.Pen("WHITE", 10))
        dc.SetTextBackground("BLACK")
        dc.SetTextForeground("WHITE")
        
        (width, height) = dc.GetSize()
        scaleX = width/100.0
        scaleY = height/100.0
        dc.DrawLine(5, int(scaleY*(100 - self.player1 - self.halfwidth)),
                    5, int(scaleY*(100 - self.player1 + self.halfwidth)))
        dc.DrawLine(int(scaleX*100 - 5),
                    int(scaleY*(100 - self.player2 - self.halfwidth)),
                    int(scaleX*100 - 5),
                    int(scaleY*(100 - self.player2 + self.halfwidth)))
        dc.DrawCircle(int(scaleX*self.ballX),
                      int(scaleY*(100-self.ballY)), 5)

        score_string = "%d : %d"%(self.score1, self.score2)
        dc.DrawText(score_string, int(width/2.0 - 10), 10);
        

class GameObserver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.app = wx.PySimpleApp(0)
        self.frame = wx.Frame(None, -1, "Draw on Frame")
        self.panel = GamePanel(self.frame)
        self.frame.Show(True)

    def DoUpdate(self):
        port = 10009
        address = ("localhost", port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        try:
            s.sendto("1", address)
            (response, address) = s.recvfrom(1024)
            lst = map(float, response.split(', '))
            self.panel.SetGameState(lst[0], lst[1], lst[2], lst[3],
                                    lst[4], lst[5])
            s.close()
        except(socket.timeout):
            s.close()
        
    def run(self):
        self.app.MainLoop()        



#print "OBS: got ", response, " from server"



# start the UI thread
gameobs = GameObserver()
gameobs.start()
    
# notify the UI thread every 10 msec
while True:
    time.sleep(0.1)
    gameobs.DoUpdate()
