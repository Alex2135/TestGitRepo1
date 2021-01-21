import socket
import json
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
connections = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("LOL, KEK")
server.bind((HOST, PORT))
server.listen()

list_of_clients = []

def user_connect(conn, addr):
    conn.send(b"Welcome to chatroom!")
    while True:
        try:
            message = conn.recv(2048)
            if message:
                send_mess = f"From {addr} : {message}"
                send_mess = bytearray(send_mess, "utf-8")
                print(send_mess)
                broadcast(send_mess, conn)
        except:
            continue

def broadcast(message, conn):
    for client in list_of_clients:
        if client != conn:
            try:
                conn.send(message)
            except:
                conn.close()

                if client in list_of_clients:
                    list_of_clients.remove(client)

list_of_threads = []
try:
    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        conn.send()
        print(addr, "connected")
        t = threading.Thread(target=user_connect, args=(conn, addr))
        list_of_threads.append(t)
        t.start()
finally:
    for t in list_of_threads:
        t.join()
    for c in list_of_clients:
        c.close()
    server.close()