import os
import socket
from rknnlite.api import RKNNLite
import argparse
import cv2
import time
import numpy as np

# gst-launch-1.0 udpsrc multicast-group=192.168.88.2 port=5000 ! application/x-rtp, payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink
#For MacOS
#gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.2.1 port=5000


# python3 main.py --time True weights/human_pose.rknn 0 --stream-ip 192.168.88.2 --stream-port 5000 --command-port 5565

#for MacOS
#python3 main.py --time True weights/human_pose.rknn 0 --stream-ip 192.168.2.1 --stream-port 5000 --command-port 5565
# python3 tools/receiver.py 0.0.0.0 5565

def parse_args():
    parser = argparse.ArgumentParser(description='Run a pose model on video and stream')
    parser.add_argument('model', help='weights file path')
    parser.add_argument('video', help='video file path or camera index')
    parser.add_argument('--size', help='the size of input image', type=int, default=512)
    parser.add_argument('--num-clusses', help='the number of classes', type=int, default=17)
    parser.add_argument('--stream-ip', help='IP address of the streaming destination', required=True)
    parser.add_argument('--stream-port', help='Port of the streaming destination', type=int, default=5000)
    parser.add_argument('--command-port', help='Port of the command destination', type=int, default=5565)
    parser.add_argument('--time', help='show inference & postprocess time', default=False)
    args = parser.parse_args()
    return args

def send_command(ip, port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(command.encode(), (ip, port))
        print(f"Sent command: '{command}' to {ip}:{port}")
    finally:
        sock.close()

def transform_preds(coords, width, model_size):
    scale_x = model_size / width
    scale_y = model_size / width
    target_coords = np.ones_like(coords)
    target_coords[:, :, 0] = coords[:, :, 0] * scale_x
    target_coords[:, :, 1] = coords[:, :, 1] * scale_y
    return target_coords

def _get_max_preds(heatmaps):
    assert isinstance(heatmaps, np.ndarray), 'heatmaps should be numpy.ndarray'
    assert heatmaps.ndim == 4, 'batch images should be 4-ndim'
    
    N, K, H, W = heatmaps.shape
    heatmaps_reshaped = heatmaps.reshape((N, K, -1)) 
    idx = np.argmax(heatmaps_reshaped, 2).reshape((N, K, 1)) 
    maxvals = np.amax(heatmaps_reshaped, 2).reshape((N, K, 1)) 

    preds = np.tile(idx, (1,1,2)).astype(np.float32)
    preds[:,:,0] = preds[:,:,0] % W 
    preds[:,:,1] = preds[:,:,1] // W 
    
    preds = np.where(np.tile(maxvals, (1,1,2)) > 0.0, preds, -1)
    return preds, maxvals

def keypoints_from_heatmaps(heatmaps, model_size):
    heatmaps = heatmaps.copy()

    N, K, H, W = heatmaps.shape
    preds, maxvals = _get_max_preds(heatmaps)
    preds = transform_preds(preds, W, model_size)
    return preds, maxvals

def decode(outputs, model_size, num_clusses, batch_size=1):
    preds, maxvals = keypoints_from_heatmaps(outputs, model_size)
    all_preds = np.zeros((batch_size, num_clusses, 3), dtype=np.float32)
    all_preds[:, :, 0:2] = preds[:, :num_clusses, 0:2]
    all_preds[:, :, 2:3] = maxvals[:,:num_clusses,:]
    return all_preds

head_pos = []
left_pos = []
right_pos = []

def draw(bgr, predict_dict):
    global head_pos, left_pos, right_pos
    head_pos = []
    left_pos = []
    right_pos = []
    for i, all_pred in enumerate(predict_dict):
        for j, (x, y, s) in enumerate(all_pred):
            cv2.circle(bgr, (int(x), int(y)), 3, (0, 255, 120), -1)
            if s > 0:
                cv2.putText(bgr, f'{j}', (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                if j == 0:
                    head_pos.append((x, y))
                elif j == 9:
                    left_pos.append((x, y))
                elif j == 10:
                    right_pos.append((x, y))
    return bgr

def preprocess_image(image, target_size=(512, 512)):
    image = cv2.resize(image, target_size)
    # image = image.astype(np.float32)
    image = np.expand_dims(image, axis=0)
    return image

def check_arms_above_head():
    global head_pos, left_pos, right_pos, STREAM_IP, COMMAND_PORT
    min_hand_distance = 100
    if len(head_pos) > 0:
        head_x, head_y = head_pos[0]

        if len(left_pos) > 0 and len(right_pos) > 0:
            left_x, left_y = left_pos[0]
            right_x, right_y = right_pos[0]
            
            
            hand_distance = np.linalg.norm(np.array([left_x, left_y]) - np.array([right_x, right_y]))

         
            if hand_distance < min_hand_distance:
                print("Please show two hands to the camera or split your hands further apart.")
                return  


        if len(left_pos) > 0:
            left_x, left_y = left_pos[0]

            if left_y < head_y:
                print("Left arm is above head")
                send_command(STREAM_IP, COMMAND_PORT, "right")
                time.sleep(1)  
            else:
                print("Left arm is not above head")


        if len(right_pos) > 0:
            right_x, right_y = right_pos[0]

            if right_y < head_y:
                print("Right arm is above head")
                send_command(STREAM_IP, COMMAND_PORT, "left")
                time.sleep(2)  
            else:
                print("Right arm is not above head")    

STREAM_IP = None
COMMAND_PORT = None

def main():
    global STREAM_IP, COMMAND_PORT
    args = parse_args()
    RKNN_MODEL = args.model
    VIDEO_PATH = args.video
    STREAM_IP = args.stream_ip
    STREAM_PORT = args.stream_port
    MODEL_SIZE = args.size
    NUM_CLUSSES = args.num_clusses
    COMMAND_PORT = args.command_port
    TIME = args.time

    rknn = RKNNLite()

    print("[main] Loading model")
    if not os.path.exists(RKNN_MODEL):
        print("Model not exist")
        exit(-1)
    ret = rknn.load_rknn(RKNN_MODEL)
    if ret != 0:
        print("Load rknn model failed!")
        exit(ret)
    print("Done")

    print("[main] Init runtime environment")
    ret = rknn.init_runtime()
    if ret != 0:
        print("Init runtime environment failed")
        exit(ret)
    print("Done")

    print("[main] Opening video source")
    if VIDEO_PATH.isdigit():
        video_source = int(VIDEO_PATH)
    else:
        video_source = VIDEO_PATH

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error opening video source")
        exit(-1)

    target_width = MODEL_SIZE
    target_height = MODEL_SIZE

    gst_pipeline = f'appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay config-interval=1 pt=96 ! udpsink host={STREAM_IP} port={STREAM_PORT}'
    out = cv2.VideoWriter(gst_pipeline, cv2.CAP_GSTREAMER, 0, 30.0, (target_width, target_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (target_width, target_height))
        img = preprocess_image(resized_frame, target_size=(MODEL_SIZE, MODEL_SIZE))

        print("[main] Running model")
        start = time.time()
        outputs = rknn.inference(inputs=[img])
        if outputs is None:
            print("Inference failed or returned None")
            continue
        outputs = outputs[0]
        end = time.time()
        runTime = end - start
        runTime_ms = runTime * 1000
        if TIME:
            print("Inference Time:", runTime_ms, "ms")
        print("[main] Running postprocess")
        start = time.time()
        predict_dict = decode(outputs, MODEL_SIZE, NUM_CLUSSES)
        out_img = draw(resized_frame, predict_dict)
        check_arms_above_head()
        end = time.time()
        runTime = end - start
        runTime_ms = runTime * 1000
        if TIME:
            print("Postprocess Time:", runTime_ms, "ms")
        out.write(out_img)
    cap.release()
    out.release()
    print("- Complete -")

if __name__ == "__main__":
    main()
