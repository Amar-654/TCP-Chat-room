from socket import *
import pickle
import sys

IP = '10.30.200.190'
PORT = 5500
FORMAT = 'utf-8'

server = socket(AF_INET, SOCK_STREAM)
server.bind((IP, PORT))
server.listen()
server.settimeout(30.0)

video_path = 'test.pdf'

with open(video_path, 'rb') as video_file:
        video_bytes = video_file.read()

#creating pickled data and getting its sisze
pickled_video_data = pickle.dumps(video_bytes)
data_size_str = str(sys.getsizeof(pickled_video_data)).encode(FORMAT)

print(data_size_str.hex())
client_socket,address = server.accept()
print("[Client connected]")

# sending data size
client_socket.send(data_size_str)

#recieving the data size recieved message
client_socket.recv(1024).decode(FORMAT)

# client_socket.sendall(pickled_video_data)

# print(len(pickled_video_data.hex()))

total_sent = 0
while(total_sent<=int(data_size_str)):
        sent = client_socket.send(pickled_video_data)
        total_sent += int(sent)
print(pickled_video_data)
 
# client_socket.recv(1024).decode(FORMAT)  
client_socket.close()