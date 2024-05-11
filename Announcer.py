from socket import *
import time
import os
import math
import json

sock = socket(AF_INET, SOCK_DGRAM)  # construct UDP
serverPort = 5001
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # setting UDP option to broadcast

content_name = input("Please enter which content you have: ")

# Read the IP addresses from dict.txt
with open('dict.txt', 'r') as file:
    contentDict = json.load(file)

chunknames = [content_name + '_1', content_name + '_2', content_name + '_3', content_name + '_4', content_name + '_5']

file_name = content_name + '.png'

c = os.path.getsize(file_name)
CHUNK_SIZE = math.ceil(math.ceil(c) / 5)

index = 1
with open(file_name, 'rb') as infile:
    chunk = infile.read(int(CHUNK_SIZE))
    while chunk:
        chunkname = content_name + "_" + str(index)
        print(chunkname)
        with open(chunkname, 'wb') as chunk_file:
            chunk_file.write(chunk)
        index += 1
        chunk = infile.read(int(CHUNK_SIZE))

# Parsing file into 5 chunks
print(str(index - 1) + " Chunks created")
print("Starting to announce chunks...")

data = {
    'chunks': [content_name + "_1", content_name + "_2", content_name + "_3", content_name + "_4", content_name + "_5"],
}

newData = json.dumps(data)

while True:
    for IP in contentDict.values():
        sock.sendto(newData.encode('utf-8'), (IP, serverPort))
    time.sleep(60)
