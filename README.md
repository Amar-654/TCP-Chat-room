# Chat Application (Socket Programming)

## Overview
This is a simple chat application implemented using Python's socket and threading modules. It allows multiple clients to connect to a server and communicate in real-time. The server handles multiple clients simultaneously, and messages are broadcast to all connected clients except the sender.

## Screenshots
![image](https://github.com/user-attachments/assets/bf5bdfc2-3a45-4019-bf5e-c8cc1c865576)
![image](https://github.com/user-attachments/assets/e8a41fbd-0009-4ffb-a535-8dd40bad064e)
![image](https://github.com/user-attachments/assets/acaaecf6-181c-4497-8048-dd943a8d1004)

## Features
- Multiple client connections
- Real-time message broadcasting
- Graceful handling of client disconnections
- Server shutdown handling with client notifications

## Requirements
- Python 3.x

## Installation & Usage

### Running the Server
1. Open a terminal or command prompt.
2. Navigate to the directory containing `chat_server.py`.
3. Run the server using:
   ```bash
   python chat_server.py
   ```
4. The server will start listening for client connections on `127.0.0.1:5500`.

### Running the Client
1. Open a separate terminal or command prompt.
2. Navigate to the directory containing `chat_client.py`.
3. Run the client using:
   ```bash
   python chat_client.py
   ```
4. Enter a unique alias when prompted.
5. Start chatting!

## Server Code Explanation
- **`broadcast(message, client_socket)`**: Sends messages to all clients except the sender.
- **`handle_client(client_socket)`**: Handles communication with an individual client.
- **`receive()`**: Listens for incoming client connections and starts a new thread for each client.
- **Graceful Shutdown**: The server closes all client connections before shutting down.

## Client Code Explanation
- **`client_receive()`**: Listens for incoming messages from the server.
- **`client_send()`**: Captures user input and sends messages to the server.
- **Handles Disconnections**: Closes the socket properly when exiting.

## Error Handling
- **Server Timeout**: The server has a `settimeout(60.0)` to prevent indefinite blocking.
- **Client Connection Refused**: If the server is not running, an appropriate message is displayed.
- **Keyboard Interrupt**: Both server and client handle `CTRL+C` for graceful shutdown.

## Notes
- The server must be running before starting a client.
- Ensure all clients use unique aliases to avoid confusion.
- The application currently runs on localhost (`127.0.0.1`) but can be modified for network usage.

## Future Improvements
- Implement a GUI-based chat client.
- Add encryption for secure messaging.
- Enhance error handling and logging mechanisms.

---

Enjoy chatting!
