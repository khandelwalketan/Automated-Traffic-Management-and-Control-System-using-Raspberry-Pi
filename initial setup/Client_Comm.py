import socket

SERVER_IP = input("Enter server IP : ")
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP,PORT))
print("Connected to server")
while(True):
try:
command = client_socket.recv(1024).decode()

if command.lower()=="stop":
print("Server sent stop command. Closing connection.")
break

if command.lower()=="do":
response="Hi"
client_socket.send(response.encode())
print(f"Sent: {response}")


except ConnectionResetError:
print("Server connection lost.")
break

client_socket.close()
