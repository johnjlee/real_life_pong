from socket import *
import bluetooth

max_dbg_nest = 10
dbg_nest_level = 1

def dbg_exit(name,val,high_prio=False):
    global dbg_nest_level,max_dbg_nest
    dbg_nest_level -= 1
    if high_prio or dbg_nest_level < max_dbg_nest: 
	if len(val.__str__()) < 25:
	    print 'exiting:',name,' ret val:',val
	else:
	    print 'exiting:',name,' ret val len:',len(val.__str__())
    return val

def dbg_enter(name,high_prio=False):
    global dbg_nest_level,max_dbg_nest
    if high_prio or (dbg_nest_level < max_dbg_nest): 
	print 'entering:',name
    dbg_nest_level += 1

def dbg( str , high_prio=False):
    global dbg_nest_level
#    if high_prio or dbg_nest_level < max_dbg_nest: 
#b	print 'dbg:',str
    

def file_readlines( filename ):
    dbg_enter('file_readlines')
    try:
	f = open(filename,'r')
	r = f.readlines()
	f.close()
    except:
	dbg('failed to open file',True)
	r = []
    return dbg_exit('file_readlines',r)

#########################

class my_bt:
    def __init__(self,target):
	dbg_enter('my_bt init')
	try:
	    #self.sock = socket(AF_BT,SOCK_STREAM)
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	    sock.connect( target )
	    sock.close()
	    ret = True
	except:
	    ret = False
	return ret
	    

class my_gps:
#    def __init__(self,target=('00:08:0d:15:5a:7f',1),btid_filename= u'e://system//apps//python//my//gpsbtid.txt'):
    def __init__(self,target=('00:08:1B:8C:8F:06',1) ,btid_filename= u'e://system//apps//python//my//gpsbtid.txt'):
	"""  Initialize it with a the bluetooth idea and port of a default gps bluetooth device.
	     Also with a file name that can store other potential devices.  If the connection fails to
	     the default device, then will try the other devices. """
	print 'entering gps initialization, version 0.127'
#	dbg_enter('init')
	self.gps_buffer = ""
	self.target = target[0]
	self.target1 = target[1]
	self.haveFix, self.haveSpeed = False, False
	self.speed, self.course, self.lat, self.lon = 0.0,0.0,0.0,0.0
	self.inv_speed, self.inv_course, self.inv_lat, self.inv_lon = 0,0,0,0

	#self.sock = socket(AF_BT,SOCK_STREAM)
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        
	if not self.connect(self.target):
	    self.connect(self.target1)
#	if not self.connected:
#	    dbg('self connected is False')
#	    potential_targets = self.read_targets( btid_filename)
#	    for target in potential_targets:
#		self.connected = self.connect( target )
#	    if self.connected:
#		self.target = target
#	else:
#	    dbg('self connected is True')
#	dbg_exit('init',self.connected)


    def disconnect(self):
	dbg_enter('disconnect')
	self.sock.close()
	self.connected = False
	return dbg_exit('disconnect',self.connected)

    def connect(self,target=None):
	dbg_enter('connect')
	if target == None:  target = self.target
	try:
	    self.sock.connect( (target, self.target1) )
	    dbg('connected to gps')
	    self.connected = True
	except:
	    dbg('could not onnect to gps %s'%target)
	    self.connected = False
	return dbg_exit('connect',self.connected)


    def read_targets(self,filename):
	dbg_enter('read_targets')
	r = file_readlines(filename)
	list = []
	for t in r:
	    tt = eval(t)
	    list.append( (tt[0],int(tt[1])) )
	return dbg_exit('read_targets', list )

    def get_sentence_slowly(self):
	try:
	    chr = self.sock.recv(1)
	    while  chr != '$':
		chr = self.sock.recv(1)
	    cmd = chr
	    while chr != '\r':
		chr = self.sock.recv(1)
		cmd = cmd + chr
	    return cmd
	except:
	    dbg('trouble with recv')
	    return False

    def fill_gps_buffer(self):
	def read_them():
	    try:
		s = self.sock.recv(1024)    # read enough to drain the buffer
	    except:
		s = ""
	    if len(s) == 0: 
		dbg('bluetooth gps connection broken',True)
		self.connected = False
		return ""
	    return s

	dbg_enter('fill_gps_buffer')
#	self.gps_buffer = ""
	s = read_them()
	while len(s) == 1024:
#	        self.gps_buffer = self.gps_buffer + s
	        self.gps_buffer = self.gps_buffer + s
		s = read_them()
	self.gps_buffer = self.gps_buffer + s
	dbg('size of gps_buffer %d'%len(self.gps_buffer))
	return dbg_exit('fill_gps_buffer',True)

	
    def get_sentence(self):
	dbg_enter('get_sentence')
	d = self.gps_buffer.find('$GPRMC')
	dbg('GPRMC is at location %d in string'%d)
	if d == -1:
	    dbg('could not find sentence head')
	    self.fill_gps_buffer()
	    d = self.gps_buffer.find('$GPRMC')
	    if d == -1:
		return dbg_exit('get_sentence', False)

	self.gps_buffer = self.gps_buffer[d:] # strip away all the earlier crap if any
	e = self.gps_buffer.find('\r') 
	dbg(' slash r is at location %d in string'%e)
	if e == -1:
	    dbg('could not find end of sentence')  # hopefully, next time will find it
	    return dbg_exit('get_sentence', False)
	retval = self.gps_buffer[:e]
	self.gps_buffer = self.gps_buffer[e:]
	return dbg_exit('get_sentence', retval )



    def valid_sentence(self, sentence ):
	""" return either False, GPGAA, or GPRMS depending on sentence.
            If sentence has valid data, then set self.haveFix = 'valid' """
	if not sentence: return False
	if sentence[0:6] == "$GPGGA":
	    dbg("Found a GP G G A sentence")
	    try:
		fields = sentence.split(",")
		if fields[6] == '1': 
		    self.haveFix = 'valid'
		    self.lat, self.lon      = (float( fields[2] ),  float( fields[4] ))
		    return 'GPGAA'
	    except:
		dbg("Problem splitting up GPGAA record")
	    return False
	if sentence[0:6] == "$GPRMC":
	    dbg("Found a GP R M C sentence")
	    try:
		(GPRMC,ut,av,lat,ns,lon,ew,speed,course,utc,mag,magns,check)=sentence.split(",")
		dbg('split the GPRMC fields sucessful',True)
		self.lat, self.lon = (float(lat),  float(lon) )
		if av == 'A': 
		    self.haveFix = 'valid'
		    if speed and course:
			self.speed, self.course = (float(speed)*1.150779,float(course))
		    return 'GPRMC'
		else:
		    self.haveFix = 'invalid'
	    except:
		dbg("Problem splitting up GPRMC record")
	    return False


	
    def get_fix(self):
	""" return False: if no valid GPS reading (whether or not there is a connection)
	           True: if good reading, later must  call gps_readings to get values
        """
	dbg_enter('get_fix')

	if not self.connected:
	    dbg('getting fix while not connected')
	    self.connect()
	    if not self.connected:
		return dbg_exit('get_fix', False )

	self.gps_buffer = ""    # before we start, get rid of stuff left over from last probe
	self.fill_gps_buffer()

	self.haveFix = False
	for ii in range(10):
	    sentence = self.get_sentence_slowly()
	    if self.valid_sentence( sentence ) == 'GPRMC':
		return dbg_exit('get_fix',self.haveFix)
	return dbg_exit('get_fix',self.haveFix)













    def readings(self):
#	if self.lon < 7000.0:
#	    self.lon, self.lat = self.lat,self.lon
	return ( self.lat, self.lon, self.speed, self.course )

    def inv_readings(self):
	return ( self.inv_lon, self.inv_lat, self.inv_speed, self.inv_course )

    def str(self):
	return ( "( %f , %f )" % (self.lat,self.lon) )


if __name__ == '__main__':
    print "starting in main"
    g = my_gps()
    fix = g.get_fix()
    print "returned with fix",fix
    if fix == 'valid':
	print "success and valid from fix:",
	print "lat:%f,lon:%f,speed:%f,course:%f" % g.readings()

        while True:
            sentence = g.get_sentence_slowly()
            if (g.valid_sentence(sentence)):
                print "lat:%f,lon:%f,speed:%f,course:%f" % g.readings()
                
    if fix == 'Invalid':
	print "success but invalid from fix:",
	print "lat:%f,lon:%f,speed:%f,course:%f" % g.inv_readings()
    if not fix:
	print "failure"

    g.disconnect()    
