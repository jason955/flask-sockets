import socket
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1235
GNU_HOST = ""
GNU_PORT = 1236

DEMO_STATE = 0

gnuradio_socket = []




def zcu_comms(currentState):
	while True:
		if currentState == 0: #INIT

			gnuradio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			gnuradio_socket.bind((GNU_HOST,GNU_PORT))
			print("Connected to GNURadio")


			currentState = 1

		elif currentState == 1: #RUN
			if DEMO_STATE == 1: #RX Demo
				print("Running RX Demo")
				try:
					#while True:
					data = gnuradio_socket.recvfrom(1024)
					if data:
						print(data[0])
					client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					client_socket.connect((SERVER_HOST, SERVER_PORT))
					client_socket.sendall(data[0])
					ret_data = client_socket.recv(1024)
					client_socket.close()
					print(ret_data)
				except:
					print("error")
					pass

			elif DEMO_STATE == 2: #TX Demo
				print("Running TX Demo")
			elif DEMO_STATE == 3: #Replay Auto Demo
				print("Running Replay Auto Demo")
			elif DEMO_STATE == 4: #Replay Manual Demo
				print("Running Replay Manual Demo")
			else:
				print("Bad state. Closing socket connection")
				currentState = 2
		elif currentState == 2: #CLOSING
			print("\nClosing socket")
			gnuradio_socket.close()
			break
		else:
			print("Invalid State")

if __name__ == '__main__':
	#DEMO_STATE = int(sys.argv[1])
	DEMO_STATE = 1
	zcu_comms(0)
