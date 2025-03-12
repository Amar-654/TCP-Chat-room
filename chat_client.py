import socket
import threading

PORT = 5501
FORMAT = 'utf-8'
CLEAR_RIGHT = "\033[K"  # clean to the right of the cursor
PREV_LINE = "\033[F"  # move cursor to the beginning of previous line

alias = input("Enter an alias: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

stop_threads = threading.Event()

try:
    client_socket.connect(('127.0.0.1', 5500))
except ConnectionRefusedError:
    print("[Connection Refused], Server might not be running")

def client_receive():
    while True:
        try:
            message = client_socket.recv(1024).decode(FORMAT)
            if message == "alias?":
                client_socket.send(alias.encode(FORMAT))
            else:
                print(message)
        except:
            print("[ERROR]")
            client_socket.close()
            break #check later

def client_send():
    while True:
        try:
            message = f'{alias}: {input("Enter text:")}'
            print(f"{PREV_LINE}{message}{CLEAR_RIGHT}")
            client_socket.send(message.encode(FORMAT))
        except:
            print("[Disconnecting]")
            client_socket.close()
            break

recieve_thread = threading.Thread(target=client_receive)
recieve_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()