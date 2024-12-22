import socket
import random
import json
import traceback


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == "__main__":
    try:
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # server_socket
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
                conn.send(json.dumps({'user':"server", "message":f"Received: {data.decode()}, random number: {random.randint(1, 100000)}"}).encode())
    except Exception as e:
        #server_socket.shutdown()
        server_socket.close()
        with open("server_log.log", 'a') as f:
            f.write(traceback.format_exc())
