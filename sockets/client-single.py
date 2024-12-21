import socket
import json
import threading



def handle_recieving(client_socket, is_busy):
    while True:
        data = client_socket.recv(1024)
        is_busy[0] = True
        print(f"Server message: {data.decode()}")
        is_busy[0] = False
        
def handle_sending(client_socket, is_busy):
    data = {
        'user':'1',
    }
    while True:
        if not is_busy[0]:
            data['payload'] = input("\033[32mYour message:\033[0m ")
            client_socket.sendall(json.dumps(data, ensure_ascii=False).encode())
        else:
            continue

if __name__ == "__main__":
    
    is_busy = [False]
    
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as client_socket:
        host = input("Enter server IP >>> ")
        client_socket.connect((host, 3141))
        thread_receiving = threading.Thread(target=handle_recieving, args=((client_socket,is_busy)))
        thread_sending = threading.Thread(target=handle_sending, args=((client_socket,is_busy)))
        
        thread_sending.start()
        thread_receiving.start()
        thread_sending.join()        
        thread_receiving.join()

        