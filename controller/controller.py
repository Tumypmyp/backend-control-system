import sys
import zmq
import threading
import queue
import socket
import argparse

# Parse command arguments
parser = argparse.ArgumentParser(description='controller')
parser.add_argument('-d', '--dest', required=True, help='manipulator(destination) address (example: 0.0.0.0:10000)')
parser.add_argument('-p', '--port', type=int, default=15000, help='port to listen for new sensors (default: %(default)s)')
args = parser.parse_args()
print(args)



# Start Subscriber
context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.setsockopt(zmq.SUBSCRIBE, b'')



# Start discovering sensors
discover_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
discover_socket.bind(('', args.port))
discover_socket.listen()

# Run discovering in new thread
import discoverer 
sensors_thread = threading.Thread(target=discoverer.add_sensors, args=(discover_socket, sub_socket))
sensors_thread.start()



dest_ip, dest_port = args.dest.split(':')

# Connect to manipulator
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.settimeout(20)
send_socket.connect((dest_ip, int(dest_port)))



import sender
q = queue.Queue()

# Run worker every 5 seconds in new threads
def worker():
    threading.Timer(5.0, worker).start()
    global q
    sender.proccess_messages(q, send_socket)
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
