import optparse
from socket import *
import threading

parser = optparse.OptionParser('usage %prog -H ' +\
	'<target host> -p <target port>')
parser.add_option('-H', dest='tgtHost', type='string',\
	help='specify target host')
parser.add_option('-I', dest='tgtIp', type='string',\
	help='specify IP address')
parser.add_option('-p', dest='tgtPort', type='string',\
	help = 'specify target port')

(options, args) = parser.parse_args()
tgtHost = options.tgtHost
tgtIp = options.tgtIp
tgtPorts = str(options.tgtPort).split(',')

if (tgtPorts == None) or (tgtHost == None and tgtIp == None):
	print parser.usage
	exit(0)

tgtVict = tgtHost
if tgtVict == None:
	tgtVict = tgtIp
else:
	try:
		tgtVict = gethostbyname(tgtHost)
	except:
		print "Unable to resolve host"

screenlock = threading.Semaphore()
def connScan(tgtHost, tgtPort):
	try:
		mysock = socket(AF_INET, SOCK_STREAM)
		mysock.connect((tgtHost, tgtPort))
		mysock.send("Hello World !\r\n")
		results = mysock.recv(5)
		screenlock.acquire()
		print '\t[+] %d/tcp open ' % tgtPort + str(results)
	except:
		screenlock.acquire()
		print '\t[-] %d/tcp closed'% tgtPort
	screenlock.release()
	mysock.close()

def scanPort(tgtVict, tgtPorts):
	name = "none"
	try:
		names = gethostbyaddr(tgtVict)
		name = names[0]
	except:
		print "Could not resolve %s"% tgtVict
	print "Scanning %s"% name
	for tgtPort in tgtPorts:
		threading.Thread(target=connScan, args=(tgtVict, int(tgtPort))).start()

ip = tgtVict
split_ip = str(tgtVict).split(".")
last = int(split_ip[3])
root_ip = split_ip[0] + "." + split_ip[1] + "." + split_ip[2]
while last < 255:
	newVict = root_ip + "." + str(last)
	screenlock.acquire()
	print "Scanning %s " %newVict
	scanPort(newVict, tgtPorts)
	last += 1
	screenlock.release()
exit(0)
