import socket
import json


with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as client_socket:
    host = input("Enter server IP >>> ")
    client_socket.connect((host,3141))
    while True:
        data = {
            'user':'1',
        }
        data['payload'] = input("Enter message >>> ")
        client_socket.sendall(json.dumps(data, ensure_ascii=False).encode())
        response = client_socket.recv(1048576)
        print(response.decode())