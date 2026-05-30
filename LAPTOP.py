import socket

# -----------------------------
# Raspberry Pi IP and port
# -----------------------------
RPI_IP = "10.158.8.13"  # Your Pi IP
RPI_PORT = 6001          # Must match Pi server

# -----------------------------
# Send command function
# -----------------------------


def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((RPI_IP, RPI_PORT))
            s.sendall(command.encode())
        print(f"✅ Command sent: {command}")
    except Exception as e:
        print(f"❌ Error sending command: {e}")


# -----------------------------
# Example usage
# -----------------------------
while True:
    cmd = input(
        "Enter command (FORWARD, BACKWARD, LEFT, RIGHT, STOP): ").strip().upper()
    if cmd in ["FORWARD", "BACKWARD", "LEFT", "RIGHT", "STOP"]:
        send_command(cmd)
    else:
        print("⚠️ Invalid command!")
