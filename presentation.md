---
marp: true
theme: default
class: lead
---

# Hand-Activated Navigation Display: HANDY

![bg right 45%](https://upload.wikimedia.org/wikipedia/commons/f/f5/PowerPoint_Presentation_Flat_Icon.svg)

---

## What is HANDY?

HANDY is an interactive presentation control system that uses hand gestures to navigate slides.

- **Objective**: Make presentations more interactive and engaging.
- **Technology**: Utilizes OrangePi and a USB camera.
- **Based on**: [MMPose by OpenMMLab](https://github.com/open-mmlab/mmpose) and [this](https://github.com/Applied-Deep-Learning-Lab/Keypoints_HRNet_RK3588) repo-tutorial

---

## How It Works

1. **Capture Video**: USB camera captures the presenter’s gestures.
2. **Pose Detection**: Uses the `RKNN` model to detect hand positions.
3. **Gesture Recognition**: Determines gestures and sends commands.
4. **Navigation**: Commands are sent to the presentation software to navigate slides.

---

## Components

### 1. OrangePi
- Single-board computer running the detection model.

### 2. USB Camera
- Captures real-time video of the presenter.

![bg right 90%](https://habrastorage.org/getpro/habr/post_images/455/4bb/6cd/4554bb6cdb0caf3222d12676f7a33581.jpg)
![bg right 35%](https://e.428.ua/img/319264/3000/2000/web_kamera_logitech_c930e_hd_960-000972~1600~1600.jpg)

---

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

## Issues with HANDY

1. **Slide Delays**: Introducing a sleep mode during inactivity can help reduce passing to many slides at one time

2. **False Positives**: Incorrect command triggers occur due to false positives. Ensuring both arms are detected by the camera can improve accuracy and prevent unintended actions.


---

## Summary

- HANDY integrates hand gesture recognition with presentation control.
- Utilizes OrangePi, a USB camera, and custom Python scripts for gesture detection and command execution.
- Enhances the presentation experience through interactive control.
---

## Questions?

Feel free to ask!


![bg right](<Screenshot from 2024-08-29 22-16-06.png>)
![bg left](<Screenshot 2024-08-29 at 23.16.57.png>)

