import pickle
import uuid
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os, platform



def send_image(client_socket, filename):
    with open(filename, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)


def receive_image(server_socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            file.write(data)

def send_image(client_socket, filename, public_key):
    with open(filename, 'rb') as file:
        while True:
            data = file.read(1024)  
            if not data:
                break
            encrypted_data = encrypt_message(data, public_key)
            client_socket.send(encrypted_data)

def receive_image(server_socket, filename, private_key):
    with open(filename, 'wb') as file:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            decrypted_data = decrypt_message(data, private_key)
            file.write(decrypted_data)

def serialize(data):
    try:
        serialized_data = pickle.dumps(data)
        return serialized_data
    except Exception as e:
        print(f"Error during serialization: {str(e)}")
        return None

def deserialize(serialized_data):
    try:
        data = pickle.loads(serialized_data)
        return data
    except Exception as e:
        print(f"Error during deserialization: {str(e)}")
        return None

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e+2] for e in range(0, 12, 2)])


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

def deserialize_key(server_public_key_data):
    server_public_key = serialization.load_pem_public_key(server_public_key_data, backend=default_backend())
    return server_public_key



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

def clear_terminal():
    system_platform = platform.system().lower()
    if system_platform == "windows":
        os.system("cls")
    else:
        os.system("clear")

def show_chat():
    clear_terminal()
    file_path="Chat.txt"
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

