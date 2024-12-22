import curses
import traceback

def display_dialog(stdscr, messages_queue):
    rows, cols = stdscr.getmaxyx()
    # displayed_queue = messages_queue[-(len(messages_queue)//(rows-1) + len(messages_queue)%(rows-1) + 1):]
    for i, message in enumerate(messages_queue[-(rows-1):]): 
        stdscr.addstr(10, 0, str(i))
        stdscr.addstr(i%rows, 0, message)

def add_message_to_dialog(stdscr, ch_list, messages_queue):
    rows, cols = stdscr.getmaxyx()
    message = ''.join(ch_list)
    if len(message) == 0:
        return
    messages_queue.append(message)
    if len(message)>0:
        stdscr.addstr(rows-1, 0, " "*(cols-1))
        stdscr.addstr(rows-1, 0, f"Message: >>> ")
        stdscr.refresh()
    display_dialog(stdscr, messages_queue)
    # pass

def display_error(stdscr, e):
    stdscr.addstr(0,0, traceback.format_exc())
    stdscr.refresh()

def get_message_input(stdscr):
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(rows-1, 0, f"Message: >>> ")
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
        elif not (key >= 33 and key <= 126): # ascii printables
            continue
        else:
            key = chr(key)
            message_pointer+=1
            message_characters.append(key)
        message_output = ''.join(message_characters)
        stdscr.addstr(rows-1, 0, " "*(cols-1))
        stdscr.addstr(rows-1, 0, f"Message: >>> " + message_output)
    return message_characters

def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    messages_queue = []
    try:
        stdscr.clear()
        stdscr.refresh()
        while True:
            try:
                message_characters = get_message_input(stdscr)
                add_message_to_dialog(stdscr, message_characters, messages_queue)
            except KeyboardInterrupt as e:
                break
            except Exception as e:
                display_error(stdscr, e)
                stdscr.napms(5000)
                with open("Error.log", "w") as f:
                    f.write(traceback.format_exc())
                break
            

    except Exception as e:
        stdscr.addstr(1, 0, str(e))
    stdscr.refresh()

curses.wrapper(main)