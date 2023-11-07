import socket
import threading
import pickle # serialization
from functions import * 

def filepush(file_path, text):
    try:
        with open(file_path, 'a') as file:
            file.write(text)
            file.write('\n')  # Add a newline character to separate entries
        # print(f"Appended text to {file_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

def send_image(file_path, client_socket):
    try:
        with open(file_path, 'rb') as file:
            image_data = file.read()
            client_socket.send(image_data)
        print("Image sent successfully.")
    except Exception as e:
        print(f"Error sending image: {str(e)}")

def receive_image(file_path, server_socket):
    try:
        image_data = server_socket.recv(1024)
        with open(file_path, 'wb') as file:
            file.write(image_data)
        print("Image received and saved successfully.")
    except Exception as e:
        print(f"Error receiving image: {str(e)}")



def send_messages(client_socket):
    while True:
        message = input('You -> ')
        filepush('server.txt','You -> '+message);
        client_socket.send(message.encode())

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        # print('Received from connected user: ' + data)
        filepush('server.txt','user: '+data);

def server_program():
    host = socket.gethostname()
    port = 5001

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)

    conn, address = server_socket.accept()
    print('Connection from: ' + str(conn))

    # Create two threads for sending and receiving messages
    send_thread = threading.Thread(target=send_messages, args=(conn,))
    receive_thread = threading.Thread(target=receive_messages, args=(conn,))

    send_thread.start()
    receive_thread.start()

if __name__ == '__main__':
    server_program()



# Example usage:
file_path = 'server.txt'