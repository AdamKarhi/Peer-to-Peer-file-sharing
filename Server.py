from socket import *
import json
import datetime

port = 8000
serverSock = socket(AF_INET, SOCK_STREAM)

serverSock.bind(('', port))

serverSock.listen(5)

print("Server listening...")

while True:
    conn, address = serverSock.accept()
    print("Connected to:", address)

    received_data = b""
    while True:
        data = conn.recv(1024)
        received_data += data
        if not data:
            break

    try:
        newData = json.loads(received_data.decode())
        chunk = newData['requested_content']
        print(chunk)

        with open(chunk, 'rb') as f:
            data = f.read(1024)
            while data:
                conn.sendall(data)
                data = f.read(1024)

        with open("downloadlog.txt", "a") as downloadLog:
            currDate = datetime.datetime.now()
            stringToWrite = f"{address} downloaded {chunk}" + " at " + currDate.strftime("%Y-%m-%d %H:%M:%S")
            downloadLog.write(stringToWrite + "\n")

    except json.JSONDecodeError:
        print("Error: Invalid JSON data received.")

    except FileNotFoundError:
        print("Error: File not found.")

    conn.close()
