import sys
import zmq
import threading
import queue
from datetime import datetime
port = '5556'
if len(sys.argv) > 1:
    port =  sys.argv[1]

if len(sys.argv) > 2:
    port1 =  sys.argv[2]


context = zmq.Context()
sub_socket = context.socket(zmq.SUB)

print('Collecting updates from weather server...')
sub_socket.connect(f'tcp://localhost:{port}')

if len(sys.argv) > 2:
    sub_socket.connect(f'tcp://localhost:{port1}')

sub_socket.setsockopt(zmq.SUBSCRIBE, b'')

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 40000))

import pickle

q = queue.Queue()

def use_messages(q):
    sum = 0
    size = 0
    while not q.empty():
        m = q.get()
        sum += m['payload']
        size += 1
    print('Result:', sum, size)

    dt = datetime.now().strftime('%Y%m%dT%H%M')
    result = {'datetime': dt, 'Status': 'up' if sum % 2 == 0 else 'down'}
    s.sendall(pickle.dumps(result))



def worker():
    threading.Timer(5.0, worker).start()
    global q
    use_messages(q)
    q = queue.Queue()

worker()

while True:
    message = sub_socket.recv_json()
    print(message)
    q.put(message)

s.close()
