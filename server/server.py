import socket
import threading

# PART 1.1: Server Implementation - Dictionary to store client sockets with their nicknames
clients = {}  # Format: {client_socket: nickname}

# PART 2.1: Private Channels - Dictionary to store chat channels and their members
channels = {}  # Format: {'channel_name': [client_socket1, client_socket2, ...]}

# PART 1.1: Broadcast function to send messages to all clients except the sender
def broadcast(message, exclude_client=None):
    for client in clients.keys():
        if client != exclude_client:
            try:
                client.send(message.encode())
            except:
                # PART 1.1: Error management and connection cleanup for failed connections
                client.close()
                remove_client(client)

# PART 1.1: Thread handler for each client connection
def handle_client(client_socket):
    try:
        # PART 2.3: Receive nickname for user authentication and add to clients list
        nickname = client_socket.recv(1024).decode()
        clients[client_socket] = nickname
        broadcast(f"{nickname} has joined the chat.")  # Notify other users

        while True:
            message = client_socket.recv(1024).decode()
            # PART 2.2: Process commands (like /join, /leave, /msg)
            if message.startswith('/'):
                process_command(client_socket, message)
            else:
                # PART 2.2: Broadcast normal messages to everyone in public chat
                broadcast(f"{nickname}: {message}", exclude_client=client_socket)
    except:
        # PART 1.1: Handle client disconnection
        remove_client(client_socket)
        client_socket.close()

# PART 2.1 and PART 2.2: Command handling for private messages, joining/leaving channels
def process_command(client_socket, message):
    nickname = clients[client_socket]
    parts = message.split()
    command = parts[0]

    if command == "/join":
        channel_name = parts[1]
        # PART 2.1: Join a channel (create if doesn't exist)
        if channel_name not in channels:
            channels[channel_name] = []
        channels[channel_name].append(client_socket)
        client_socket.send(f"Joined channel {channel_name}".encode())
    elif command == "/leave":
        channel_name = parts[1]
        if channel_name in channels and client_socket in channels[channel_name]:
            channels[channel_name].remove(client_socket)
            client_socket.send(f"Left channel {channel_name}".encode())
    elif command == "/msg":
        # PART 2.1: Private message to a specific user
        target_nickname = parts[1]
        private_message = ' '.join(parts[2:])
        for client, name in clients.items():
            if name == target_nickname:
                client.send(f"[Private from {nickname}]: {private_message}".encode())
                break

# PART 1.1: Cleanup function to remove disconnected clients
def remove_client(client_socket):
    if client_socket in clients:
        nickname = clients[client_socket]
        broadcast(f"{nickname} has left the chat.")  # Notify all users of disconnection
        del clients[client_socket]

# PART 1.1: Server socket setup to accept multiple clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # Set server to listen on all interfaces on port 12345
server.listen()  # Start listening for connections

print("Server is running and waiting for connections...")

# Main loop to accept new clients
while True:
    client_socket, addr = server.accept()
    print(f"New connection from {addr}")
    # Create a new thread for each connected client
    threading.Thread(target=handle_client, args=(client_socket,)).start()
