import sys
import zmq
import threading
import queue
import socket
import argparse
import multiprocessing

# Parse command arguments
parser = argparse.ArgumentParser(description='controller')
parser.add_argument('-d', '--destination', required=True, help='manipulator(destination) address (example: 0.0.0.0:10000)')
parser.add_argument('-p', '--port', type=int, default=15000, help='port to listen for new sensors (default: %(default)s)')
parser.add_argument('-s', '--server-port', type=int, default=20000, help='port to serve the status on (default: %(default)s)')
args = parser.parse_args()
print(args)



# Start Subscriber
context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.setsockopt(zmq.SUBSCRIBE, b'')


# Run discovering in new thread
import discoverer
sensors_thread = threading.Thread(target=discoverer.discover_sensors, args=(args.port, sub_socket, ))
sensors_thread.start()


dest_ip, dest_port = args.destination.split(':')

# Connect to manipulator
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.settimeout(10)
send_socket.connect((dest_ip, int(dest_port)))


status = multiprocessing.Manager().dict({'datetime': '', 'Status': ''})

# Serve the status
import server
server_process = multiprocessing.Process(target=server.serve, args=(status, args.server_port, ))
server_process.start()


import sender
q = queue.Queue()

# Run worker every 5 seconds in new threads
def worker():
    threading.Timer(5.0, worker).start()
    global q
    sender.proccess_messages(q, send_socket, status)
    q = queue.Queue()

worker()

# Recieve messages from sensors
try:
    while True:
        message = sub_socket.recv_json()
        q.put(message)
finally:
    sub_socket.close()

send_socket.close()
