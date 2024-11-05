import socket
import threading

# PART 1.2: Function to handle receiving messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)  # Print received message to console
        except:
            # PART 1.2: Handle server disconnection and cleanup
            print("Disconnected from server.")
            client_socket.close()
            break

# PART 1.2: Function to handle sending messages from client to server
def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())  # Send message input to server

# PART 1.2: Connect to the server and set up threads for receiving/sending
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))  # Connect to server IP and port

# PART 2.3: Set nickname (authentication) by sending first message
nickname = input("Enter your nickname: ")
client_socket.send(nickname.encode())

# Create threads for receiving and sending messages simultaneously
threading.Thread(target=receive_messages, args=(client_socket,)).start()
send_messages(client_socket)
