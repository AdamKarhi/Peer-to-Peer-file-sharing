import os
import time
from socket import *
import json

port = 8000

file_name = input("Enter file name to download: ")
chunknames = [file_name + '_1', file_name + '_2', file_name + '_3', file_name + '_4', file_name + '_5']

with open('dict.txt', 'r') as file:
    contentDict = json.load(file)

# Check if chunks are already available locally
missing_chunks = [chunk for chunk in chunknames if chunk not in os.listdir()]

if missing_chunks:
    print("Missing chunks:", missing_chunks)

    # Request missing chunks from the server
    data = {
        "requested_chunks": missing_chunks
    }
    newData = json.dumps(data)

    try:
        tcpSock = socket(AF_INET, SOCK_STREAM)
        tcpSock.settimeout(10)  # Set a timeout value of 10 seconds

        for IP in contentDict.values():
            try:
                tcpSock.connect((IP, port))
                tcpSock.send(newData.encode())

                for chunk in missing_chunks:
                    received_data = b""
                    while True:
                        data = tcpSock.recv(1024)
                        received_data += data
                        if not data:
                            break

                    with open(chunk, 'wb') as f:
                        f.write(received_data)

                print("Missing chunks downloaded from the server.")
                break

            except timeout:
                print("Connection timed out. Trying another peer...")
                continue

        tcpSock.close()

    except ConnectionRefusedError:
        print("Connection refused. Unable to retrieve missing chunks.")

# Combine the downloaded chunks into the final file
with open('sentPhoto' + '.png', 'wb') as outfile:
    for chunk in chunknames:
        with open(chunk, 'rb') as infile:
            outfile.write(infile.read())

print("File", file_name + '.png', "is successfully downloaded and combined.")
