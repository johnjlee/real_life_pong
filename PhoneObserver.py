import e32
from socket import *
from appuifw import *

def msg_to_lst(msg):
    return map(float, msg.split(','))

def abort():
    listening = False
    appuifw.app.set_exit()

def print_game_state(lst):  # for debugging purposes
    appuifw.app.body.clear()
    appuifw.app.body.text((10,10), unicode("width: %d" % appuifw.app.body.size[0]))
    appuifw.app.body.text((10,20), unicode("height: %d" % appuifw.app.body.size[1]))
    appuifw.app.body.text((10,40), unicode("pos 1: %f" % lst[0]))
    appuifw.app.body.text((10,50), unicode("pos 2: %f" % lst[1]))
    appuifw.app.body.text((10,70), unicode("ball x: %f" % lst[2]))
    appuifw.app.body.text((10,80), unicode("ball y: %f" % lst[3]))
    appuifw.app.body.text((10,100), unicode("score 1: %f" % lst[4]))
    appuifw.app.body.text((10,110), unicode("score 2: %f" % lst[5]))
    
def draw_game_state(lst):
    width = float(appuifw.app.body.size[0])
    height = float(appuifw.app.body.size[1])
    pos1 = lst[0]
    pos2 = lst[1]
    ball_x = lst[2]*width
    ball_y = lst[3]*height
    score1 = int(lst[4])
    score2 = int(lst[5])
    
    appuifw.app.body.clear()
    #print score on top
    appuifw.app.body.text((69,10), unicode("%d : %d" % (lst[4], lst[5]))) 
    #paddles
    appuifw.app.body.rectangle( (1, height-(pos1+0.1)*height, 6, height-(pos1-0.1)*height), fill=0x00ff00)
    appuifw.app.body.rectangle( (width-6, height-(pos2+0.1)*height, width-1, height-(pos2-0.1)*height), fill=0x0000ff)
    #ball
    appuifw.app.body.ellipse( (ball_x-5, height-(ball_y+5), ball_x+5, height-(ball_y-5)), fill=0xff0000)


listen_port = 5
listening = True
#appuifw.app.body = appuifw.Canvas(self.handle_redraw, self.handle_event, None)
appuifw.app.body = appuifw.Canvas()
appuifw.app.exit_key_handler = abort


while listening:
    sock = socket(AF_BT, SOCK_STREAM)
    sock.bind(("", listen_port))
    set_security(sock, AUTH)
    sock.listen(1)
    try:
        (client, address) = sock.accept()
        msg = client.recv(1024)
        #print_game_state(msg_to_lst(msg))
        draw_game_state(msg_to_lst(msg))
    finally:
        sock.close()
        client.close()
    e32.ao_yield()
