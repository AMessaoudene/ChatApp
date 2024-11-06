import socket
import threading

clients = {}  # Dictionary to store client socket and nickname
channels = {}  # Dictionary to store channels with connected clients

def handle_client(client_socket):
    try:
        # Receive and store the client's nickname
        nickname = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = nickname
        broadcast(f"{nickname} has joined the chat.", client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("/"):
                handle_command(message, client_socket)
            else:
                broadcast(f"{nickname}: {message}", client_socket)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_disconnect(client_socket)

def handle_command(command, client_socket):
    if command.startswith("/list"):
        list_users(client_socket)
    elif command.startswith("/join "):
        join_channel(client_socket, command.split()[1])
    elif command.startswith("/leave"):
        leave_channel(client_socket)
    elif command.startswith("/help"):
        send_help(client_socket)
    elif command.startswith("/quit"):
        client_disconnect(client_socket)

def broadcast(message, client_socket=None):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client_disconnect(client)

def list_users(client_socket):
    active_users = ", ".join(clients.values())
    client_socket.send(f"Active users: {active_users}".encode('utf-8'))

def join_channel(client_socket, channel_name):
    if client_socket in channels.get(channel_name, []):
        client_socket.send("Already in this channel.".encode('utf-8'))
    else:
        channels.setdefault(channel_name, []).append(client_socket)
        broadcast(f"{clients[client_socket]} joined {channel_name} channel.", client_socket)

def leave_channel(client_socket):
    for channel, members in channels.items():
        if client_socket in members:
            members.remove(client_socket)
            broadcast(f"{clients[client_socket]} left {channel} channel.", client_socket)

def client_disconnect(client_socket):
    nickname = clients.pop(client_socket, None)
    if nickname:
        broadcast(f"{nickname} has left the chat.")
    for channel in channels.values():
        if client_socket in channel:
            channel.remove(client_socket)
    client_socket.close()

def send_help(client_socket):
    help_message = (
        "/help - Show this help message\n"
        "/list - List all active users\n"
        "/join <channel> - Join or create a channel\n"
        "/leave - Leave the current channel\n"
        "/quit - Quit the chat\n"
    )
    client_socket.send(help_message.encode('utf-8'))

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen()
    print("Server started on port 5555")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
