import socket
import threading
import pickle
from two_way_server import filepush
from two_way_server import receive_image
from functions import *
import time


public_key, private_key =generate_key_pair()
client_public_key=0


stop_loops=1
reciver_port=5001 # server port


def send_messages(client_socket,mac_id):
    while True:
        message = input('You -> ')
        if(message[0:2]=="p "):
            type="photo"
            filename=message[2:]
            data=[filename,type,mac_id]
            filepush('Chat.txt','You-> '+filename+" Sent!");
            serial_data=serialize(data)
            client_socket.send(serial_data)
            send_image(client_socket,filename,client_public_key)
            continue
        else:
            type="Text"
            send_data=message
            send_data=encrypt_message(send_data,client_public_key)
            filepush('Chat.txt','You-> '+message);
            data=[send_data,type,mac_id]
            serial_data=serialize(data)
            client_socket.send(serial_data)
        show_chat()
            

        if(message=="EXIT 0000"):
            stop_loops=0
            return
        
        
        
        

def sender_program(host,port,mac_id):
    input("Server Running->")
    sender_socket = socket.socket()
    sender_socket.connect((host, port))
    sender_socket.send(public_key)

    
    send_thread = threading.Thread(target=send_messages, args=(sender_socket,mac_id))
    send_thread.start()





def receive_messages(client_socket,address):
    while stop_loops:
        deserial_data = client_socket.recv(1024)
        if not deserial_data:
            break
        name=str(address[0])
        data=(deserialize(deserial_data))

        data=list(data)
        
        rec_data=data[0]
        type=data[1]
        mac_=data[2]

        if(type=="photo"):

            filename=data[0]
            receive_image(client_socket,filename,private_key)
            filepush('Chat.txt',mac_+' :'+filename+" Recieved");
        
        else:
            text=rec_data
            text=decrypt_message(text,private_key)
            filepush('Chat.txt',mac_+' :'+text);
        
    client_socket.close()

def reciver_program():# port in use 5001
    host = "0.0.0.0"
    port = reciver_port

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)

    conn, address = server_socket.accept()
    print('Connection from: ' + str(address))
    client_public_key=server_socket.recv(1024)

    client_public_key=client_public_key


    receive_thread = threading.Thread(target=receive_messages, args=(conn,address))
    receive_thread.start()

if __name__=='__main__':
    port=5002
    host="192.168.38.130"# where we want to send
    # host = "localhost"
    # port =5001
    mac_id=get_mac_address()
    
    

    sender=threading.Thread(target=sender_program,args=(host,port,mac_id))
    reciver=threading.Thread(target=reciver_program,args=())
    sender.start()
    reciver.start()


