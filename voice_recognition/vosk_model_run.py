import os
import sys
import wave
import pyaudio
from vosk import Model, KaldiRecognizer
import socket
import json
import argparse

#python3 vosk_model_run.py /home/orangepi/emai_sem_proj/voice_recognition/vosk-model-small-en-us-0.15 --stream-ip 192.168.2.1 --stream-port 5565 

def parse_args():
    parser = argparse.ArgumentParser(description='Run a pose model on video and stream')
    parser.add_argument('model_path', help='weights file path', type=str)
    parser.add_argument('--stream-ip', help='IP address of the streaming destination', required=True)
    parser.add_argument('--stream-port', help='Port of the streaming destination', type=int, default=5565)


    args = parser.parse_args()
    return args

def main():
    # Load Vosk model
    args = parse_args()
    vosk_model = args.model_path
    STREAM_IP = args.stream_ip
    STREAM_PORT = args.stream_port
    model = Model(vosk_model)
    rec = KaldiRecognizer(model, 16000)

    # Initialize audio input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    stream.start_stream()

    print("Listening...")

    # Set up the client


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((STREAM_IP, STREAM_PORT))
        
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = rec.Result()
                

                # Extract text from the JSON result
                result_json = json.loads(result)
                recognized_text = result_json.get("text", "")  # Get the text field
                print(recognized_text)

                # Send the recognized text to the server
                client_socket.sendall(recognized_text.encode('utf-8'))

if __name__ == "__main__":
    main()
