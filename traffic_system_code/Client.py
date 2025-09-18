# client_loop_input.py
import socket
import struct
import os

def set_leds(value):
    if value == 0:
        print("[LED] GREEN ON, RED OFF")
    else:
        print("[LED] RED ON, GREEN OFF")

def send_image(image_path, host='localhost', port=12345):
    if not os.path.exists(image_path):
        print(f"[ERROR] File not found: {image_path}")
        return

    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        size = len(data)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.sendall(struct.pack('>I', size))
        sock.sendall(data)

        result = sock.recv(1)
        value = struct.unpack('B', result)[0]
        set_leds(value)
        sock.close()
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    ip=input("IP of server: ")
    while True:
        image_path = input("\nEnter path to image (or 'q' to quit): ").strip()
        if image_path.lower() == 'q':
            print("Exiting client.")
            break
        send_image(image_path,ip)
