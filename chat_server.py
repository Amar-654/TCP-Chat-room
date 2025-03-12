import socket
import threading

IP = '127.0.0.1'
PORT = 5500
FORMAT = 'utf-8'
SERVER_RUNNING = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
server.settimeout(60.0)

clients = []
aliases = []

#function to broadcast to the chat room
def broadcast(message, client_socket):
    for client in clients:
        if client!=client_socket:
            client.send(message)
    
#function to handle each client
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            alias = aliases[index]
            broadcast(f"{alias} has left the chatroom".encode(FORMAT), client_socket)
            aliases.remove(alias)
            break
    client_socket.close()

def recieve():
    global SERVER_RUNNING
    while SERVER_RUNNING:
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
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
        except socket.timeout:
            continue
        except KeyboardInterrupt:
            print("[SERVER IS SHUTTING DOWN]")
            break
    print("[Closing all client connections]")
    for client in clients:
        client.send("[SERVER is shutting down]".encode(FORMAT))
        client.close()
    server.close()

if __name__ == "__main__":
    try:
        recieve()
    except:
            print("[SERVER IS SHUTTING DOWN]")
            server.close()