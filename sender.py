import socket

def send_pdf(client_socket, filename):
    with open(filename, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)

def client_program():
    host = "localhost"  # Replace with the server's IP address
    port = 12345  # Use the same port as the server

    client_socket = socket.socket()
    client_socket.connect((host, port))

    filename = "test.pdf"  # Replace with the path to the PDF file you want to send
    send_pdf(client_socket, filename)
    print("PDF sent successfully")

    client_socket.close()

if __name__ == '__main__':
    client_program()
