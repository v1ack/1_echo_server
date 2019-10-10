import os
import socket
import sys
from threading import Thread
from common import SocketMethods

sock = socket.socket()

address = input('Input address: ')
if not address:
    address = 'localhost'
port = input('Input port: ')
if not port:
    port = 9000
else:
    port = int(port)

sock.connect((address, port))
os.system('')

try:
    with open('token', 'r') as file:
        token = file.read()
except FileNotFoundError:
    token = '--no token--'
SocketMethods.send_text(sock, token)

connection_alive = True


def custom_input() -> str:
    result = ''
    if os.name == 'nt':
        import msvcrt
        while True:
            entered = msvcrt.getwch()
            if entered == '\r':
                break
            msvcrt.putwch(entered)
            result += entered
    else:
        import curses
        console = curses.initscr()
        while True:
            entered = console.get_wch()
            if entered == '\n':
                break
            result += entered
    print('\r', flush=False, end='')
    # print('>', result)
    return result


def receive_messages():
    global connection_alive
    while True:
        received = SocketMethods.receive_text(sock)
        if received[:2] == '//':
            if received == '//close':
                sock.close()
                connection_alive = False
                break
            if received == '//token':
                with open('token', 'w') as file:
                    file.write(SocketMethods.receive_text(sock))
                continue
        print(received)
    sys.exit()


Thread(target=receive_messages, daemon=True).start()

while True:
    message = custom_input()
    if connection_alive:
        SocketMethods.send_text(sock, message)
    else:
        break
