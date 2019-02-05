import socket
import os
import ctypes
import struct
import optparse
import threading
import time
import netaddr

class IP(ctypes.Structure): #Structure allows to map c-data types to fields
	_fields_ = [ # From C struct 'ip'
		("ihl",		ctypes.c_ubyte, 4), # length 4 bit width
		("version", ctypes.c_ubyte, 4), # version 4 bit width
		("tos",		ctypes.c_ubyte), # type of service
		("len", 	ctypes.c_ushort),
		("id",		ctypes.c_ushort),
		("off",		ctypes.c_ushort),
		("ttl",		ctypes.c_ubyte),
		("p",		ctypes.c_ubyte),
		("sum",		ctypes.c_ushort),
		("src",		ctypes.c_uint32),
		("dst",		ctypes.c_uint32)
	]

	def __new__(self, buf=None):
		return self.from_buffer_copy(buf)

	def __init__(self, buf=None):
		self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
		self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
		self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))

		try:
			self.protocol = self.protocol_map[self.p]
		except:
			self.protocol = str(self.p)

class ICMP(ctypes.Structure):
	_fields_ = [
		("type",	ctypes.c_ubyte),
		("code",	ctypes.c_ubyte),
		("sum",		ctypes.c_ushort),
		("unused",	ctypes.c_ushort),
		("next",	ctypes.c_ushort)
	]

	def __new__(self, socket_buffer):
		return self.from_buffer_copy(socket_buffer)

	def __init__(self, socket_buffer):
		pass

parser = optparse.OptionParser('usage %prog -s <IP>')
parser.add_option('-s', dest='ip_sub', type='string', \
	help='Specify Target Subnet')

(options, args) = parser.parse_args()
host_ip = options.ip_sub
if host_ip == None:
	print parser.usage
	exit(0)

if os.name == "nt" : #windows
	socket_protocol = socket.IPPORTO_IP # windows allow all ip protocols
else:
	socket_protocol = socket.IPPROTO_ICMP #linux have to specify icmp

sniffer_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer_socket.bind((host_ip, 0))
sniffer_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
	sniffer_socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	# if windows send ioctl signal for SIO_RCVALL which allows port to accept all ip data

try:
	while True:
		raw_buffer = sniffer_socket.recvfrom(65565)[0]
		#print raw_buffer
		ip_head = IP(raw_buffer)
		print "Protocol: %s %s -> %s" % (ip_head.protocol, ip_head.src_address \
							, ip_head.dst_address)
		print ip_head.p
		if ip_head.protocol == "ICMP":
			offset = ip_head.ihl * 4 # Get size of ip header coz ICMP is after
			buf = raw_buffer[offset:offset + ctypes.sizeof(ICMP)] # Only get icmp info
			icmp_head = ICMP(buf)
			print "\tICMP -> Type: %d Code: %d" % (icmp_head.type, icmp_head.code)

except KeyboardInterrupt:
	if os.name == "nt":
		sniffer_socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
