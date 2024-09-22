# receiver.py
import socket
from pynput import keyboard

# Define a dictionary mapping commands to keyboard actions
COMMANDS = {
    'up': keyboard.Key.up,
    'down': keyboard.Key.down,
    'left': keyboard.Key.left,
    'right': keyboard.Key.right,
    'volume_up': keyboard.Key.media_volume_up,
    'volume_down': keyboard.Key.media_volume_down,
    'play_pause': keyboard.Key.media_play_pause,
    'next': keyboard.Key.media_next,
    'prev': keyboard.Key.media_previous,
}

def handle_command(command):
    if command in COMMANDS: 
        key = COMMANDS[command]
        controller = keyboard.Controller()
        
        
         
        controller.press(key)
        controller.release(key)
        print(f"Executed command: '{command}'")
    else:
        print(f"Unknown command: '{command}'")

def start_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"Listening for commands on {ip}:{port}")

    while True:
        message, _ = sock.recvfrom(1024)
        command = message.decode()
        handle_command(command)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Receive UDP commands and simulate key presses.")
    parser.add_argument("ip", help="IP address to bind to")
    parser.add_argument("port", type=int, help="Port to bind to")
    return parser.parse_args()

def main():
    args = parse_args()
    start_server(args.ip, args.port)

if __name__ == "__main__":
    main()
