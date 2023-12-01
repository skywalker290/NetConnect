import pickle
import uuid
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os, platform
import socket



def send_image(client_socket, filename):
    with open(filename,'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)


def receive_image(server_socket, filename):
    with open(filename,'wb') as file:
        while True:
            data = server_socket.recv(1024) 
            if not data:
                break
            file.write(data)

# def send_image(client_socket, filename, public_key):
#     with open(filename, 'rb') as file:
#         while True:
#             data = file.read(1024)  
#             if not data:
#                 break
#             encrypted_data = public_key.encrypt(data,padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None)
#     )
#             client_socket.send(encrypted_data)

def Send_image(sender_socket, filename,  public_key):
    # Read the file and encrypt and send each chunk
    with open(filename, 'rb') as file:
        while True:
            data = file.read(128)  # Use 117 bytes for RSA 1024-bit key
            if not data:
                break
            encrypted_data = public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            sender_socket.send(encrypted_data)

    sender_socket.send(b'')
            

def Receive_image(server_socket, output_filename,private_key ):
    with open(output_filename, 'wb') as file:
        while True:
            encrypted_data = server_socket.recv(128 )  # Use 128 bytes for RSA 1024-bit key
            if not encrypted_data:
                break
            decrypted_data = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
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
    try:
        # If the key is a private key, extract the public key
        if isinstance(key, rsa.RSAPrivateKey):
            key = key.public_key()

        # Serialize the public key to PEM format
        serialized_key = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return serialized_key
    except Exception as e:
        print(f"Error in serialize_key: {e}")
        return None

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
    try:
        decrypted_message = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()
    except Exception as e:
        print(f"Error in decrypt_message: {e}")
        return None

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

def encrypt_serialized_data(data, public_key):
    try:
        # Serialize the data
        serialized_data = pickle.dumps(data)

        # Encrypt the serialized data
        encrypted_data = public_key.encrypt(
            serialized_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_data

    except Exception as e:
        print(f"Error in encrypt_serialized_data: {e}")
        return None
    
def decrypt_and_deserialize(encrypted_data, private_key):
    try:
        # Decrypt the data
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Deserialize the decrypted data
        original_data = pickle.loads(decrypted_data)

        return original_data

    except Exception as e:
        print(f"Error in decrypt_and_deserialize: {e}")
        return None

def save_text_to_file(file_path, text):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text saved successfully to {file_path}")
    except Exception as e:
        print(f"Error saving text to {file_path}: {e}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None

