import sys
import socket 
import struct 
import array 
import fcntl 

# Get the list of network interfaces
def get_interface_list():
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    return [namestr[i:i+32].split('\0', 1)[0] for i in range(0, outbytes, 32)]

# Get the MAC address for a network interface
def get_mac_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

# Get the list of open ports on the system
def get_open_ports():
    open_ports = []
    with open('/proc/net/tcp', 'r') as f:
        for line in f:
            fields = line.split()
            if fields[3] == '0A':  # Listen state
                open_ports.append(int(fields[1], 16))
    return open_ports

while True:
    print("\nMenu:")
    print("1. List network interfaces")
    print("2. List open ports")
    print("3. Quit")
    choice = input("Enter your choice: ")

    if choice == '1':
        interface_list = get_interface_list()
        for interface in interface_list:
            mac_address = get_mac_address(interface)
            print(f'Interface {interface}: MAC address {mac_address}')
    elif choice == '2':
        open_ports = get_open_ports()
        print(f'Open ports: {open_ports}')
    elif choice == '3':
        sys.exit()
    else:
        print("Invalid choice. Try again.")
