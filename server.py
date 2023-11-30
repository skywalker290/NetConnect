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

def serialize_key(key):
    return key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def decrypt_message(cipher_text, private_key):
    decrypted_message = private_key.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(1)

    print("Server listening on port 8080...")

    private_key, public_key = generate_key_pair()

    while True:
        conn, addr = server.accept()
        with conn:
            print('Connected by', addr)
            conn.sendall(serialize_key(public_key))
            data = conn.recv(1024)
            decrypted_data = decrypt_message(data, private_key)
            print('Received:', decrypted_data)

if __name__ == "__main__":
    start_server()
