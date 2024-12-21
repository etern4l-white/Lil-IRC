import curses
import traceback
import time



def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    bottom_pointer = rows-1
    queue = []
    try:
        stdscr.clear()
        stdscr.addstr(1, 0, 'hi')
        current_pointer = 1
        stdscr.refresh()
        # stdscr = curses.initscr()
        # curses.noecho()
        # curses.cbreak()
        # stdscr.keypad(True)
        while True:
            try:
                stdscr.addstr(rows-1, 0, f"Message: {current_pointer} >>> ")
                stdscr.refresh()
                message = []
                message_pointer = 0
                while True:
                    key = (stdscr.getch())
                    stdscr.addstr(10, 0, str(key))
                    if key == 10:
                        break
                    if key == 8 or key == 127 or key == 263: # ascii backspace lol
                        if (message_pointer<=0):
                            continue
                        message_pointer-=1
                        message.pop()
                    elif not (key >= 33 and key <= 126): # ascii printables
                        continue
                    else:
                        key = chr(key)
                        message_pointer+=1
                        message.append(key)
                    message_output = ''.join(message)
                    stdscr.addstr(rows-1, 0, " "*(cols-1))
                    stdscr.addstr(rows-1, 0, f"Message: {current_pointer} >>> " + message_output)
                    
                message = ''.join(message)
                # message = stdscr.getstr(rows-1, len(f"Message: {current_pointer} >>> "))
                # if len(queue >= rows-1):
                #     queue.pop(0)
                # queue.append(message)
                if len(message)>0:
                    stdscr.addstr(current_pointer, 0, message)
                    stdscr.addstr(rows-1, 0, " "*(cols-1))
                    stdscr.addstr(rows-1, 0, f"Message: {current_pointer} >>> ")
                    current_pointer+=1
                    stdscr.refresh()
            except KeyboardInterrupt as e:
                
                break
        # for i in range(10):
        #     stdscr.addstr(i+1, 0, f"{i*2}")
        #     curses.napms(500)
        #     stdscr.refresh()
    except Exception as e:
        stdscr.addstr(1, 0, str(e))
        # print(e)
        # print(traceback.format_exc())
        # curses.nocbreak()
        # stdscr.keypad(False)
        # curses.echo()
        # curses.endwin()
    stdscr.refresh()
    # stdscr.getkey()

curses.wrapper(main)