import socket

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ("192.168.16.92", 12345)  # Replace with your server's IP address
client_socket.connect(server_address)

while True:
    message = input("Enter a message: ")
    client_socket.send(message.encode('utf-8'))
    if message.lower() == "exit":
        break

# Close the client socket
client_socket.close()
