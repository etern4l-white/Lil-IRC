import curses
import traceback
import json
import threading
import socket


def display_dialog(stdscr, messages_queue):
    rows, cols = stdscr.getmaxyx()
    # displayed_queue = messages_queue[-(len(messages_queue)//(rows-1) + len(messages_queue)%(rows-1) + 1):]
    for i, message_data in enumerate(messages_queue[-(rows-1):]):
        if message_data['user'] == "Me":
            style = curses.color_pair(1) | curses.A_BOLD
        else:
            style = curses.color_pair(2)
        stdscr.addstr(i%rows, 0, ' '*cols)
        stdscr.addstr(i%rows, 0, f"{message_data['user']}",  style)
        stdscr.addstr(i%rows, len(f"{message_data['user']}") + 1, f"{message_data['message']}")
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

def handle_recieving(stdscr, client_socket, messages_queue):
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
            # debug(host)
            client_socket.connect((host, int(port)))
            thread_receiving = threading.Thread(target=handle_recieving, args=((stdscr, client_socket,messages_queue)))
            thread_sending = threading.Thread(target=handle_sending, args=((stdscr, client_socket, messages_queue)))
            
            thread_sending.start()
            thread_receiving.start()
            thread_sending.join()        
            thread_receiving.join()
        # while True:
        #     try:
        #         message_characters = get_message_input(stdscr)
        #         add_message_to_dialog(stdscr, message_characters, messages_queue)
        #     except KeyboardInterrupt as e:
        #         break
        #     except Exception as e:
        #         display_error(stdscr, e)
        #         # stdscr.napms(10000)
        #         debug(traceback.format_exc())
        #         with open("Error.log", "w") as f:
        #             f.write(traceback.format_exc())
        #         break

    except Exception as e:
        stdscr.addstr(1, 0, str(e))
    stdscr.refresh()

curses.wrapper(main)
