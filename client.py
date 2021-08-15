import socket

HEADER = 6400
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.126"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def set_boi():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)

def send(msg, send=True):
	if send:
		message = msg.encode(FORMAT)
		client.send(message)

	msgFromServer = client.recv(HEADER).decode(FORMAT)
	return msgFromServer