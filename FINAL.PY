import socket
import numpy as np
import tensorflow as tf
from PIL import Image
import os
import glob

# -----------------------------
# GTSRB Labels (43 classes)
# -----------------------------
labels = {
    0: "Speed limit (20km/h)", 1: "Speed limit (30km/h)", 2: "Speed limit (50km/h)",
    3: "Speed limit (60km/h)", 4: "Speed limit (70km/h)", 5: "Speed limit (80km/h)",
    6: "End of speed limit (80km/h)", 7: "Speed limit (100km/h)", 8: "Speed limit (120km/h)",
    9: "No passing", 10: "No passing for vehicles over 3.5t", 11: "Right-of-way at intersection",
    12: "Priority road", 13: "Yield", 14: "Stop", 15: "No vehicles",
    16: "Vehicles > 3.5t prohibited", 17: "No entry", 18: "General caution",
    19: "Dangerous curve left", 20: "Dangerous curve right", 21: "Double curve",
    22: "Bumpy road", 23: "Slippery road", 24: "Road narrows on the right",
    25: "Road work", 26: "Traffic signals", 27: "Pedestrians",
    28: "Children crossing", 29: "Bicycles crossing", 30: "Beware of ice/snow",
    31: "Wild animals crossing", 32: "End of all speed and passing limits",
    33: "Turn right ahead", 34: "Turn left ahead", 35: "Ahead only",
    36: "Go straight or right", 37: "Go straight or left", 38: "Keep right",
    39: "Keep left", 40: "Roundabout mandatory", 41: "End of no passing",
    42: "End of no passing by vehicles > 3.5t"
}

# -----------------------------
# Raspberry Pi connection details
# -----------------------------
PI_IP = "10.158.8.13"  # Pi IP
PI_PORT = 6001          # <-- must match your Pi bot server port


def send_command_to_pi(command):
    """Send command to Raspberry Pi"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((PI_IP, PI_PORT))
            s.sendall(command.encode())
        print(f"✅ Sent command to Pi: {command}")
    except Exception as e:
        print("❌ Error sending command:", e)


# -----------------------------
# Load TFLite Model
# -----------------------------
interpreter = tf.lite.Interpreter(
    model_path="traffic_sign_detection_cnn.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# -----------------------------
# Preprocess image
# -----------------------------


def preprocess_image(image_path):
    img = Image.open(image_path).resize((48, 48))
    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# -----------------------------
# Speed limit mapping
# -----------------------------
speed_map = {
    "Speed limit (20km/h)": "SPEED_20",
    "Speed limit (30km/h)": "SPEED_30",
    "Speed limit (50km/h)": "SPEED_50",
    "Speed limit (60km/h)": "SPEED_60",
    "Speed limit (70km/h)": "SPEED_70",
    "Speed limit (80km/h)": "SPEED_80",
    "Speed limit (100km/h)": "SPEED_100",
    "Speed limit (120km/h)": "SPEED_120"
}

# -----------------------------
# Pick the latest image
# -----------------------------
image_folder = r"C:\Users\swath\OneDrive\Desktop\images"
list_of_files = glob.glob(os.path.join(image_folder, "*.jpg"))
if not list_of_files:
    print("❌ No images found.")
    exit()

latest_file = max(list_of_files, key=os.path.getctime)
print(f"📷 Processing latest image: {latest_file}")

# -----------------------------
# Predict
# -----------------------------
img = preprocess_image(latest_file)
interpreter.set_tensor(input_details[0]['index'], img)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
predicted_class = int(np.argmax(output_data))
label = labels[predicted_class]
print(f"📊 Predicted class {predicted_class}: {label}")

# -----------------------------
# Decide and send commands
# -----------------------------
if label in speed_map:
    send_command_to_pi(speed_map[label])
elif label == "Stop":
    send_command_to_pi("STOP")
elif label in ["Ahead only", "Go straight or right", "Go straight or left"]:
    send_command_to_pi("FORWARD")
elif label in ["Turn left ahead", "Keep left"]:
    send_command_to_pi("LEFT")
elif label in ["Turn right ahead", "Keep right"]:
    send_command_to_pi("RIGHT")
else:
    print(f"⚠️ Ignored sign: {label}")
    send_command_to_pi(label)
