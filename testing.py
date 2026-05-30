import socket
from pathlib import Path
from datetime import datetime
from PIL import Image
import numpy as np
import tensorflow as tf

# ==== CONFIG ====
HOST = "0.0.0.0"   # Listen on all network interfaces
PORT = 5001
SAVE_DIR = Path(r"C:\Users\swath\OneDrive\Desktop\images")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# ==== CLASS LABELS ====
# Replace/add all your dataset classes here
CLASS_LABELS = {
    0: "LEFT TURN",
    1: "RIGHT TURN",
    2: "SPEED LIMIT 50",
    3: "NO ENTRY",
    4: "SOME SIGN 4",
    5: "SOME SIGN 5",
    6: "speed",
    7: "SOME SIGN 7",
    # Add the rest according to your dataset
}

# ==== LOAD TFLITE MODEL ====
interpreter = tf.lite.Interpreter(
    model_path="traffic_sign_detection_cnn.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Input details:", input_details)
print("Output details:", output_details)


def run_inference(image_path):
    # --- Preprocess image ---
    img = Image.open(image_path).convert("RGB")
    input_shape = input_details[0]['shape']  # e.g. [1, 64, 64, 3]
    img = img.resize((input_shape[2], input_shape[1]))  # width, height
    img = np.array(img, dtype=np.float32)

    # Normalize if needed
    if np.issubdtype(input_details[0]['dtype'], np.floating):
        img = img / 255.0

    # Add batch dimension
    img = np.expand_dims(img, axis=0)

    # --- Run inference ---
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    predicted_class = int(np.argmax(output_data))
    class_name = CLASS_LABELS.get(predicted_class, "Unknown")
    return predicted_class, class_name


# ==== SOCKET SERVER ====
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Listening on port {PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive image size
    size_data = conn.recv(16).decode().strip()
    size = int(size_data)

    # Receive image
    image_data = b""
    while len(image_data) < size:
        packet = conn.recv(4096)
        if not packet:
            break
        image_data += packet

    # Save image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = SAVE_DIR / f"received_image_{timestamp}.jpg"
    with open(filename, "wb") as f:
        f.write(image_data)

    print(f"Image saved at {filename}")

    # Run inference
    predicted_class, class_name = run_inference(filename)
    print(f"Predicted class: {predicted_class} ({class_name})")

    conn.close()
