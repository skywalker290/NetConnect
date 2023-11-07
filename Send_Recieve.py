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
        filepush('Chat.txt','You-> '+message);

def sender_program(host,port=5001):
    sender_socket = socket.socket()
    sender_socket.connect((host, port))
    
    send_thread = threading.Thread(target=send_messages, args=(sender_socket,))
    send_thread.start()

def receive_messages(client_socket,address):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        name=str(address)
        filepush('Chat.txt',name+' :'+data);   

def reciver_program():
    host = "0.0.0.0"
    port = 5001

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    conn, address = server_socket.accept()
    print('Connection from: ' + str(address))

    receive_thread = threading.Thread(target=receive_messages, args=(conn,address))
    receive_thread.start()

if __name__=='__main__':
    port=5001
    host="192.168.183.196"# where we want to send

    sender=threading.Thread(target=reciver_program,args=(host,port))
    reciver=threading.Thread(target=reciver_program,args=())