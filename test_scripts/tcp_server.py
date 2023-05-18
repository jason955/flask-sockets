import socket
import sys
from enum import Enum

HOST = "127.0.0.1"
PORT = 1235
DEMO_STATE = 0

#define a state variable
class State(Enum):
	INIT = 1
	RUN = 2
	CLOSE = 3


def zcu_comms(currentState,host,port):
	while True:
		if currentState == State.INIT:
			server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_socket.bind((HOST, PORT))
			server_socket.listen()
			conn, addr = server_socket.accept()

			print("Initialized") #TODO: Add error handling?
			currentState = State.RUN

		elif currentState == State.RUN:
			if DEMO_STATE == "1": #RX Demo
				print("Running RX Demo...")
				try:
					#while True:
					print(f"Connected by {addr}")
					data = conn.recv(1024)
					conn.sendall(b"Data Received")
					if data:
						print("Received data: " + str(data))
				except KeyboardInterrupt:
					pass
				currentState = State.CLOSE

			elif DEMO_STATE == "2": #TX Demo
				print("Running TX Demo...")
				try:
					while True:
						data = input("Enter payload: ")
						server_socket.send(data.encode())
						print("\tData sent to target")

				except KeyboardInterrupt:
					pass
				currentState = State.CLOSE

			elif DEMO_STATE == "3": #Replay Auto
				print("3")

			elif DEMO_STATE == "4": #Replay Manual
				print("Running Manual Replay...")
				try:
					while True:
						data = server_socket.recv(1024).decode()
						if data:
							x = input("Replay message: " + data + "\n Press enter to send")
							if not x:
								server_socket.send(data.encode())
								print("\tReplay sent to target\n")
				except KeyboardInterrupt:
					pass
				currentState = State.CLOSE
		
			else:
				print("Bad state. Closing socket connection")
				currentState = State.CLOSE

		elif currentState == State.CLOSE:
			print("\nClosing socket")
			server_socket.close()
			break
		else:
			print("Invalid State")

if __name__ == '__main__':
	DEMO_STATE = sys.argv[1]
	zcu_comms(State.INIT,HOST,PORT)


