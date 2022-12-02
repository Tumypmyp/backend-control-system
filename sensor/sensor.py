import zmq
import random
import sys
import time
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description='Publish sensor messages')
parser.add_argument('-p', '--port', type=int, default=5000, help='port to publish messages on (default: %(default)s)')
args = parser.parse_args()

context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f'tcp://*:{args.port}')

try:
    while True:
        dt = datetime.now().strftime('%Y%m%dT%H%M')
        payload = random.randrange(1, 200)
        data = {'datetime' : dt, 'payload' : payload}
        print(data)

        pub_socket.send_json(data)
        time.sleep(1)
finally:
    pub_socket.close()
