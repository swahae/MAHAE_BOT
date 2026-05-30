import socket
import RPi.GPIO as GPIO

# Motor driver pins
ENA = 12   # Enable pin for Motor A (PWM)
ENB = 13   # Enable pin for Motor B (PWM)
IN1 = 23   # Motor A input 1
IN2 = 24   # Motor A input 2
IN3 = 27   # Motor B input 1
IN4 = 17   # Motor B input 2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup motor pins
for pin in [IN1, IN2, IN3, IN4, ENA, ENB]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Setup PWM for enable pins
pwmA = GPIO.PWM(ENA, 1000)  # 1 kHz
pwmB = GPIO.PWM(ENB, 1000)
pwmA.start(10)
pwmB.start(10)


def set_speed(speed):
    """Set motor speed (0-100)"""
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)


def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(0)


def backward(speed=10):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(speed)


def forward(speed=10):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(speed)


def left(speed=10):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(speed)


def right(speed=10):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(speed)


# -----------------------------
# Socket server
# -----------------------------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 6001))
server.listen(1)

print("✅ Bot Control Server started, waiting for commands...")

# Speed mapping (custom PWM values for each speed limit)
speed_map = {
    "SPEED_20": 20,
    "SPEED_30": 22,
    "SPEED_50": 25,
    "SPEED_60": 28,
    "SPEED_70": 30,
    "SPEED_80": 35,
    "SPEED_100": 40,
    "SPEED_120": 45
}

try:
    while True:
        client, addr = server.accept()
        data = client.recv(1024).decode().strip()
        print(f"📩 Received: {data}")

        # Movement commands
        if data == "STOP":
            stop()
        elif data == "FORWARD":
            forward(10)  # default forward speed
        elif data == "BACKWARD":
            backward(10)
        elif data == "LEFT":
            left(10)
        elif data == "RIGHT":
            right(10)
        # Speed limit commands
        elif data in speed_map:
            print(f"⚡ Setting speed to {speed_map[data]} due to {data}")
            set_speed(speed_map[data])
      # Automatically move forward after setting speed
            forward(speed_map[data])

        else:
            print(f"⚠️ Unknown command: {data}")

        client.close()

except KeyboardInterrupt:
    print("\n🛑 Exiting and cleaning up GPIO...")
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
