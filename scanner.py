import optparse
import time
import socket
import netaddr
import threading
from ctypes import *
import struct

parser = optparse.OptionParser('usage scanner -s <subnet> -h <host>')
parser.add_option('-s', type='string', dest='target_sub', \
	help='Specify target subnet')
parser.add_option('-H', type='string', dest='host',\
	help = 'Specify Host')
(options, args) = parser.parse_args()

target_sub = options.target_sub
host = options.host
if target_sub == None or host == None:
	print parser.usage
	exit(0)

magic_message = "nkosi"

def udp_sender(subnet, magic_message):
	time.sleep(5)
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for ip in netaddr.IPNetwork(subnet):
		try:
			sender.sendto(magic_message, ("%s" % ip, 65212))
		except:
			pass

t = threading.Thread(target=udp_sender, args=(target_sub, magic_message))
t.start()

class IP(Structure):
	_fields_ = [
		("v",	c_ubyte, 4),
		("hl",	c_ubyte, 4),
		("tos",	c_ubyte),
		("tl",	c_ushort),
		("id",	c_ushort),
		("off",	c_ushort),
		("ttl",	c_ubyte),
		("p",	c_ubyte),
		("sum",	c_ushort),
		("src",	c_uint32),
		("dst",	c_uint32)
	]
	
	def __new__(self, buf):
		return self.from_buffer_copy(buf)

	def __init__(self, buf):
		self.protocol_map = {1: "ICMP", 6:"TCP", 17:"UDP"}
		self.src_addr = socket.inet_ntoa(struct.pack("@I", self.src))
		self.dst_addr = socket.inet_ntoa(struct.pack("@I", self.dst))
		try:
			self.proto = self.protocol_map[self.p]
		except:
			self.proto = str(self.p)

class ICMP(Structure):
	_fields_ = [
		("type",	c_ubyte),
		("code",	c_ubyte),
		("sum",		c_ushort),
		("unused",	c_ushort),
		("hop",		c_ushort)
	]

	def __new__(self, buf):
		return self.from_buffer_copy(buf)

	def __init__(self, buf):
		pass

sniff_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
sniff_sock.bind((host, 0))
sniff_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

try:
	while True:
		raw_buf = sniff_sock.recvfrom(65565)[0]
		ip_head = IP(raw_buf)
		if ip_head.proto == "ICMP":
			offset = ip_head.hl * 4
			icmp_buf = raw_buf[offset: offset + sizeof(ICMP)]
			icmp_head = ICMP(icmp_buf)
			#if icmp_head.code == 3 and icmp_head.type == 3:
			if netaddr.IPAddress(ip_head.src_addr) in netaddr.IPNetwork(target_sub):
				print "got sommin %s" % ip_head.src_addr
				if raw_buf[len(raw_buf) - len(magic_message):] == magic_message:
					print "Host is up %s" % ip_head.src_addr
except KeyboardInterrupt:
	exit(1)
