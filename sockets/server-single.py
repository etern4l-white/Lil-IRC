import socket

server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, )
server_socket.bind(("0.0.0.0",3141))
server_socket.listen()


conn, addr = server_socket.accept()
with conn:
    print(f"Accepted connection from {addr}")
    while True:
        data = conn.recv(1024)
        print(data)
        if not data:
            # print(type(data))
            break
        # conn.send(f"Received data {data}".encode())