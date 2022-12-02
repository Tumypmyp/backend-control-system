import sys
import zmq
import threading
import queue

import socket
import argparse

parser = argparse.ArgumentParser(description='controller')
parser.add_argument('-d', '--dest', required=True, help='manipulator(destination) IP address')
parser.add_argument('-s', '--source', nargs='+', help='sensor(sourse) IP addresses')
args = parser.parse_args()

print(args)


dest_port = 10000
src_port = 5000



context = zmq.Context()
sub_socket = context.socket(zmq.SUB)

for address in args.source:
    sub_socket.connect(f'tcp://{address}:{src_port}')


sub_socket.setsockopt(zmq.SUBSCRIBE, b'')

send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.connect((args.dest, dest_port))



import sender
q = queue.Queue()

def worker():
    threading.Timer(5.0, worker).start()
    global q
    sender.proccess_messages(q, send_socket)
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
