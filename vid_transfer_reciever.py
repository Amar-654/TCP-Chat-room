from socket import *
import pickle

FORMAT = 'utf-8'

#establish connection
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('10.30.200.190', 5500))

#recieved the size of the video beign sent
size = int(client_socket.recv(1024).decode(FORMAT))
video = "new.mp4"
client_socket.send("recieved".encode(FORMAT))
# print(size)

total_recieved = 0
pickled_data=b"" 
while(total_recieved<size):
    data = client_socket.recv(size)
    pickled_data+=data
    total_recieved += len(data)

# print(len(pickled_data.hex()))

unpickled_vid = pickle.loads(pickled_data)

with open(video, 'wb') as video_file:
    video_file.write(unpickled_vid)

print("File recieved")