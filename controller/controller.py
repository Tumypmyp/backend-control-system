import sys
import zmq
import threading
import queue
from datetime import datetime

import socket
import pickle
import argparse

parser = argparse.ArgumentParser(description='controller')
parser.add_argument('-d', '--dest', required=True, help='manipulator(destination) IP address')
parser.add_argument('-s', '--source', nargs='+', help='sensor(sourse) IP addresses')
args = parser.parse_args()

print(args)
dest_port = 5000
src_port = 6000



context = zmq.Context()
sub_socket = context.socket(zmq.SUB)

for address in args.source:
    sub_socket.connect(f'tcp://{address}:{src_port}')
sub_socket.setsockopt(zmq.SUBSCRIBE, b'')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.dest, dest_port))



q = queue.Queue()

def use_messages(q):
    sum = 0
    size = 0
    while not q.empty():
        m = q.get()
        sum += m['payload']
        size += 1
    print('Result:', sum, size)

    send_status('up' if sum % 2 == 0 else 'down')

def send_status(status):
    dt = datetime.now().strftime('%Y%m%dT%H%M')
    result = {'datetime': dt, 'Status': status}
    s.sendall(pickle.dumps(result))



def worker():
    threading.Timer(5.0, worker).start()
    global q
    use_messages(q)
    q = queue.Queue()

worker()

try:
    while True:
        message = sub_socket.recv_json()
        print(message)
        q.put(message)
finally:
    sub_socket.close()
    s.close()
