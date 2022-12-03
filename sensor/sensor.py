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
parser.add_argument('-d', '--dest', required=True, help='destination(controller) address (example: 0.0.0.0:30000)')
args = parser.parse_args()


# Get our ip
hostname = socket.gethostname()   
ip_address = socket.gethostbyname(hostname) 
print(ip_address)

# Connect to controller
dest_ip, dest_port = args.dest.split(':')
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.settimeout(20)
send_socket.connect((dest_ip, int(dest_port)))

# Send address for published messages
send_socket.sendall(bytes(f'{ip_address}:{args.port}', 'utf-8'))
send_socket.close()

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
        time.sleep(1)
finally:
    pub_socket.close()
