import socket
import os
import time
from picamera2 import Picamera2

# ==== CONFIGURATION ====
PC_IP = "10.158.8.80"  # Replace with your PC's IP
PORT = 5001
IMAGE_PATH = "image.jpg"

# ==== STEP 1: CAPTURE IMAGE ====
print("Initializing camera...")
picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

picam2.start()
time.sleep(2)  # Allow camera to adjust
picam2.capture_file(IMAGE_PATH)
picam2.stop()

print(f"Image captured and saved as {IMAGE_PATH}")

# ==== STEP 2: SEND IMAGE TO PC ====
print(f"Connecting to PC at {PC_IP}:{PORT}...")

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((PC_IP, PORT))

# Get image size
size = os.path.getsize(IMAGE_PATH)
client_socket.sendall(str(size).encode().ljust(16)
                      )  # Send file size (16 bytes)

# Send image data
with open(IMAGE_PATH, "rb") as f:
    data = f.read()
    client_socket.sendall(data)

print("Image sent successfully.")

client_socket.close()
