import socket
import threading

HOST = socket.gethostname()
PORT = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
clients = []
nicknames = []

# broadcast message to all clients
def broadcast_msg(message):
    for client in clients:
        client.send(message)

# handles clients
def handle_client(client, addr):
    connected = True
    while connected:
        msg = client.recv(1024)
        if msg:
            # exiting from server
            if msg.decode('ascii')[-7:] == ': .exit':
                connected = False
            else:
                broadcast_msg(msg)

    # removes client and nickname from server when exiting
    index = clients.index(client)
    nickname = nicknames[index]
    clients.remove(client)
    client.close()
    broadcast_msg(f"{nickname} has left the chatroom.".encode('ascii'))
    print(f"{nickname} has left the server.")
    nicknames.remove(nickname)

def start_server():
    server.listen()
    while True:
        client, addr = server.accept()
        print("Connection has been established with a new client.")

        # gets nickname from client
        client.send("nickname".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f"The nickname of this client is {nickname}.")
        broadcast_msg(f"{nickname} has connected to the chatroom.".encode('ascii'))
        client.send("You are now connected to the chatroom.".encode('ascii'))

        # starts threading
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

print("Server is starting...")
start_server()

