import socket
import select
import sys
import threading
import queue

# 1 byte value [0, 255]
# IP addr has 4 bytes
# Port has number by 2 bytes

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

e = False
q = queue.Queue()

def get_message(server, que):
	while True:
		with threading.Lock() :
			message = server.recv(2048)
			if message:
				que.put(message)
				e = True
			else:
				message = sys.stdin.readline()
				if message :
					que.put(message)
					e = True	

t = threading.Thread(target=get_message, args=(server, q) )
try:
    t.start()
    while True:
        if e :
            print(q.get())
        else:
            message = input()
            message = bytearray(message, "utf-8")
            server.send(message)
            print(message.decode("utf-8"))
            e = False
finally:
    t.join()
    server.close()
