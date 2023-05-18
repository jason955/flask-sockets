import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1240

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
client_socket.sendall(b"data")
ret_data = client_socket.recv(1024)
client_socket.close()
print(ret_data)