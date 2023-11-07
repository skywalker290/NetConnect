import pickle
import uuid

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

def send_image(file_path):
    try:
        with open(file_path, 'rb') as file:
            image_data = file.read()
            return image_data
        print("Image sent successfully.")
    except Exception as e:
        print(f"Error sending image: {str(e)}")

def receive_image(file_path,image_data):
    try:
        with open(file_path, 'wb') as file:
            file.write(image_data)
            return 
    except Exception as e:
        print(f"Error receiving image: {str(e)}")


