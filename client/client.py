import socket
import threading
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("Disconnected from server.")
                client_socket.close()
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        try:
            message = input()
            client_socket.send(message.encode('utf-8'))
            if message.lower() == "/quit":
                print("Exiting chat...")
                client_socket.close()
                sys.exit()
        except Exception as e:
            print(f"Error sending message: {e}")
            client_socket.close()
            sys.exit()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    # Prompt for nickname locally and send to server
    nickname = input("Enter your nickname: ")
    client_socket.send(nickname.encode('utf-8'))

    # Start threads for receiving and sending messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    threading.Thread(target=send_messages, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
