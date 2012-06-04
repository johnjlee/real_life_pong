import socket
import time
import sys
import bluetooth

#print "What is the IP address or hostname of the game server?"
#game_host = sys.stdin.readline().rstrip()
gs_host = "localhost"
gs_port = 10009

# phone_addr = '00:12:D1:FF:34:8E'  # manu's phone
phone_addr = '00:12:62:9F:EE:A2' # my phone
phone_port = 5



while True:
    #connect to game server as observer
    obs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obs.settimeout(1)
    obs.sendto("1", (gs_host, gs_port))

    #connect to phone 
    phone_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
##    phone_sock.connect((phone_addr, phone_port))
    
    try:        
        (response, address) = obs.recvfrom(1024)
        phone_sock.connect((phone_addr, phone_port))
        if len(response) > 0:
            lst = map(float, response.split(','))
            print "relay server received data from game server:"
            print "pos 1:",str(lst[0])
            print "pos 2:",str(lst[1])
            print "ball x:",str(lst[2])
            print "ball y:",str(lst[3])
            print "score 1:",str(lst[4])
            print "score 2:",str(lst[5])
            phone_sock.send(response)
        obs.close()
        phone_sock.close()
    except:
        obs.close()
        phone_sock.close()

    time.sleep(0.1)

    
        
        
