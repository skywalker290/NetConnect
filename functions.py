import pickle
import uuid
# def send_pdf(client_socket, filename):
#     with open(filename, 'rb') as file:
#         while True:
#             data = file.read(1024)
#             if not data:
#                 break
#             client_socket.send(data)

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


