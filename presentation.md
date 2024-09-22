---
marp: true
theme: default
class: lead
---

# Hand-Activated Navigation Display: HANDY

![bg right 45%](https://upload.wikimedia.org/wikipedia/commons/f/f5/PowerPoint_Presentation_Flat_Icon.svg)

---

## What is HANDY?

HANDY is an interactive presentation control system that uses hand gestures to navigate slides, making presentations more engaging and intuitive.

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

—


## Components

- **OrangePi**: Single-board computer running the pose detection model.
- **USB Camera**: Used to capture video of the presenter.

—
## Key Code Components

### 1. `main.py`

- **Main Function**:
  ```python
  def main():
      ...
      while True:
          ...
          # inference
          check_arms_above_head()
          # drawing
          ...
  ```

- **Gesture Detection**:
  ```python
  def check_arms_above_head():
      ...
      # simple check ```
---

## Code Snippet: `tools/receiver.py`

- **Purpose**: Receives commands and simulates key presses.
  
  ```python
  import socket
  from pynput import keyboard

  def handle_command(command):
      ...

  def start_server(ip, port):
      ...
  ```

- **Usage**:
  ```bash
  python3 tools/receiver.py 0.0.0.0 5565
  ```

---

## Running HANDY

1. **Start the Model**:
   ```bash
   python3 main.py --time True weights/human_pose.rknn 0 --stream-ip YOUR_IP --stream-port 5000 --command-port 5565
   ```

2. **Start the Receiver**:
   ```bash
   python3 tools/receiver.py 0.0.0.0 5565
   ```
---


## Running HANDY

1. **Start the HANDY Model**.
2. **Start the Command Receiver**.

---

## Voice Recognition Feature

**Voice Recognition**: We set up OrangePi to capture voice and interpret the same commands.

### Technology Stack
- **Vosk Library**
- **Vosk Model for English Detection**

### Usage

Enter the voice_recognition directory and run the command on OrangePI
```bash 
python3 vosk_model_run.py {Your Model Path} --stream-ip {IP of your PC} --stream-port 5565
```

On your PC run the script to receive commands from OrangePI
```bash
python3 receiver_voice.py 0.0.0.0 5565
```

For the script to execute you need to say "Next" or "Back" loudly, while running the model



---

## Known Issues

* **Slide Delays**: Too many slides can be skipped due to rapid hand movements. Introducing a sleep mode or timeout during inactivity can help control slide transitions.
* **False Positives**: Occasionally, gestures are misinterpreted, causing unintended actions. Improving camera positioning and ensuring both arms are visible can reduce this issue.

---

## Work Division
- **Max**: Found and integrated all models in the project. Enchanted their accuracy and performed the main program.
- **Bohdan**: Developed the Python script for receiving data and executing commands and created the voice recognition feature.


---

## Summary

HANDY integrates hand gesture recognition with presentation control to create a seamless, interactive experience. It enhances presentations by allowing the presenter to control slides through simple hand movements.

---

## Questions?

Feel free to ask!

![bg right](<Screenshot from 2024-08-29 22-16-06.png>)
![bg left](<Screenshot 2024-08-29 at 23.16.57.png>)



