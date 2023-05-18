from threading import Thread, Event
from time import sleep
import socket
HOST = "127.0.0.1"
PORT = 1237
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1237

event = Event()

def tcp_server():
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        conn, addr = server_socket.accept()
        data = conn.recv(1024)
        conn.sendall(b"Data Received")
        html(data)
    server_socket.close()
    if data:
        print("Received data: " + str(data))
		
def tcp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    client_socket.sendall(b"data")
    ret_data = client_socket.recv(1024)
    client_socket.close()
    print(ret_data)


def html(data):
    print("JB")
    print(data)
    print("JB")

tcp_server_t = Thread(target=tcp_server)
tcp_client_t = Thread(target=tcp_client)

tcp_server_t.start()
tcp_client_t.start()

tcp_server_t.join()
tcp_client_t.join()
