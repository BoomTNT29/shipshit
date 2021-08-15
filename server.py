import socket
import threading

HEADER = 6400
PORT = 5050
SERVER = "ipv4"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn1, conn2):
	connected = True
	while connected:
		msg_1 = conn1.recv(HEADER)
		if msg_1.decode(FORMAT) == '':
			connected = False

		msg_2 = conn2.recv(HEADER)
		if msg_2.decode(FORMAT) == '':
			connected = False

		if connected:
			conn1.send(msg_2)
			conn2.send(msg_1)

		else:
			conn1.send(DISCONNECT_MESSAGE.encode(FORMAT))
			conn2.send(DISCONNECT_MESSAGE.encode(FORMAT))
			break
	
	conn1.close()
	conn2.close()

def start():
	server.listen()
	conn1, addr1 = server.accept()
	conn1.send("YELLOW".encode(FORMAT))
	print("connection 1")

	conn2, addr2 = server.accept()
	conn2.send("RED".encode(FORMAT))
	print("connection 2")
	handle_client(conn1, conn2)

while True:
	start()
