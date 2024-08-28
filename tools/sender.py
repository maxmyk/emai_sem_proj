# sender.py
import socket
import argparse

def send_command(ip, port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(command.encode(), (ip, port))
        print(f"Sent command: '{command}' to {ip}:{port}")
    finally:
        sock.close()

def parse_args():
    parser = argparse.ArgumentParser(description="Send UDP commands.")
    parser.add_argument("ip", help="IP address of the receiver")
    parser.add_argument("port", type=int, help="Port of the receiver")
    parser.add_argument("command", help="Command to send")
    return parser.parse_args()

def main():
    args = parse_args()
    send_command(args.ip, args.port, args.command)

if __name__ == "__main__":
    main()
