from socket import *
import json
import time

udpSocket = socket(AF_INET, SOCK_DGRAM)
socketPort = 5001

# Enable broadcasting
udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

udpSocket.bind(('', socketPort))

new_dict = {}
x = {}

print("Listening...")

while True:
    data, address = udpSocket.recvfrom(1024)
    content_data = json.loads(data)

    for chunk in content_data["chunks"]:
        chunk_name = chunk
        new_dict[chunk_name] = address[0]

    # Combine existing dictionary with new entries
    a = {**new_dict, **x}

    # Write dictionary to file
    with open('dict.txt', 'w') as file:
        json.dump(a, file)

    ip_addr = address[0]  # IP address of the sender
    print(a)

    time.sleep(5)
