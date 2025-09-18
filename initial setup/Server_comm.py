import socket
import threading
import time

# Server setup
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12345       # Port for communication

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)  # Listen for up to two clients

clients = {}  # Dictionary to store connected clients

def handle_client(conn, client_id):
    """Handles communication with a connected client."""
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break  # If client disconnects, exit loop
           
            print(f"Client {client_id}: {message}")
       
        except ConnectionResetError:
            print(f"Client {client_id} disconnected unexpectedly.")
            break

    conn.close()
    del clients[client_id]  # Remove client from dictionary
    print(f"Client {client_id} connection closed.")

# Accept connections for two client

for i in range(1, 3):
    conn, addr = server_socket.accept()
    clients[i] = conn  # Store client connection
    print(f"Client {i} connected from {addr}")
    threading.Thread(target=handle_client, args=(conn, i), daemon=True).start()

# Main thread to send messages
while True:
    time.sleep(0.1)
    user_input = input("Enter command (Do 1 / Do 2 / Stop): ").strip().lower()

    if user_input == "stop":
        print("Stopping all clients...")
        for conn in clients.values():
            conn.send("Stop".encode())  # Notify clients to stop
            conn.close()
        break  # Exit main loop

    elif user_input in ["do 1", "do 2"]:
        target_client = int(user_input.split()[1])  # Extract client ID
        if target_client in clients:
            clients[target_client].send("Do".encode())  # Send "Do" to respective client
        else:
            print(f"Client {target_client} is not connected.")
   
    else:
        print("Invalid command. Use 'Do 1', 'Do 2', or 'Stop'.")

server_socket.close()
