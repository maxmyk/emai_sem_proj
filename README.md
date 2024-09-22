# HANDY: Hand-Activated Navigation Display

**HANDY** is an interactive presentation control system that uses hand gestures to navigate slides, making presentations more engaging and intuitive.

## Overview

HANDY utilizes an **OrangePi** single-board computer and a **USB camera** to capture real-time video of the presenter’s gestures. It processes these gestures using a **pose detection model** and sends navigation commands to the presentation software.

### Objective
The goal of HANDY is to enhance presentations by allowing the presenter to control the slides through hand gestures, reducing the need for physical interaction with a keyboard or remote.

### Technology Stack
- **OrangePi**: Runs the detection model.
- **USB Camera**: Captures real-time video for gesture detection.
- **MMPose**: A pre-trained model from OpenMMLab used for pose detection.
  - Repository: [MMPose by OpenMMLab](https://github.com/open-mmlab/mmpose)
  - Tutorial: [Keypoints HRNet for RK3588](https://github.com/Applied-Deep-Learning-Lab/Keypoints_HRNet_RK3588)

---

## How It Works

1. **Capture Video**: The USB camera captures the presenter's gestures in real-time.
2. **Pose Detection**: The captured video is processed by a **RKNN model** to detect hand positions.
3. **Gesture Recognition**: The system interprets gestures and sends corresponding commands.
4. **Navigation**: Commands are sent to the presentation software, enabling slide navigation based on detected gestures.

---

## Components

- **OrangePi**: Single-board computer running the pose detection model.
- **USB Camera**: Used to capture video of the presenter.

---

## Code Structure

1. **`main.py`**: This is the core of the system. It handles the video capture, gesture detection, and command processing.
   - **Functionality**:
     - Continuously captures video.
     - Runs inference to detect hand positions.
     - Draws detected gestures and sends commands based on arm positions.

2. **`tools/receiver.py`**: Receives commands over UDP and simulates key presses for slide navigation.
   - **Functionality**:
     - Listens for incoming commands.
     - Uses `pynput` to simulate keyboard actions based on received commands.

---

## Usage

### 1. Start the HANDY Model:
```bash
python3 main.py --time True weights/human_pose.rknn 0 --stream-ip YOUR_IP --stream-port 5000 --command-port 5565
```
### 2. Start the Command Receiver:
```python
python3 tools/receiver.py 0.0.0.0 5565
```
## Known Issues

* **Slide Delays:** Too many slides can be skipped due to rapid hand movements. Introducing a sleep mode or timeout during inactivity can help control slide transitions.
* **False Positives:** Occasionally, gestures are misinterpreted, causing unintended actions. Improving camera positioning and ensuring both arms are visible can reduce this issue.

## Additional features
**Voice recognition**
- We set up Orangepi to capture voice and interpritate the same commands
### Technology Stack
- Vosk library 
- Vosk model for English detecture

### Usage

Enter voice_recognition directory and run command on OrangePI
```bash 
python3 vosk_model_run.py {Your Model Path} --stream-ip {IP of your PC} --stream-port 5565
```

At your PC run script to receive commands from OrangePI
```bash
python3 receiver_voice.py 0.0.0.0 5565
```

For script to execute you need say "Next" or "Back" laudly, while running model

## Summary

HANDY integrates hand gesture recognition with presentation control to create a seamless, interactive experience. It enhances presentations by allowing the presenter to control slides through simple hand movements.
