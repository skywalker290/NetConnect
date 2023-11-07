import socket
import threading
import pickle
from two_way_server import filepush
from two_way_server import receive_image
from functions import *

def send_messages(client_socket):
    while True:
        message = input('You -> ')
        client_socket.send(message.encode())
        filepush('client.txt','You-> '+message);

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        # print('Received from the server: ' + data)
        filepush('client.txt','user: '+data);

def client_program():
    # host = socket.gethostname()
    host="192.168.183.196"
    port = 5001

    client_socket = socket.socket()

    client_socket.connect((host, port))

    # Create two threads for sending and receiving messages
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

if __name__ == '__main__':
    client_program()