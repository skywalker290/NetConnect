import uuid

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e+2] for e in range(0, 12, 2)])

if __name__ == '__main__':
    try:
        mac_address = get_mac_address()
        print(f"MAC Address: {mac_address}")
    except:
        print("Failed to retrieve MAC address.")
