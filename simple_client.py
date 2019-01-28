import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
host = socket.gethostname()
port = 12345
sock.connect((host, port))
print sock.recv(1024)
sock.close()
