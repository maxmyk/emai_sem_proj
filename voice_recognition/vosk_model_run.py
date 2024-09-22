import os
import sys
import wave
import pyaudio
from vosk import Model, KaldiRecognizer
import socket
import json

#python3 vosk_model_run.py vosk-model-small-en-us-0.15 --stream-ip 192.168.2.1 --stream-port 5000 --command-port 5565

def parse_args():
    parser = argparse.ArgumentParser(description='Run a pose model on video and stream')
    parser.add_argument('model', help='weights file path')
    parser.add_argument('--stream-ip', help='IP address of the streaming destination', required=True)
    parser.add_argument('--stream-port', help='Port of the streaming destination', type=int, default=5000)
    parser.add_argument('--command-port', help='Port of the command destination', type=int, default=5565)

    args = parser.parse_args()
    return args

def main():
    # Load Vosk model
    args = parse_args()
    vosk_model = args.model
    STREAM_IP = args.stream_ip
    STREAM_PORT = args.stream_port
    COMMAND_PORT = args.command_port
    
    rec = KaldiRecognizer(model, 16000)

    # Initialize audio input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    stream.start_stream()

    print("Listening...")

    # Set up the client


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((stream_ip, stream_port))
        
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