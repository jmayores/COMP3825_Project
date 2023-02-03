import socket
import threading
import sys

HOST = socket.gethostname()
PORT = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nickname = input("Choose a nickname: ")

# receives message from server
def client_receive():
    try:
        while True:
            message = client.recv(1024).decode('ascii')

            # if message is "nickname", sends client's nickname to server
            if message == "nickname":
                client.send(nickname.encode('ascii'))
            else:
                print(message)
    except:
        sys.exit()

# sends message to server
def client_send():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

        # exiting
        if message == f'{nickname}: .exit':
            print("Disconnecting from server...")
            client.close()
            sys.exit()

# begins threading
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
