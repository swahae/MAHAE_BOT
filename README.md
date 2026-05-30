# MAHAE_BOT

An autonomous traffic sign detection and robotic control system built using Raspberry Pi, computer vision, and TensorFlow Lite. The bot captures road images, detects traffic signs, interprets their meaning, and controls the robot's movement accordingly.

---

## Project Overview

MAHAE_BOT is designed to simulate an intelligent autonomous vehicle that can recognize traffic signs and react appropriately. The system uses image processing and a trained TensorFlow Lite model to identify traffic signs and generate movement commands for the robot.

### Workflow

```text
Camera
   │
   ▼
capture_send.py
   │
   ▼
receive.py
   │
   ▼
FINAL.PY
(Traffic Sign Detection)
   │
   ▼
after_detection_sign.py
(Command Processing)
   │
   ▼
mahae_control_receive.py
(Motor Control)
   │
   ▼
Robot Movement
```

---

## Features

- Real-time image capture
- Wireless image transmission
- Traffic sign recognition using TensorFlow Lite
- Automated decision making
- Robot movement control
- Modular architecture for easy maintenance and upgrades

---

## Project Structure

```text
MAHAE_BOT/
│
├── FINAL.PY
├── capture_send.py
├── receive.py
├── after_detection_sign.py
├── mahae_control_receive.py
├── testing.py
├── traffic_sign_detection_cnn.tflite
└── README.md
```

---

## File Descriptions

### 1. FINAL.PY

**Purpose:** Main processing and traffic sign detection module.

#### Responsibilities

- Loads the TensorFlow Lite model
- Preprocesses captured images
- Performs traffic sign classification
- Generates movement decisions
- Sends commands to the robot controller

#### Example Actions

| Detected Sign | Command |
|--------------|----------|
| Stop | STOP |
| Turn Left | LEFT |
| Turn Right | RIGHT |
| Speed Limit | SPEED CONTROL |
| No Entry | STOP |

---

### 2. capture_send.py

**Purpose:** Image acquisition and transmission module.

#### Responsibilities

- Captures images from the camera
- Converts images into transferable format
- Sends images to the processing system
- Maintains communication with the receiver

#### Input

- Camera feed

#### Output

- Captured image transmitted over network

---

### 3. receive.py

**Purpose:** Image receiving module.

#### Responsibilities

- Receives images from the sender
- Stores incoming images
- Makes images available for processing

#### Input

- Image packets from capture_send.py

#### Output

- Saved image files for detection

---

### 4. after_detection_sign.py

**Purpose:** Post-detection command processing module.

#### Responsibilities

- Interprets detected traffic sign results
- Converts classifications into movement commands
- Filters invalid detections
- Prepares commands for robot execution

#### Example

```text
STOP Sign
    ↓
Generate STOP Command
    ↓
Send to Robot Controller
```

---

### 5. mahae_control_receive.py

**Purpose:** Robot control module.

#### Responsibilities

- Receives movement commands
- Controls motor operations
- Executes navigation instructions
- Stops, turns, or moves the robot

#### Example Commands

```text
FORWARD
BACKWARD
LEFT
RIGHT
STOP
```

---

### 6. testing.py

**Purpose:** Testing and debugging module.

#### Responsibilities

- Verifies communication between modules
- Tests image processing pipeline
- Evaluates detection accuracy
- Supports debugging during development

#### Note

This file is intended for development and testing purposes only and is not required during normal deployment.

---

## Requirements

### Hardware

- Raspberry Pi
- Camera Module / USB Camera
- Motor Driver
- DC Motors
- Power Supply
- Wireless Network Connection

### Software

- Python 3.x
- TensorFlow Lite
- NumPy
- OpenCV
- Pillow

---

## Installation

Clone the repository:

```bash
git clone https://github.com/swahae/MAHAE_BOT.git
cd MAHAE_BOT
```

Install dependencies:

```bash
pip install tensorflow
pip install numpy
pip install pillow
pip install opencv-python
```

---

## Running the Project

### Step 1: Start Image Capture

```bash
python capture_send.py
```

### Step 2: Start Receiver

```bash
python receive.py
```

### Step 3: Run Traffic Sign Detection

```bash
python FINAL.PY
```

### Step 4: Start Robot Controller

```bash
python mahae_control_receive.py
```

---

## System Architecture

```text
+-------------------+
| Camera Module     |
+---------+---------+
          |
          v
+-------------------+
| capture_send.py   |
+---------+---------+
          |
          v
+-------------------+
| receive.py        |
+---------+---------+
          |
          v
+-------------------+
| FINAL.PY          |
| Traffic Detection |
+---------+---------+
          |
          v
+-------------------+
| after_detection   |
+---------+---------+
          |
          v
+-------------------+
| Robot Controller  |
| mahae_control_    |
| receive.py        |
+---------+---------+
          |
          v
+-------------------+
| Motors & Movement |
+-------------------+
```

---

## Future Enhancements

- Lane detection
- Obstacle avoidance
- Real-time video processing
- GPS-based navigation
- Cloud-based monitoring
- Improved traffic sign dataset

---

## Authors

Developed as part of the MAHAE_BOT autonomous traffic sign detection and robotic navigation project.

---
