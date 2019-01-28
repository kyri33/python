import optparse
from socket import *

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

def connScan(tgtHost, tgtPort):
	try:
		mysock = socket(AF_INET, SOCK_STREAM)
		mysock.connect((tgtHost, tgtPort))
		print '[+]%d/tcp open'% tgtPort
		mysock.close()
	except:
		print '[-]%d/tcp closed'% tgtPort

for tgtPort in tgtPorts:
	connScan(tgtVict, int(tgtPort))
