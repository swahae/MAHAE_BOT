import socket
import os
from pathlib import Path
from datetime import datetime

# Listening IP and port
HOST = "0.0.0.0"
PORT = 5001

# Folder to save received images
SAVE_DIR = Path(r"C:\Users\swath\OneDrive\Desktop\images")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Listening for incoming connections on port {PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive image size
    size_data = conn.recv(16).decode().strip()
    size = int(size_data)
    print(f"Receiving image of size: {size} bytes")

    # Receive image data
    image_data = b""
    while len(image_data) < size:
        packet = conn.recv(4096)
        if not packet:
            break
        image_data += packet

    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = SAVE_DIR / f"received_image_{timestamp}.jpg"

    with open(filename, "wb") as f:
        f.write(image_data)

    print(f"Image saved at {filename}")

    conn.close()
