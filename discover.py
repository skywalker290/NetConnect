import socket
import psutil
from scapy.all import ARP, Ether, srp

def get_wireless_interface():
    for iface, addrs in psutil.net_if_addrs().items():
        if ("wl" or "Wireless") in iface.lower():
            return iface
    return None

def get_ip_address(interface_name):
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            if iface == interface_name:
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        return addr.address
        return "Not found"
    except Exception as e:
        return str(e)

def main():
    wireless_interface = get_wireless_interface()
    if wireless_interface:
        my_ip = get_ip_address(wireless_interface)

        if my_ip != "Not found" and not my_ip.startswith("127."):
            print(f"My IP address is: {my_ip}")
        else:
            print("Could not determine an external IP address.")

        target_ip = "/24"  # Replace with your network's subnet
        target_ip = my_ip + target_ip
        arp = ARP(pdst=target_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        result = srp(packet, timeout=3, verbose=0)[0]
        ip_mac = []

        for sent, received in result:
            ip_mac.append([received.psrc, received.hwsrc])
        print(ip_mac)
        return ip_mac
    else:
        print(wireless_interface)
        print("Wireless interface not found.")

if __name__ == '__main__':
    main()


