import socket 
import struct 
import textwrap 


def get_mac_addr(mac):
    # Convert MAC address from bytes to string format
    mac_str = map('{:02x}'.format, mac)
    # Join the MAC address parts with colons to create a formatted string
    return ':'.join(mac_str).upper()

def main():
        conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.ntohs(3))
        
        while True:
             raw_data, addr = conn.recvfrom(65536)
             dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
             print('/nEthernet Frame:')
             print('Destination: {}, Source {}, Protocol {}'.format(dest_mac, src_mac,eth_proto))


# unpack ethernet frame 
def ethernet_frame (data):
    dest_mac, src_mac, proto =struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac),get_mac_addr(src_mac), socket.htons(proto), data[14:]

#return properly formatted MAC address (i.e AA:BB:CC:DD:EE:FF)
def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()


main()