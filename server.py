import socket
import random
import json
import traceback

with open("auth_db.json", 'r') as f:
    AUTH_DB = json.loads(f.read()) # Temp solution for now


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

class Client:
    def __init__(self, client_id=None):
        self.client_id = client_id
        self.username = None
        self.password = None

    def client_creds(self):
        return f"{self.username}, {self.password}"

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.loads(f.read)()
    except Exception as e:
        print("Error occured while reading file", filename)
        print(traceback.format_exc())
        return []

def write_json(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(json.dumps(content, indent=4, ensure_ascii=False))
    except Exception as e:
        print("Error occured when writing to file", filename)
        print(traceback.format_exc())

def send_message(connection, message):
    conn.send(json.dumps({'user':"server", "message":message}).encode())
    
def register_user(conn):
    print("registering user")
    while True:
        send_message(conn, "Enter username")
        data = conn.recv(1024).decode()
        username = json.loads(data)['message']
        if username in AUTH_DB['users']:
            send_message(conn, "Username already exists")
        else:
            send_message(conn, "Enter password")
            data = conn.recv(1024).decode()
            password = json.loads(data)['message']
            AUTH_DB['users'][username] = password
            write_json('auth_db.json', AUTH_DB)
            send_message(conn, "Registration successful")
            break

    client = Client()
    client.username = username
    client.password = password
    return client

def auth(conn):
    print("Authenticating user")
    send_message(conn, "Enter username")
    data = conn.recv(1024).decode()
    username = json.loads(data)['message']

    send_message(conn, "Enter password")
    data = conn.recv(1024).decode()
    password = json.loads(data)['message']

    client = Client()
    if username in AUTH_DB['users'] and password == AUTH_DB['users'][username]:
        client.username = username
        client.password = password
        send_message(conn, "Auth Success")
    else:
        send_message(conn, "Invalid creds")
    return client

if __name__ == "__main__":
    while True:
        try:
            server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            # server_socket
            port = random.randint(2000, 65000)
            server_socket.bind(("0.0.0.0", port))
            server_socket.listen()
            print("Listenning on port",port) 
            conn, addr = server_socket.accept()
            with conn:
                print(f"Accepted connection from {addr}")
                client = Client()

                while True:
                    data = conn.recv(1024)
                    print(data)
                    message = json.loads(data.decode())
                    if message['message'] == '/auth':
                        client = auth(conn)
                    elif message['message'] == '/register':
                        client = register_user(conn)
                    if not data:
                        # print(type(data))
                        break
                    conn.send(json.dumps({'user':"server", "message":f"Received: {data.decode()}, from: {client.client_creds()}.. random number: {random.randint(1, 100000)}"}).encode())
        except KeyboardInterrupt as e:
            print("Terminating server...")
            server_socket.close()
            break
        except Exception as e:
            print("Error occured")
            print(traceback.format_exc())
            #server_socket.shutdown()
            with open("server_log.log", 'a') as f:
                f.write(traceback.format_exc())
    
    print("terminated server")

