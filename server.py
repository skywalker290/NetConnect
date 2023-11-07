import socket

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to your device's IPv4 address and a specific port
server_socket.bind(("192.168.16.92", 12345))  # Replace with your IPv4 address

# Listen for incoming connections
server_socket.listen(5)

print("Server is listening for connections...")

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")

    # Handle client messages
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode('utf-8')}")

    # Close the client connection
    client_socket.close()
