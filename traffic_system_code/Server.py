# server_compare_loop.py
import socket
import struct
import threading
import os
import uuid
from vehicle_count import count_vehicles_in_image

HOST = '0.0.0.0'
PORT = 12345

lock = threading.Lock()
clients = []
images = []

def receive_image(conn):
    packed_size = conn.recv(4)
    size = struct.unpack('>I', packed_size)[0]
    data = b''
    while len(data) < size:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet

    image_path = f'temp_{uuid.uuid4().hex}.jpg'
    with open(image_path, 'wb') as f:
        f.write(data)
    return image_path

def process_and_respond():
    print("\n[SERVER] Received images from both clients. Processing...")

    count1_dict = count_vehicles_in_image(images[0])
    count2_dict = count_vehicles_in_image(images[1])

    count1 = sum(count1_dict.values())
    count2 = sum(count2_dict.values())

    print(f"[SERVER] Client 1: {clients[0][1]}, Vehicle Count = {count1}, Breakdown = {count1_dict}")
    print(f"[SERVER] Client 2: {clients[1][1]}, Vehicle Count = {count2}, Breakdown = {count2_dict}")

    if count1 < count2:
        print("[SERVER] Client 2 has more traffic.")
        result1, result2 = 0, 1
    else:
        print("[SERVER] Client 1 has more traffic or equal.")
        result1, result2 = 1, 0

    for i, result in enumerate([result1, result2]):
        conn, addr = clients[i]
        print(f"[SERVER] Sending result {result} to Client {i+1} ({addr})")
        conn.sendall(struct.pack('B', result))
        conn.close()
        os.remove(images[i])

    clients.clear()
    images.clear()
    print("[SERVER] Ready for next pair of clients.\n")

def handle_client(conn, addr):
    image_path = receive_image(conn)
    with lock:
        clients.append((conn, addr))
        images.append(image_path)
        if len(clients) == 2:
            process_and_respond()

def start_server():
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == '__main__':
    start_server()
