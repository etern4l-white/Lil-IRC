import curses
import traceback
import json
import threading
import socket

class Client:
    def __init__(self, client_id=None):
        self.client_id = client_id


def autistic_escaping(message_to_add, message):
    return "\\027181813141" + message_to_add[message_to_add.index(message['user']):message_to_add.index(message['user']) + len(message['user'])] + "\\027181823141" + message_to_add[message_to_add.index(message['user']) + len(message['user']):]

def format_messages_to_display(stdscr, messages_queue):
    rows, cols = stdscr.getmaxyx()
    temp_list = [f"{message['user']} {message['message']}" for message in messages_queue]
    displayed_messages = []
    for x, message in enumerate(temp_list):
        if len(message) >= cols:
            i = 0
            while i < -(-len(message)//cols):
                message_to_add = message[i*cols:(i+1)*cols]
                if i == 0:
                    message_to_add = autistic_escaping(message_to_add, messages_queue[x])
                displayed_messages.append(message_to_add)
                i+=1
        else:
            displayed_messages.append(autistic_escaping(message, messages_queue[x]))
    return displayed_messages
    
def display_dialog(stdscr, messages_queue):
    rows, cols = stdscr.getmaxyx()
    messages_queue = format_messages_to_display(stdscr, messages_queue)
    # displayed_queue = messages_queue[-(len(messages_queue)//(rows-1) + len(messages_queue)%(rows-1) + 1):]
    for i, message in enumerate(messages_queue[-(rows-1):]):
        if '\\027181813141' in message:
            user = message[message.index('\\027181813141') + len('\\027181813141'):message.index('\\027181823141')]
            
            if user == "Me":
                style = curses.color_pair(1) | curses.A_BOLD
            else:
                style = curses.color_pair(2)
        
            stdscr.addstr(i%rows, 0, ' '*cols)
            stdscr.addstr(i%rows, 0, user,  style)
            stdscr.addstr(i%rows, len(user)+ 1, message[(message.index('\\027181823141')+len('\\027181823141')):])
        else:
            stdscr.addstr(i%rows, 0, ' '*cols)
            stdscr.addstr(i%rows, 0, message)
        
    stdscr.refresh()

def add_message_to_dialog(stdscr, message, messages_queue):
    rows, cols = stdscr.getmaxyx()
    if len(message) == 0:
        return
    message_data = {
        'user':"Me",
        "message":message
    }
    messages_queue.append(message_data)
    if len(message)>0:
        stdscr.addstr(rows-1, 0, " "*(cols-1))
        stdscr.addstr(rows-1, 0, f"Message: >>> ")
        stdscr.refresh()
    display_dialog(stdscr, messages_queue)
    # pass

def display_error(stdscr, e):
    stdscr.addstr(0,0, traceback.format_exc())
    stdscr.refresh()

def get_message_input(stdscr, prompt = f"Message: >>> "):
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(rows-1, 0, " "*(cols-1)) # clearing the input field
    stdscr.addstr(rows-1, 0, prompt)
    stdscr.refresh()
    message_characters = []
    message_pointer = 0
    while True:
        key = (stdscr.getch())
        if key == 10: # \n (enter)
            break
        if key == 8 or key == 127 or key == 263: # ascii backspace 
            if (message_pointer<=0):
                continue
            message_pointer-=1
            message_characters.pop()
        elif not (key >= 32 and key <= 126): # ascii printables
            continue
        else:
            key = chr(key)
            message_pointer+=1
            message_characters.append(key)
        message_output = ''.join(message_characters)
        stdscr.addstr(rows-1, 0, " "*(cols-1))
        stdscr.addstr(rows-1, 0, prompt + message_output)
    return ''.join(message_characters)

def initiate_colors():
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)

def handle_recieving(stdscr, client_socket, messages_queue, client):
    while True:
        data = client_socket.recv((1024**2)//4) # 256 kb
        messages_queue.append(json.loads(data.decode()))
        # print(f"Server message: {data.decode()}")
        display_dialog(stdscr, messages_queue)

def handle_sending(stdscr, client_socket, messages_queue):
    message_data = {
        'user':'Me',
    }
    while True:
        message_data['message'] = get_message_input(stdscr)
        if len(message_data['message'].strip()) == 0:
            continue
        add_message_to_dialog(stdscr, message_data['message'], messages_queue)
        # messages_queue.append(message_data)
        display_dialog(stdscr, messages_queue)
        client_socket.sendall(json.dumps(message_data, ensure_ascii=False).encode())

def debug(something):
    with open("tt.log", 'a') as f:
        f.write(str(something) + '\n')

def main(stdscr):
    initiate_colors()
    messages_queue = []
    try:
        stdscr.clear()
        stdscr.refresh()
        
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as client_socket:
            host = get_message_input(stdscr, "Enter server's IP >>> ")
            port = get_message_input(stdscr, "Enter Port >>> ")
            client_id = get_message_input(stdscr, "Enter your ID >>> ")
            client = Client(client_id=client_id)
            # debug(host)
            client_socket.connect((host, int(port)))
            thread_receiving = threading.Thread(target=handle_recieving, args=((stdscr, client_socket,messages_queue)))
            thread_sending = threading.Thread(target=handle_sending, args=((stdscr, client_socket, messages_queue)))
            
            thread_sending.start()
            thread_receiving.start()
            thread_sending.join()        
            thread_receiving.join()

    except Exception as e:
        stdscr.addstr(1, 0, str(e))
    stdscr.refresh()

curses.wrapper(main)
