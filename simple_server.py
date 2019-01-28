import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
hostname = socket.gethostname()
port = 12345
sock.bind((hostname, port))
sock.listen(5)
while True:
	conn, addr = sock.accept()
	print "Got connection from ", addr, conn.gethostname();
	conn.send("Thank you for connecting")
	conn.close()
