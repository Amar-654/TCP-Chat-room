import socket
import threading

IP = '127.0.0.1'
PORT = 5500
FORMAT = 'utf-8'
SERVER_RUNNING = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
server.settimeout(3.0)

shutdown_event = threading.Event()

clients = []
aliases = []
client_threads = []

class clientThread(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
    
    def run(self):
        '''This function is run when the class object is created.'''

        while not shutdown_event.is_set():
            try:
                message = self.client_socket.recv(1024)
                if not message:  #why did i add this line again?
                    break
                broadcast(message, self.client_socket)
            except:
                break
        self.cleanup()
    
    def cleanup(self):
        ''''''
        if self.client_socket in clients:    
            index = clients.index(self.client_socket)
            alias = aliases[index]
            clients.remove(self.client_socket)
            aliases.remove(alias)
            broadcast(f"{alias} has left the chatroom".encode(FORMAT), self.client_socket)
        self.client_socket.close()



def broadcast(message, client_socket):
    '''This function is used to send the message to all the clients.'''

    for client in clients:
        if client!=client_socket:
            try:
                client.send(message)
            except:
                print(f"[ERROR]: Could not send message to {client} Removing from the clients list")
                clients.remove(client)
                client.close()




def recieve():
    '''This is the functoin that handles creating of threads for each client socket'''

    global SERVER_RUNNING
    while not shutdown_event.is_set():
        try:
            print(f"[SERVER is listening on {PORT}]")
            client_socket, address = server.accept()
            print(f"Connection established with {str(address)}")
            client_socket.send("alias?".encode(FORMAT))
            alias = client_socket.recv(1024).decode(FORMAT)
            aliases.append(alias)
            clients.append(client_socket)
            print(f"Alias of this client is {alias}")
            broadcast(f"{alias} has connected".encode(FORMAT), client_socket)
            client_socket.send("[You are now connected!]".encode(FORMAT))
            client_thread = clientThread(client_socket)
            client_thread.start()
            client_threads.append(client_thread)
        except socket.timeout:
            continue
        except OSError:
            break



def shutdown_server():
    '''This function is called during server shutdown to cleanup the lists of threads and clients and aliases.'''
    
    global SERVER_RUNNING
    SERVER_RUNNING = False

    shutdown_event.set()
    print("[SENDING CLOSING MESSAGE OVER ALL CLIENT SOCKETS]")
    for client in clients[:]:
        try:
            client.send("[SERVER IS SHUTTING DOWN]".encode(FORMAT))
            client.close()
        except:
            pass
    clients.clear()
    
    print("[WAITING FOR CLIENTS THREADS TO TERMINATE]")
    for thread in client_threads:
        thread.join()
    
    print("[CLOSING SERVER SOCKET]")
    server.close()


if __name__ == "__main__":
    try:
        recieve()
    except:
        shutdown_server()