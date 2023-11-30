# Client

import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_message(message, public_key):
    cipher_text = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_text

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8080))

    server_public_key_data = client.recv(1024)
    server_public_key = serialization.load_pem_public_key(server_public_key_data, backend=default_backend())

    message = "Hello, Server!"
    encrypted_message = encrypt_message(message, server_public_key)

    client.sendall(encrypted_message)
    client.close()

if __name__ == "__main__":
    start_client()
