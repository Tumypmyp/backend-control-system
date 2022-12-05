import zmq
import random
import sys
import time
from datetime import datetime
import argparse
import socket

# Parse command arguments
parser = argparse.ArgumentParser(description='Publish sensor messages')
parser.add_argument('-p', '--port', type=int, default=5000, help='port to publish messages on (default: %(default)s)')
parser.add_argument('-d', '--destination', required=True, help='destination(controller) address (example: 0.0.0.0:30000)')
parser.add_argument('-t', '--times-per-second', type=int, default=300, help='number of times per second the sensor sends a message(default: %(default)s)')
args = parser.parse_args()
print(args)


# Get our ip
hostname = socket.gethostname()   
ip_address = socket.gethostbyname(hostname) 
print("ip:", ip_address)

dest_ip, dest_port = args.destination.split(':')

def share_publisher_address(destination, ip_address, port):
    # Connect to controller
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect(destination)
            print('connection successful')
            break
        except socket.error:
            time.sleep(1)

    # Send address for published messages
    s.sendall(bytes(f'{ip_address}:{port}', 'utf-8'))
    s.close()

share_publisher_address((dest_ip, int(dest_port)), ip_address, args.port)

# Start Publisher 
context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f'tcp://*:{args.port}')


try:
    while True:
        # Generate data
        dt = datetime.now().strftime('%Y%m%dT%H%M')
        payload = random.randrange(1, 200)
        data = {'datetime' : dt, 'payload' : payload}

        # Publish the data
        pub_socket.send_json(data)
        time.sleep(1 / args.times_per_second)
finally:
    pub_socket.close()
