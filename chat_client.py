import tkinter as tk
from tkinter import simpledialog, messagebox
import sys
import socket
import threading

PORT = 5501
FORMAT = 'utf-8'
CLEAR_RIGHT = "\033[K"  # clean to the right of the cursor
PREV_LINE = "\033[F"  # move cursor to the beginning of previous line

stop_threads = threading.Event()
chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    alias = input("Enter an alias: ")
    chat_socket.connect(('127.0.0.1', 5500))
except KeyboardInterrupt:
    print("\n[ERROR] KeyboardInterrupt raised")
    exit()
except Exception as e:
    print(f"\n[ERROR] {e}")
    exit()

def chat_receive():
    while not stop_threads.is_set():
        try:
            message = chat_socket.recv(1024).decode(FORMAT)
            if message == "alias?":
                chat_socket.send(alias.encode(FORMAT))
            else:
                print(message)
        except:
            print("[Disconnecting]")
            chat_socket.close()
            break #check later

def chat_send():
    while not stop_threads.is_set():
        try:
            message = f'{alias}: {input("")}'
            print(f"{PREV_LINE}{message}{CLEAR_RIGHT}")
            chat_socket.send(message.encode(FORMAT))
        except BaseException as e:
            print(f"[Disconnecting] {e}")
            chat_socket.close()
            break

recieve_thread = threading.Thread(target=chat_receive, daemon=True)
recieve_thread.start()

send_thread = threading.Thread(target=chat_send, daemon=True)
send_thread.start()

try:
    recieve_thread.join()
    send_thread.join()
except:
    print("Sending shutdown signal to threads")
    stop_threads.set()
    chat_socket.close()
    exit()